'''
views.py: part of expfactory package

Copyright (c) 2017, Vanessa Sochat
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

* Redistributions of source code must retain the above copyright notice, this
  list of conditions and the following disclaimer.

* Redistributions in binary form must reproduce the above copyright notice,
  this list of conditions and the following disclaimer in the documentation
  and/or other materials provided with the distribution.

* Neither the name of the copyright holder nor the names of its
  contributors may be used to endorse or promote products derived from
  this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

'''

from flask import (
    flash,
    render_template, 
    request, 
    redirect,
    session
)

from flask_wtf.csrf import generate_csrf
from flask_cors import cross_origin
from expfactory.logger import bot
from werkzeug import secure_filename
from expfactory.utils import (
    convert2boolean, 
    getenv,
    get_post_fields
)


from expfactory.database import save_data
from expfactory.server import app
from random import choice
import os
import pickle

from expfactory.forms import ParticipantForm


# SECURITY #####################################################################

@app.after_request
def inject_csrf_token(response):
    response.headers.set('X-CSRF-Token', generate_csrf())
    return response
  

# EXPERIMENT PORTAL ############################################################

@app.route('/experiments')
def experiment_base():
    return render_template('experiments/index.html')


# Home portal to start experiments
@app.route('/', methods=['GET', 'POST'])
def home():

    form = ParticipantForm()

    if request.method == "POST":   

        print('SESSION')
        print(session)
        # Submit and valid
        if form.validate_on_submit():

            # User name is not required
            username = 'You'
            if form.openid.data not in [None,""]:
                username = form.openid.data

            session['username'] = username
            session['experiments'] = form.exp_ids.data.split(',') # list
            flash('Participant ID: "%s", Experiments: %s' %
                  (username,
                  str(form.exp_ids.data)))
            return redirect('/start')

        # Submit but not valid
        return render_template('portal/index.html', experiments=app.lookup,
                                                    base=app.base,
                                                    form=form, toggleform=True)

    # Not submit
    return render_template('portal/index.html', experiments=app.lookup,
                                                base=app.base,
                                                form=form)


# EXPERIMENT ROUTER ############################################################


@app.route('/next', methods=['POST', 'GET'])
def next():
    print(request)
    if request.method == 'POST':
        fields = get_post_fields(request)
        res = {'session':session, 'fields':fields}
        pickle.dump(res, open('/tmp/result.pkl','wb'))
        result_file = save_data(session, fields)
        print(result_file)

    username = session.get('username')
    if username is None:
        flash('You must start a session before doing experiments.')
        return redirect('/')

    experiment = app.get_next(session)
    if experiment is None:
        flash('Congratulations, you have finished the battery!')
        return redirect('/finish')

    return redirect('http://127.0.0.1/experiments/%s' %experiment)


# Reset/Logout
@app.route('/logout', methods=['POST', 'GET'])
def logout():

    # If the user has finished, clear session
    del session['expfactory_subid']
    del session['username']
    del session['experiments']
    return redirect('/')


# Finish
@app.route('/finish', methods=['POST', 'GET'])
def finish():

    # If the user has finished, clear session
    del session['expfactory_subid']
    del session['username']
    del session['experiments']

    #TODO: need to handle POST with CSRF, document standard post
    # create local result database and option to use "real" db - both
    # should be easy to do / switch based on environment setting.
    return render_template('finish/index.html')



@app.route('/start')
def start():
    '''start a battery.
    '''
    username = session.get('username')
    if username is None:
        flash('You must start a session before doing experiments.')
        return redirect('/')

    # If the user hasn't started, assign new subid
    if not session.get('expfactory_subid'):
        session['expfactory_subid'] = generate_subid()

    print('SESSION')
    print(session)
    print(request.headers)
    return render_template('start/index.html')

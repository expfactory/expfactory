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
from expfactory.views.utils import (
    perform_checks, 
    clear_session
)
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

            if not session.get('subid'):
                subid = generate_subid()
                session['subid'] = subid

            session['username'] = username
            session['experiments'] = form.exp_ids.data.split(',') # list
            flash('Participant ID: "%s", Name %s, Experiments: %s' %
                  (subid, username,
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
    if request.method == 'POST':
        fields = get_post_fields(request)
        exp_id = session.get('exp_id')
        result_file = save_data(session=session, fields=fields, exp_id=exp_id)
        print(result_file)

    # Redirects to another template view
    return perform_checks('/experiments/%s' %experiment, do_redirect=True)


# Reset/Logout
@app.route('/logout', methods=['POST', 'GET'])
def logout():

    # If the user has finished, clear session
    clear_session()
    return redirect('/')


# Finish
@app.route('/finish', methods=['POST', 'GET'])
def finish():

    # If the user has finished, clear session
    clear_session()

    #TODO: need to handle POST with CSRF, document standard post
    # create local result database and option to use "real" db - both
    # should be easy to do / switch based on environment setting.
    return render_template('finish/index.html')



@app.route('/start')
def start():
    '''start a battery.
    '''
    return perform_checks('start/index.html')

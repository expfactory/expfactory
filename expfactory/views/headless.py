'''
headless.py: part of expfactory package

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
    jsonify,
    render_template, 
    request, 
    redirect,
    session
)

from flask_wtf.csrf import generate_csrf
from flask_cors import cross_origin
from expfactory.defaults import EXPFACTORY_LOGS
from werkzeug import secure_filename
from expfactory.utils import get_post_fields

from expfactory.views.utils import (
    perform_checks, 
    clear_session
)
from expfactory.server import app
from random import choice
import logging
import os
import json

from expfactory.forms import EntryForm


# HEADLESS LOGIN ###############################################################

@app.route('/login', methods=['POST'])
def login():

    # Only allowed to login via post from entry (headless) url
    form = EntryForm()

    # If not headless, we don't need to login
    if not app.headless:
        app.logger.debug('Not running in headless mode, redirect to /start.')
        redirect('/start')

    subid = session.get('subid')
    if not subid:
        if form.validate_on_submit():
            token = form.token.data

            subid = app.validate_token(token)
            if subid is None:
                return headless_denied(form=form)

            session['subid'] = subid
            session['token'] = token

            app.logger.info('Logged in user [subid] %s' %subid)
    return redirect('/next')


# Denied Entry for Headless
def headless_denied(form=None):
    if form is None:
        form = EntryForm()
    message = "A valid token is required. Contact the experiment administrator if you believe this to be a mistake."
    return render_template('routes/entry.html', form=form,
                                                message=message)

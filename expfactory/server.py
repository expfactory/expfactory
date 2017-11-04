'''
Copyright (c) 2016-2017 Vanessa Sochat

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

'''

from expfactory.experiment import (
    get_experiments, 
    make_lookup,
    get_selection
)

from flask import (
    Blueprint,
    Flask, 
    render_template, 
    request, 
    flash
)
from flask_restful import Resource, Api
from flask_wtf.csrf import (
    CSRFProtect, 
    generate_csrf
)
from flask_cors import CORS
from expfactory.logger import bot
from werkzeug import secure_filename
from expfactory.utils import (
    convert2boolean, 
    getenv
)

import jinja2
import tempfile
import shutil
import random
import sys
import os

# SERVER CONFIGURATION #########################################################

class EFServer(Flask):

    def __init__(self, *args, **kwargs):
        super(EFServer, self).__init__(*args, **kwargs)
        
        self.setup()
        self.initdb()

        # Completed will go into list
        self.completed = []

    def initdb(self):
        '''initdb will check for writability of the data folder, meaning
           that it is bound to the local machine. If the folder isn't bound,
           expfactory runs in demo mode (not saving data)
        '''

        self.data = getenv('EXPFACTORY_DATA','/scif/data')
        if not os.access(self.data, os.W_OK):
            bot.warning("%s is not writable, running in demo mode." %self.data)
            self.data = None

        if self.data is not None:
            bot.log("Data base: %s" %self.data)


    def setup(self):

        # Step 1: obtain installed and selected experiments (/scif/apps)
        self.selection = getenv('EXPFACTORY_EXPERIMENTS', [])
        self.base = getenv('EXPFACTORY_BASE')

        self.randomize = convert2boolean(getenv('EXPFACTORY_RANDOM', True))
        available = get_experiments("%s" % self.base)
        self.experiments = get_selection(available, self.selection)
        bot.debug(self.experiments)
        self.lookup = make_lookup(self.experiments)
        final = "\n".join(list(self.lookup.keys()))        

        bot.log("User has selected: %s" %self.selection)
        bot.log("Experiments Available: %s" %"\n".join(available))
        bot.log("Randomize: %s" % self.randomize)
        bot.log("Final Set \n%s" % final)
       

    def get_next(self, session):
        '''return the name of the next experiment, depending on the user's
           choice to randomize. We don't remove any experiments here, that is
           done on finish, in the case the user doesn't submit data (and
           thus finish). A return of None means the user has completed the
           battery of experiments.
        '''
        next = None
        experiments = session.get('experiments', [])
        if len(experiments) > 0:    
            if app.randomize is True:
                next = random.choice(range(0,len(experiments)))
                print(next)
                print(experiments)
                next = experiments[next]
        return next


app = EFServer(__name__)
app.config.from_object('expfactory.config')

# EXPERIMENTS #################################################################

# Cors
cors = CORS(app, origins="http://127.0.0.1", 
            allow_headers=["Content-Type", 
                           "Authorization", 
                           "X-Requested-With",
                           "Access-Control-Allow-Credentials"],
            supports_credentials=True)

app.config['CORS_HEADERS'] = 'Content-Type'

csrf = CSRFProtect(app)

import expfactory.views
import expfactory.api

# This is how the command line version will run
def start(port=5000, debug=False):
    bot.info("Nobody ever comes in... nobody ever comes out...")
    app.run(host="localhost", debug=debug, port=port)

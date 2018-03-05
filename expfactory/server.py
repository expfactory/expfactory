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

from expfactory.database import *
from flask import Flask
from flask_wtf.csrf import (
    CSRFProtect, 
    generate_csrf
)
from expfactory.variables import generate_runtime_vars
from flask_cors import CORS
from expfactory.logger import bot
from expfactory.defaults import *

import random
import sys
import os

# SERVER CONFIGURATION #########################################################

class EFServer(Flask):

    def __init__(self, *args, **kwargs):
        super(EFServer, self).__init__(*args, **kwargs)
        
        self.setup()
        self.initdb()


    def initdb(self):
        '''initdb will check for writability of the data folder, meaning
           that it is bound to the local machine. If the folder isn't bound,
           expfactory runs in demo mode (not saving data)
        '''

        self.database = EXPFACTORY_DATABASE
        bot.info("DATABASE: %s" %self.database)

        # Supported database options
        valid = ('sqlite', 'postgres', 'mysql', 'filesystem')
        if not self.database.startswith(valid):
            bot.warning('%s is not yet a supported type, saving to filesystem.' % self.database)
            self.database = 'filesystem'

        # Add functions specific to database type
        self.init_db() # uses url in self.database

        bot.log("Data base: %s" % self.database)


    def setup(self):
        ''' obtain database and filesystem preferences from defaults,
            and compare with selection in container.
        '''

        self.selection = EXPFACTORY_EXPERIMENTS
        self.ordered = len(EXPFACTORY_EXPERIMENTS) > 0
        self.data_base = EXPFACTORY_DATA
        self.study_id = EXPFACTORY_SUBID
        self.base = EXPFACTORY_BASE
        self.randomize = EXPFACTORY_RANDOMIZE
        self.headless = EXPFACTORY_HEADLESS

        # Generate variables, if they exist
        self.vars = generate_runtime_vars() or None

        available = get_experiments("%s" % self.base)
        self.experiments = get_selection(available, self.selection)
        self.logger.debug(self.experiments)
        self.lookup = make_lookup(self.experiments)
        final = "\n".join(list(self.lookup.keys()))       

        bot.log("Headless mode: %s" % self.headless)
        bot.log("User has selected: %s" % self.selection)
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
                next = experiments[next]
            else:
                next = experiments[0]
        return next


    def finish_experiment(self, session, exp_id):
        '''remove an experiment from the list after completion.
        '''
        self.logger.debug('Finishing %s' %exp_id)
        experiments = session.get('experiments', [])
        experiments = [x for x in experiments if x != exp_id]
        session['experiments'] = experiments
        return experiments


EFServer.init_db = init_db
EFServer.save_data = save_data
EFServer.generate_subid = generate_subid
EFServer.generate_user = generate_user

# Tokens
EFServer.validate_token = validate_token
EFServer.refresh_token = refresh_token
EFServer.revoke_token = revoke_token

# User Actions
EFServer.list_users = list_users
EFServer.print_user = print_user
EFServer.finish_user = finish_user
EFServer.restart_user = restart_user

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

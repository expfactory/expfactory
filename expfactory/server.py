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

from flask import Flask, render_template, request
from flask_restful import Resource, Api
from expfactory.logman import bot
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

# SERVER CONFIGURATION ##############################################
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
        self.selection = getenv('EXPERIMENTS', [])
        self.base = getenv('EXPFACTORY_BASE','/scif/apps')
        self.randomize = convert2boolean(getenv('EXPFACTORY_RANDOM', True))
        available = get_experiments("%s" % self.base)
        self.experiments = get_selection(available, self.selection)
        self.lookup = make_lookup(self.experiments)
        final = "\n".join(list(self.lookup.keys()))        

        bot.log("User has selected: %s" %self.selection)
        bot.log("Experiments Available: %s" %"\n".join(available))
        bot.log("Randomize: %s" % self.randomize)
        bot.log("Final Set \n%s" % final)
       

    def get_next(self):
        '''return the name of the next experiment, depending on the user's
           choice to randomize
        '''
        # TODO: this should be looked up based on participant ID
        next = 0
        if app.randomize is True:
            next = choice(range(0,len(self.experiments)))
        next_experiment = self.experiments.pop(next)


app = EFServer(__name__)
app.config['ALLOWED_EXTENSIONS'] = set(['png', 'jpg', 'jpeg','gif'])

    
# For a given file, return whether it's an allowed type or not
def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']


# This is how the command line version will run
def start(port=5000, debug=True):
    bot.info("Nobody ever comes in... nobody ever comes out...")
    import expfactory.api
    app.run(host="0.0.0.0", debug=debug, port=port)
    

if __name__ == '__main__':
    start()

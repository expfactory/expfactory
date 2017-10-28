'''
api.py: part of expfactory package

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

from expfactory.logman import bot
from expfactory.server import app
import os


# API VIEWS ####################################################################

class apiExperiments(Resource):
    '''apiExperiments
    Main view for REST API to display all available experiments
    '''
    def get(self):
        return app.lookup
        
class apiExperimentSingle(Resource):
    '''apiExperimentSingle
    return complete meta data for specific experiment
    :param exp_id: exp_id for experiment to preview
    '''
    def get(self, exp_id):
        return {exp_id: app.lookup[exp_id]}


# Create custom loader with experiments to serve
#loader = jinja2.ChoiceLoader([
#             app.jinja_loader,
#             jinja2.FileSystemLoader(['/scif/apps'])
#         ])

#app.jinja_loader = loader

#import pickle
#pickle.dump(loader,open('loader.pkl','wb'))

api = Api(app)    
api.add_resource(apiExperiments,'/experiments')
api.add_resource(apiExperimentSingle,'/experiments/<string:exp_id>')

'''
api.py: part of expfactory package

Copyright (c) 2017-2019, Vanessa Sochat
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

from flask_restful import Resource, Api
from expfactory.logger import bot
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
        return app.lookup[exp_id]


# Create custom loader with experiments to serve
#loader = jinja2.ChoiceLoader([
#             app.jinja_loader,
#             jinja2.FileSystemLoader(['/scif/apps'])
#         ])

#app.jinja_loader = loader

#import pickle
#pickle.dump(loader,open('loader.pkl','wb'))

api = Api(app)    
api.add_resource(apiExperiments,'/api/experiments')
api.add_resource(apiExperimentSingle,'/api/experiments/<string:exp_id>')

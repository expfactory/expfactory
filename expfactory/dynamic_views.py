'''
dynamic_views.py: part of expfactory package

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
    Blueprint,
    flash,
    render_template, 
    request, 
    redirect,
    session
)

from flask_wtf.csrf import generate_csrf
from flask_cors import cross_origin
from expfactory.logman import bot
from werkzeug import secure_filename
from expfactory.utils import (
    convert2boolean, 
    getenv,
    get_post_fields
)


from expfactory.database import generate_subid
from expfactory.server import app
import os

# TODO: These experiment blueprints will be automatically generated on build

test_task = Blueprint('test-task', __name__,
                       static_url_path='/experiments', 
                       static_folder='/scif/apps/test-task',
                       template_folder='/scif/apps')

@test_task.route('/experiments/test-task')
def test_task_base():
    experiment = 'test-task/index.html'
    return render_template('experiments/experiment.html', experiment=experiment)

test_task.before_request(csrf.protect)
app.register_blueprint(test_task)

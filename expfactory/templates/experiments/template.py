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
from expfactory.logger import bot

from flask import (
    Blueprint,
    render_template, 
)
from expfactory.views.utils import (
    perform_checks, 
    clear_session
)
from expfactory.server import app, csrf
import os


{{ exp_id_python }} = Blueprint('{{ exp_id }}', __name__,
                                static_url_path='/experiments/{{ exp_id }}', 
                                static_folder='/scif/apps/{{ exp_id }}',
                                template_folder='/scif/apps')

@{{ exp_id_python }}.route('/experiments/{{ exp_id }}/')
def {{ exp_id_python }}_base():
    context = {'experiment': '{{ exp_id }}/index.html'}
    return perform_checks('experiments/experiment.html', quiet=True,
                                                         context=context,
                                                         next="{{ exp_id }}")

{{ exp_id_python }}.before_request(csrf.protect)
app.register_blueprint({{ exp_id_python }})

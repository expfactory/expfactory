'''

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

from expfactory.validator import ExperimentValidator
from expfactory.experiment import load_experiment
from expfactory.utils import (
    get_template, 
    sub_template,
    get_viewsdir
)
from expfactory.logger import bot
import tempfile
import sys
import os


def main(args,parser,subparser):

    folder = args.folder
    if folder is None:
        folder = os.getcwd()

    print(args.src)
    source = args.src[0]
    if source is None:
        bot.error('Please provide a Github http address to install.')
        sys.exit(1)

    # Is the experiment valid?
    cli = ExperimentValidator()
    result = cli.validate(source, cleanup=False)
    if result is True:
        config = load_experiment("%s/%s" %(cli.tmpdir,exp_id))
        exp_id = config['exp_id']

    # Move static files to output folder
    folder = "%s/%s" %(folder,exp_id)

    bot.log("Installing %s to %s" %(exp_id, folder))
    os.system('mkdir -p %s' %folder)

    bot.log("Preparing experiment routes...")
    template = get_template('experiments/template.py')
    template = sub_template(template, '{{ exp_id }}', exp_id)

    # 1. Python blueprint
    views = "%s/experiments" % get_viewsdir()
    python_module = exp_id.replace('-','_').lower()
    view_output = "%s/%s.py" %(views, python_module)
    save_template(template, views_output, base=views)
    
    # 2. append to __init__
    init = "%s/__init__.py" % views
    with open(init,'a') as filey:
        filey.writelines('from .%s import *\n' %python_module)

    # 3. Instructions
    if "instructions" in config:
        instruct = "%s/%s.help" %(views, python_module)
    with open(instruct,'w') as filey:
        filey.writelines(config['instructions'])
    
    

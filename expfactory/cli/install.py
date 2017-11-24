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
    get_viewsdir,
    get_template, 
    run_command,
    sub_template,
    save_template
)
from expfactory.logger import bot
import tempfile
import sys
import os


def main(args,parser,subparser):

    folder = args.folder
    if folder is None:
        folder = os.getcwd()

    source = args.src[0]
    if source is None:
        bot.error('Please provide a Github https address to install.')
        sys.exit(1)

    # Is the experiment valid?
    cli = ExperimentValidator()
    valid = cli.validate(source, cleanup=False)
    exp_id = os.path.basename(source).replace('.git','')

    if valid is True:

        # Local Install
        if os.path.exists(source):
            config = load_experiment(source)
            source = os.path.abspath(source)
        else:
            config = load_experiment("%s/%s" %(cli.tmpdir,exp_id))
            source = "%s/%s" %(cli.tmpdir,exp_id)

        exp_id = config['exp_id']
        python_module = exp_id.replace('-','_').lower()
    else:
        bot.error('%s is not valid.' % exp_id)
        sys.exit(1)

    # Move static files to output folder
    dest = "%s/%s" %(folder,exp_id)

    bot.log("Installing %s to %s" %(exp_id, dest))
    
    # Building container
    in_container = False
    if os.environ.get('SINGULARITY_IMAGE') is not None:
        in_container = True

    # Running, live container
    elif os.environ.get('EXPFACTORY_CONTAINER') is not None:
        in_container = True

    if in_container is True:

        # if in container, we always force
        args.force = True

        bot.log("Preparing experiment routes...")
        template = get_template('experiments/template.py')
        template = sub_template(template, '{{ exp_id }}', exp_id)
        template = sub_template(template, '{{ exp_id_python }}', python_module)

        # 1. Python blueprint
        views = get_viewsdir(base=args.base)
        view_output = "%s/%s.py" %(views, python_module)
        save_template(view_output, template, base=views)
    
        # 2. append to __init__
        init = "%s/__init__.py" % views
        with open(init,'a') as filey:
            filey.writelines('from .%s import *\n' %python_module)

        # 3. Instructions
        if "instructions" in config:
            instruct = "%s/%s.help" %(views, python_module)
        with open(instruct,'w') as filey:
            filey.writelines(config['instructions'])

    if not os.path.exists(dest):
        os.system('mkdir -p %s' %dest)
    else:
        if args.force is False:
            bot.error('%s is not empty! Use --force to delete and re-create.' %folder)
            sys.exit(1) 

    # We don't need to copy if experiment already there
    if source != dest:
        os.system('cp -R %s/* %s' %(source, dest))

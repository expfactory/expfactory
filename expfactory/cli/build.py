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

from expfactory.utils import (
    copy_directory,
    get_templatedir,
    get_template,
    sub_template,
    write_file
)
from expfactory.experiment import (
    get_library, 
    load_experiment
)
from expfactory.validator import ExperimentValidator
from expfactory.logger import bot
from glob import glob
import tempfile
import sys
import os


def main(args,parser,subparser):

    template = 'build/docker/Dockerfile.template'

    # Full path to template is required if provided via input
    if args.input is not None:
        template = args.input

    template = get_template(template)
    
    # For now, only one database provided
    database = args.database
    studyid = args.studyid
    experiments = args.experiments
    branch = "-b %s" %os.environ.get('EXPFACTORY_BRANCH','master')

    headless = "false"
    if args.headless is True:
        headless = "true"

    template = sub_template(template,"{{studyid}}",studyid)
    template = sub_template(template,"{{database}}",database)
    template = sub_template(template,"{{headless}}",headless)
    template = sub_template(template,"{{branch}}",branch)

    if args.headless is True:
        bot.info("Headless build detected, you will need to generate tokens for application entry with expfactory users --new")

    library = get_library(key='name')

    apps = "\n"

    # Add local experiments to library, first preference
    local_installs = 0
    for experiment in experiments:
        if os.path.exists(experiment):

            bot.info('local experiment %s found, validating...' %experiment)

            # Is the experiment valid?
            cli = ExperimentValidator()
            valid = cli.validate(experiment, cleanup=False)

            if valid is True:
                local_installs +=1
                config = load_experiment(experiment)
                exp_id = config['exp_id']

                # If we aren't building in the experiment directory, we need to copy there
                output_dir = "%s/%s" %(os.path.abspath(os.path.dirname(args.output)), exp_id)
                experiment_dir = os.path.abspath(experiment)
                if output_dir != experiment_dir:
                    copy_directory(experiment_dir, output_dir)

                config['local'] = os.path.abspath(experiment)
                library[exp_id] = config


    # Warn the user that local installs are not reproducible (from recipe)
    if local_installs > 0:
        bot.warning("%s local installs detected: build is not reproducible without experiment folders" %local_installs)

    # Build Image with Experiments
    for experiment in experiments:
        exp_id = os.path.basename(experiment)
        if exp_id in library:
            config = library[exp_id]

            app = "LABEL EXPERIMENT_%s /scif/apps/%s\n" %(exp_id, exp_id)

            # Here add custom build routine, should be list of lines
            if "install" in config:
                commands = "\n".join(["RUN %s "%s for x in config['install']]).strip('\n')
                app = "%s%s\n" %(app, commands)

            # The final installation step, either from Github (url) or local folder
            if "local" in config:
                app = "%sADD %s /scif/apps/%s\n" %(app, exp_id, exp_id)
                app = "%sWORKDIR /scif/apps\nRUN expfactory install %s\n" %(app, exp_id)
            else:
                app = "%sWORKDIR /scif/apps\nRUN expfactory install %s\n" %(app, config['github'])  
            apps = "%s%s\n" %(apps,app)


        else:
            bot.warning('%s not in library, check spelling & punctuation.' %exp_id)

    if apps == "\n":
        bot.error('No valid experiments found, cancelling recipe build.')
        sys.exit(1)

    template = sub_template(template,"{{experiments}}",apps)
    outfile = write_file(args.output,template)
    bot.log("Recipe written to %s" %outfile)

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
    get_templatedir,
    get_template,
    sub_template,
    write_file
)
from expfactory.experiment import get_library
from expfactory.logger import bot
from glob import glob
import tempfile
import sys
import os


def main(args,parser,subparser):

    # List of experiments is required
    template = get_template('build/docker/Dockerfile.template')
    
    # For now, only one database provided
    database = args.database
    studyid = args.studyid
    experiments = args.experiments
    
    template = sub_template(template,"{{studyid}}",studyid)
    template = sub_template(template,"{{database}}",database)

    library = get_library(key='name')

    apps = "\n"
    for experiment in experiments:
        if experiment in library:
            config = library[experiment]
            app = "LABEL EXPERIMENT_%s /scif/apps/%s\n" %(experiment,experiment)

            # Here add custom build routine, should be list of lines
            if "install" in config:
                commands = "\n".join(["RUN %s "%s for x in config['install']]).strip('\n')
                app = "%s%s\n" %(app, commands)

            # The final installation step
            app = "%sWORKDIR /scif/apps\nRUN expfactory install %s\n\n" %(app,config['github'])  
            apps = "%s%s\n" %(apps,app)

        else:
            bot.warning('%s not in library, check spelling & punctuation.' %experiment)

    if apps == "\n":
        bot.error('No valid experiments found, cancelling recipe build.')
        sys.exit(1)

    template = sub_template(template,"{{experiments}}",apps)
    outfile = write_file(args.output,template)
    bot.log("Recipe written to %s" %outfile)

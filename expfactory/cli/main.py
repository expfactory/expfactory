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

from expfactory.logger import bot
from glob import glob
import tempfile
import sys
import os


def main(args,parser,subparser=None):
    '''this is the main entrypoint for a container based web server, with
       most of the variables coming from the environment. See the Dockerfile
       template for how this function is executed.

    '''

    # First priority to args.base
    base = args.base
    if base is None:
        base = os.environ.get('EXPFACTORY_BASE')

    # Does the base folder exist?
    if base is None:
        bot.error("You must set a base of experiments with --base" % base)
        sys.exit(1)

    if not os.path.exists(base):
        bot.error("Base folder %s does not exist." % base)
        sys.exit(1)

    # Export environment variables for the client
    experiments = args.experiments
    if experiments is None:
        experiments = " ".join(glob("%s/*" % base))

    os.environ['EXPFACTORY_EXPERIMENTS'] = experiments

    # If defined and file exists, set runtime variables
    if args.vars is not None:
        if os.path.exists(args.vars):
            os.environ['EXPFACTORY_RUNTIME_VARS'] = args.vars
            os.environ['EXPFACTORY_RUNTIME_DELIM'] = args.delim
        else:
            bot.warning('Variables file %s not found.' %args.vars)


    subid = os.environ.get('EXPFACTORY_STUDY_ID')
    if args.subid is not None:
        subid = args.subid 
        os.environ['EXPFACTORY_SUBID'] = subid

    os.environ['EXPFACTORY_RANDOM'] = str(args.disable_randomize)
    os.environ['EXPFACTORY_BASE'] = base
    
    from expfactory.server import start
    start(port=5000)

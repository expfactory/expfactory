'''

defaults.py: this script acts as a gateway between variables defined at
runtime, and defaults. Any variable that has an unchanging default value 
can be found here. The order of operations works as follows:
  
    1. First preference goes to environment variable set at runtime
    2. Second preference goes to default defined in this file
    3. Then, if neither is found, null is returned except in the 
       case that required = True. A required = True variable not found
       will system exit with an error.

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
    convert2boolean, 
    getenv
)
import tempfile
import os
import pwd
import sys


#######################################################################
# Expfactory Registry
#######################################################################

EXPFACTORY_REGISTRY = getenv("EXPFACTORY_REGISTRY_BASE",
                             default="https://expfactory.github.io")

EXPFACTORY_LIBRARY = "%s/experiments/library.json" %(EXPFACTORY_REGISTRY)

EXPFACTORY_SERVER = getenv('EXPFACTORY_SERVER', 'localhost')


#######################################################################
# Expfactory Database
#######################################################################

EXPFACTORY_LOGS = getenv('EXPFACTORY_LOGS', '/scif/logs')
EXPFACTORY_DATABASE = getenv('EXPFACTORY_DATABASE', 'filesystem')
EXPFACTORY_BASE = getenv('EXPFACTORY_BASE', '/scif/apps')
EXPFACTORY_DATA = getenv('EXPFACTORY_DATA', '/scif/data')


#######################################################################
# Expfactory Experiments
#######################################################################

EXPFACTORY_SUBID = getenv('EXPFACTORY_STUDY_ID', 'expfactory')
EXPFACTORY_EXPERIMENTS = getenv('EXPFACTORY_EXPERIMENTS', [])
EXPFACTORY_RANDOMIZE = convert2boolean(getenv('EXPFACTORY_RANDOM', True))
EXPFACTORY_HEADLESS = convert2boolean(getenv('EXPFACTORY_HEADLESS', False))

# Runtime Variables
EXPFACTORY_RUNTIME_VARS = getenv('EXPFACTORY_RUNTIME_VARS')
EXPFACTORY_RUNTIME_DELIM = getenv('EXPFACTORY_RUNTIME_DELIM', ',')


#######################################################################
# Formatting
#######################################################################

COLORIZE = getenv("EXPFACTORY_COLORIZE", default=None)
if COLORIZE is not None:
    COLORIZE = convert2boolean(COLORIZE)

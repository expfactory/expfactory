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
from flask import session
from expfactory.logger import bot
from expfactory.utils import write_json
from expfactory.defaults import (
    EXPFACTORY_SUBID,
    EXPFACTORY_DATA
)
from glob import glob
import os
import sys


# DEFAULT FLAT #################################################################
# Default "database" is flat files written to the system


def generate_subid(digits=5):
    '''assumes a flat (file system) database, organized by experiment id, and
       subject id, with data (json) organized by subject identifier
    ''' 
    folder_id = 0
    folders = glob('%s/%s/*' %(EXPFACTORY_DATA, EXPFACTORY_SUBID))
    folders.sort()
    if len(folders) > 0:
        folder_id = int(folders[-1]).zfill(digits)
    return "%s/%s" % (EXPFACTORY_SUBID, folder_id)
    

def save_data(session, exp_id, fields):
    '''save data will obtain the current subid from the session, and save it
       depending on the database type. Currently we just support flat files'''

    subid = session.get('subid', None) 

    # We only attempt save if there is a subject id, set at start
    data_file = None
    if subid is not None:
        if EXPFACTORY_DATA is not None:

            # Data base for experiment study id, /scif/data/expfactory
            if not os.path.exists(EXPFACTORY_DATA):
                os.mkdir(EXPFACTORY_DATA)

            # Subject specific folder
            data_base = "%s/%s" %(EXPFACTORY_DATA, subid)
            if not os.path.exists(data_base):
                os.mkdir(data_base)

            data_file = "%s/%s-results.json" %(data_base, exp_id)
            if os.path.exists(data_file):
                bot.warning('%s exists, and is being overwritten.' %data_file)
            write_json(fields, data_file)

    return data_file

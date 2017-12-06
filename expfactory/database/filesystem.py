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
from expfactory.utils import (
    write_json,
    mkdir_p
)
from expfactory.defaults import (
    EXPFACTORY_SUBID,
    EXPFACTORY_DATA
)
from glob import glob
import uuid
import os
import sys


# DEFAULT FLAT #################################################################
# Default "database" is flat files written to the system
################################################################################
# This is an Expfactory Flask Server database plugin. It implements common 
# functions (generate_subid, save_data, init_db) that should prepare a 
# database and perform actions to save data to it. The functions are added
# to the main application upon initialization of the server.


def generate_subid(self, token=None, digits=5):
    '''assumes a flat (file system) database, organized by experiment id, and
       subject id, with data (json) organized by subject identifier
    ''' 

    # Not headless auto-increments
    if not token:
        folder_id = 0
        folders = glob('%s/*' %(self.database))
        folders.sort()
        if len(folders) > 0:
            folder_id = int(os.path.basename(folders[-1])) + 1
        folder_id = str(folder_id).zfill(digits)
        return "%s/%s" % (self.study_id, folder_id)

    # Headless doesn't use any folder_id, just generated token folder
    return "%s/%s" % (self.study_id, token)


def validate_token(self, token):
    '''retrieve a subject based on a token. Valid means we return a participant
       invalid means we return None
    '''
    subid = self.generate_subid(token=token)
    data_base = "%s/%s" %(self.data_base, subid)
    if not os.path.exists(data_base):
        subid = None
    return subid


def generate_user(self, subid=None, digits=5):
    '''generate a new user on the filesystem, still session based so we
       create a new identifier. This function is called from the users new 
       entrypoint, and it assumes we want a user generated with a token.
       since we don't have a database proper, we write the folder name to 
       the filesystem
    '''
    # Only generate token if subid being created
    if subid is None:
        token = str(uuid.uuid4())
        subid = self.generate_subid(token=token)

    if os.path.exists(self.data_base):    # /scif/data
        data_base = "%s/%s" %(self.data_base, subid)
        # expfactory/00001
        if not os.path.exists(data_base):
            mkdir_p(data_base)

    return data_base



def save_data(self, session, exp_id, content):
    '''save data will obtain the current subid from the session, and save it
       depending on the database type. Currently we just support flat files'''

    subid = session.get('subid')

    # We only attempt save if there is a subject id, set at start
    data_file = None
    if subid is not None:

        data_base = "%s/%s" %(self.data_base, subid)

        # If not running in headless, ensure path exists
        if not self.headless and not os.path.exists(data_base):
            mkdir_p(data_base)

        # If headless with token pre-generated OR not headless
        if self.headless and os.path.exists(data_base) or not self.headless:
            data_file = "%s/%s-results.json" %(data_base, exp_id)
            if os.path.exists(data_file):
                bot.warning('%s exists, and is being overwritten.' %data_file)
            write_json(content, data_file)

    return data_file


def init_db(self):
    '''init_db for the filesystem ensures that the base folder (named 
       according to the studyid) exists.
    '''
    self.session = None

    if not os.path.exists(self.data_base):
        mkdir_p(self.data_base)

    self.database = "%s/%s" %(self.data_base, self.study_id)
    if not os.path.exists(self.database):
        mkdir_p(self.database)

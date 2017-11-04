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

#from sqlalchemy import create_engine
#from sqlalchemy.orm import (
#    scoped_session, 
#    sessionmaker
#)

#from sqlalchemy.ext.declarative import declarative_base
from expfactory.logger import bot
from expfactory.utils import write_json
from expfactory.defaults import EXPFACTORY_SUBID, EXPFACTORY_DATABASE
from glob import glob
import os
import sys


def generate_subid(digits=5):
    '''find the most recent data path for saving data. If not writable, then
       return None (and we assume the user is not logged in / testing)
    '''
    if EXPFACTORY_DATABASE == '/scif/data':
        return _generate_subid_flat(digits)
 

def _generate_subid_flat(digits):
    '''assumes a flat (file system) database, organized by experiment id, and
       subject id, with data (json) organized by subject identifier
    ''' 
    folder_id = 0
    folders = glob('%s/%s/*' %(EXPFACTORY_DATABASE, EXPFACTORY_SUBID))
    folders.sort()
    if len(folders) > 0:
        folder_id = int(folders[-1])
    return "%s/%s" % (EXPFACTORY_SUBID, folder_id)
    

# DEFAULT FLAT #################################################################
# Default "database" is flat files written to the system

def save_data(session, exp_id, fields):
    '''save data will obtain the current subid from the session, and save it
       depending on the database type. Currently we just support flat files'''

    subid = session.get('expfactory_subid', None) 
    
    # We only attempt save if there is a subject id, set at start
    data_file = None
    if subid is not None:
        if EXPFACTORY_DATABASE == '/scif/data':
            data_base = "%s/%s" %(EXPFACTORY_DATABASE, subid)
            data_file = "%s/%s-results.json" %(data_base, exp_id)
            write_json(fields, data_file)

    return data_file

#engine = create_engine('sqlite:///%s.db' %(subid), convert_unicode=True)
#db_session = scoped_session(sessionmaker(autocommit=False,
#                                         autoflush=False,
#                                         bind=engine))
#Base = declarative_base()
#Base.query = db_session.query_property()

#def init_db():
    # import all modules here that might define models so that
    # they will be registered properly on the metadata.  Otherwise
    # you will have to import them first before calling init_db()
#    import expfactory.models
#    Base.metadata.create_all(bind=engine)

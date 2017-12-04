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

from sqlalchemy import create_engine
from sqlalchemy.orm import (
    scoped_session, 
    sessionmaker
)

from sqlalchemy.ext.declarative import declarative_base
from expfactory.logger import bot
from expfactory.utils import write_json
from expfactory.defaults import (
    EXPFACTORY_SUBID, 
    EXPFACTORY_DATA
)
from glob import glob
import os
import json
import sys


# SQLITE3 FILE #################################################################
#
# This is an Expfactory Flask Server database plugin. It implements common 
# functions (generate_subid, save_data, init_db) that should prepare a 
# database and perform actions to save data to it. The functions are added
# to the main application upon initialization of the server.
#
################################################################################

def save_data(self,session, exp_id, content):
    '''save data will obtain the current subid from the session, and save it
       depending on the database type.'''
    from expfactory.database.models import (
        Participant,
        Result
    )
    subid = session.get('subid') 
    bot.info('Saving data for subid %s' % subid)    

    # We only attempt save if there is a subject id, set at start
    if subid is not None:
        p = Participant.query.filter(Participant.id == subid).first() # better query here

        # Preference is to save data under 'data', otherwise do all of it
        if "data" in content:
            content = content['data']

        if isinstance(content,dict):
            content = json.dumps(content)

        result = Result(data=content,
                        exp_id=exp_id,
                        participant_id=p.id) # check if changes from str/int
        self.session.add(result)
        p.results.append(result)
        self.session.commit()

        bot.info("Participant: %s" %p)
        bot.info("Result: %s" %result)


Base = declarative_base()

def init_db(self):
    '''initialize the database, with the default database path or custom of
       the format sqlite:////scif/data/expfactory.db

    '''

    # Database Setup, use default if uri not provided
    if self.database == 'sqlite':
        db_path = os.path.join(EXPFACTORY_DATA, '%s.db' % EXPFACTORY_SUBID)
        self.database = 'sqlite:///%s' % db_path

    bot.info("Database located at %s" % self.database)
    self.engine = create_engine(self.database, convert_unicode=True)
    self.session = scoped_session(sessionmaker(autocommit=False,
                                               autoflush=False,
                                               bind=self.engine))
    
    Base.query = self.session.query_property()

    # import all modules here that might define models so that
    # they will be registered properly on the metadata.  Otherwise
    # you will have to import them first before calling init_db()
    import expfactory.database.models
    Base.metadata.create_all(bind=self.engine)
    self.Base = Base

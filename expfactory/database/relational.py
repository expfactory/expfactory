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
import uuid
import pickle
import json
import sys


# RELATIONAL ###################################################################
#
# This is an Expfactory Flask Server database plugin. It implements common 
# functions (generate_subid, save_data, init_db) that should prepare a 
# database and perform actions to save data to it. The functions are added
# to the main application upon initialization of the server. This relational
# module has support for sqlite3, mysql, and postgres
#
################################################################################

def generate_subid(self, token=None, return_user=False):
    '''generate a new user in the database, still session based so we
       create a new identifier.
    '''    
    from expfactory.database.models import Participant
    if not token:
        p = Participant()
    else:
        p = Participant(token=token)
    self.session.add(p)
    self.session.commit()
    if return_user is True:
        return p
    return p.id


def print_user(self, user):
    '''print a relational database user
    ''' 
    status = "active"
    token = user.token

    if token in ['finished', 'revoked']:
        status = token

    if token is None:
        token = ''
  
    subid = "%s\t%s[%s]" %(user.id, token, status)
    print(subid)
    return subid


def list_users(self, user=None):
    '''list users, each having a model in the database. A headless experiment
       will use protected tokens, and interactive will be based on auto-
       incremented ids.
    ''' 
    from expfactory.database.models import Participant
    participants = Participant.query.all()
    users = []
    for user in participants:
        users.append(self.print_user(user))
    return users


# Actions ######################################################################

def generate_user(self):
    '''generate a new user in the database, still session based so we
       create a new identifier. This function is called from the users new 
       entrypoint, and it assumes we want a user generated with a token.
    '''
    token = str(uuid.uuid4())
    return self.generate_subid(token=token, return_user=True)


def finish_user(self, subid):
    '''finish user will remove a user's token, making the user entry not
       accesible if running in headless model'''        

    p = self.revoke_token(subid)
    p.token = "finished"
    self.session.commit()
    return p


def restart_user(self, subid):
    '''restart a user, which means revoking and issuing a new token.'''
    p = self.revoke_token(subid)
    p = self.refresh_token(subid)
    return p


# Tokens #######################################################################


def validate_token(self, token):
    '''retrieve a subject based on a token. Valid means we return a participant
       invalid means we return None
    '''
    from expfactory.database.models import Participant
    p = Participant.query.filter(Participant.token == token).first()
    if p is not None:
        if p.token.endswith(('finished','revoked')):
            p = None
        else:
            p = p.id
    return p


def revoke_token(self, subid):
    '''revoke a token by removing it. Is done at finish, and also available
    as a command line option'''
    from expfactory.database.models import Participant
    p = Participant.query.filter(Participant.id == subid).first()
    if p is not None:
        p.token = 'revoked'
    self.session.commit()
    return p


def refresh_token(self, subid):
    '''refresh or generate a new token for a user'''
    from expfactory.database.models import Participant
    p = Participant.query.filter(Participant.id == subid).first()
    if p is not None:
        p.token = str(uuid.uuid4())
    self.session.commit()
    return p


def save_data(self,session, exp_id, content):
    '''save data will obtain the current subid from the session, and save it
       depending on the database type. Currently we just support flat files'''
    from expfactory.database.models import (
        Participant,
        Result
    )
    subid = session.get('subid')
    token = session.get('token') 

    self.logger.info('Saving data for subid %s' % subid)    

    # We only attempt save if there is a subject id, set at start
    if subid is not None:
        p = Participant.query.filter(Participant.id == subid).first() # better query here

        # Does 
        if self.headless and p.token != token:
            self.logger.warning('%s attempting to use mismatched token [%s] skipping save' %(p.id, token))
        elif self.headless and p.token.endswith(('finished','revoked')):
            self.logger.warning('%s attempting to use expired token [%s] skipping save' %(p.id, token))
        else:

            # Preference is to save data under 'data', otherwise do all of it
            if "data" in content:
                content = content['data']

            result = Result(data=content,
                            exp_id=exp_id,
                            participant_id=p.id) # check if changes from str/int

            # Create and save the result
            self.session.add(result)
            p.results.append(result)
            self.session.commit()

            self.logger.info("Save [participant] %s [result] %s" %(p, result))


Base = declarative_base()
    

def init_db(self):
    '''initialize the database, with the default database path or custom with
       a format corresponding to the database type:

       Examples:

       sqlite:////scif/data/expfactory.db
    '''

    # The user can provide a custom string
    if self.database is None:
        self.logger.error("You must provide a database url, exiting.")
        sys.exit(1)

    self.engine = create_engine(self.database, convert_unicode=True)
    self.session = scoped_session(sessionmaker(autocommit=False,
                                               autoflush=False,
                                               bind=self.engine))

    # Database Setup
    Base.query = self.session.query_property()

    # import all modules here that might define models so that
    # they will be registered properly on the metadata.  Otherwise
    # you will have to import them first before calling init_db()
    import expfactory.database.models
    self.Base = Base
    self.Base.metadata.create_all(bind=self.engine)

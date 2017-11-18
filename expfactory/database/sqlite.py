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
import sys

# Primary (Shared) functions

def generate_subid(digits=5):
    '''generate a new user in the database, still session based so we
       create a new identifier.

    This might be helpful
            user = User(name="Joe")
            session = self.sessionmaker()
            session.save(user)
            session.flush()
            print 'user_id', user.user_id
            session.commit()
            session.close()
    '''    
    from expfactory.database.models import Participant
    p = Participant()
    db_session.add(p)
    db_session.commit()
    print('session:')
    print(p)
    print(p.id)
    return p.id



def save_data(session, exp_id, content):
    '''save data will obtain the current subid from the session, and save it
       depending on the database type. Currently we just support flat files'''
    from expfactory.database.models import (
        Participant,
        Result
    )
    subid = session.get('expfactory_subid', None) 
    bot.info('Saving data for subid %s' % subid)    

    # We only attempt save if there is a subject id, set at start
    if subid is not None:
        p = Participant.query.filter(Participant.id == subid).first() # better query here
        result = Result(data=content, # might need to json.dumps
                        exp_id=exp_id,
                        participant_id=p.id) # check if changes from str/int
        db_session.add(result)
        p.results.append(result)
        db_session.commit()

        bot.info("Participant: %s" %p)
        bot.info("Result: %s" %result)


# Database Setup
db_path = os.path.join(EXPFACTORY_DATA, '%s.db' % EXPFACTORY_SUBID)
bot.info("Database located at %s" % db_path)
engine = create_engine('sqlite:///%s' % db_path, convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

def init_db():
    # import all modules here that might define models so that
    # they will be registered properly on the metadata.  Otherwise
    # you will have to import them first before calling init_db()
    import expfactory.database.models
    Base.metadata.create_all(bind=engine)
    return engine.url # populates app.database

'''
models.py: datanases for the expfactory package

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
from sqlalchemy import (
    Column, 
    DateTime,
    Integer, 
    String, 
    Text,
    ForeignKey,
    func
)
from sqlalchemy.orm import relationship, backref
from uuid import uuid4
from expfactory.database import Base


class Participant(Base):
    '''A participant in a local assessment. id must be unique. If a token is
       revoked or finished, it will end with `_revoked` or `_finished`. A
       user generated without a token will have value of None
    '''
    __tablename__ = 'participant'
    id = Column(Integer, primary_key=True)
    name = Column(String(150))
    token = Column(String(50))
    results = relationship('Result', lazy='select',
                           backref=backref('participant', lazy='joined'))
    def __init__(self, name=None, token=None):
        self.name = name
        self.token = token

    def __repr__(self):
        return '<Participant %r>' % (self.name)

    def url(self):
        '''return the participant url'''
        

class Result(Base):
    '''a result is an experiment name, json dump, and datetime'''
    __tablename__ = 'result'
    id = Column(Integer, primary_key=True)
    date = Column(DateTime, default=func.now())
    data = Column(Text, nullable=False)
    exp_id = Column(String(250), nullable=False)
    participant_id = Column(Integer, 
                            ForeignKey('participant.id'),
                            nullable=False)

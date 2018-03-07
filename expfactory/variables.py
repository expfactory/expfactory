'''

Copyright (c) 2018, Vanessa Sochat
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

import filecmp
from expfactory.utils import read_file
from expfactory.defaults import (
    EXPFACTORY_RUNTIME_DELIM,
    EXPFACTORY_RUNTIME_VARS
)
from expfactory.logger import bot
import json
import re
import os


def get_runtime_vars(varset, experiment, token):
    '''get_runtime_vars will return the urlparsed string of one or more runtime
       variables. If None are present, None is returned.
  
       Parameters
       ==========
       varset: the variable set, a dictionary lookup with exp_id, token, vars
       experiment: the exp_id to look up
       token: the participant id (or token) that must be defined.
 
       Returns
       =======
       url: the variable portion of the url to be passed to experiment, e.g,
            '?words=at the thing&color=red&globalname=globalvalue'

    '''
    url = ''
    if experiment in varset:

        variables = dict()

        # Participant set variables

        if token in varset[experiment]:
            for k,v in varset[experiment][token].items():
                variables[k] = v

        # Global set variables
        if "*" in varset[experiment]:
            for k,v in varset[experiment]['*'].items():

                # Only add the variable if not already defined
                if k not in variables:
                    variables[k] = v

        # Join together, the first ? is added by calling function
        varlist = ["%s=%s" %(k,v) for k,v in variables.items()]
        url = '&'.join(varlist)

    bot.debug('Parsed url: %s' %url)
    return url


def generate_runtime_vars(variable_file=None, sep=','):
    '''generate a lookup data structure from a 
       delimited file. We typically obtain the file name and delimiter from
       the environment by way of EXPFACTORY_RUNTIME_VARS, and
       EXPFACTORY_RUNTIME_DELIM, respectively, but the user can also parse
       from a custom variable file by way of specifying it to the function
       (preference is given here). The file should be csv, with the
       only required first header field as "token" and second as "exp_id" to
       distinguish the participant ID and experiment id. The subsequent
       columns should correspond to experiment variable names. No special parsing
       of either is done. 

       Parameters
       ==========
       variable_file: full path to the tabular file with token, exp_id, etc.
       sep: the default delimiter to use, if not set in enironment.

       Returns
       =======
       varset: a dictionary lookup by exp_id and then participant ID.

       { 'test-parse-url': {
                             '123': {
                                      'color': 'red',
                                      'globalname': 'globalvalue',
                                      'words': 'at the thing'
                                    },

                             '456': {'color': 'blue',
                                     'globalname': 'globalvalue',
                                     'words': 'omg tacos'}
                              }
       }

    '''

    # First preference goes to runtime, then environment, then unset

    if variable_file is None:    
        if EXPFACTORY_RUNTIME_VARS is not None:
            variable_file = EXPFACTORY_RUNTIME_VARS

    if variable_file is not None:
        if not os.path.exists(variable_file):
            bot.warning('%s is set, but not found' %variable_file)
            return variable_file

    # If still None, no file
    if variable_file is None:
        return variable_file

    # If we get here, we have a variable file that exists
    delim = sep
    if EXPFACTORY_RUNTIME_DELIM is not None:
        delim = EXPFACTORY_RUNTIME_DELIM
    bot.debug('Delim for variables file set to %s' %sep)

    # Read in the file, generate config

    varset = dict()
    rows = _read_runtime_vars(variable_file)
    
    if len(rows) > 0:

        # When we get here, we are sure to have 
        # 'exp_id', 'var_name', 'var_value', 'token'

        for row in rows:

            exp_id = row[0].lower()   # exp-id must be lowercase
            var_name = row[1]
            var_value = row[2]
            token = row[3]

            # Level 1: Experiment ID
            if exp_id not in varset:
                varset[exp_id] = {}

            # Level 2: Participant ID
            if token not in varset[exp_id]:
                varset[exp_id][token] = {}

            # If found global setting, courtesy debug message
            if token == "*":
                bot.debug('Found global variable %s' %var_name)

            # Level 3: is the variable, issue warning if already defined
            if var_name in varset[exp_id][token]:
                bot.warning('%s defined twice %s:%s' %(var_name, exp_id, token))
            varset[exp_id][token][var_name] = var_value


    return varset


def _read_runtime_vars(variable_file, sep=','):
    '''read the entire runtime variable file, and return a list of lists,
       each corresponding to a row. We also check the header, and exit
       if anything is missing or malformed.

       Parameters
       ==========

       variable_file: full path to the tabular file with token, exp_id, etc.
       sep: the default delimiter to use, if not set in enironment.

       Returns
       =======

       valid_rows: a list of lists, each a valid row

           [['test-parse-url', 'globalname', 'globalvalue', '*'],
            ['test-parse-url', 'color', 'red', '123'], 
            ['test-parse-url', 'color', 'blue', '456'],
            ['test-parse-url', 'words', 'at the thing', '123'],
            ['test-parse-url', 'words', 'omg tacos', '456']]

    '''

    rows = [x for x in read_file(variable_file).split('\n') if x.strip()]
    valid_rows = []

    if len(rows) > 0:

        # Validate header and rows, exit if not valid

        header = rows.pop(0).split(sep)
        validate_header(header)
        for row in rows:
            row = _validate_row(row, sep=sep, required_length=4)

            # If the row is returned, it is valid

            if row:
                valid_rows.append(row)

    return valid_rows


def _validate_row(row, sep=',', required_length=None):
    '''validate_row will ensure that a row has the proper length, and is
       not empty and cleaned of extra spaces.
 
       Parameters
       ==========
       row: a single row, not yet parsed.

       Returns a valid row, or None if not valid

    '''
    if not isinstance(row, list):
        row = _parse_row(row, sep)

    if required_length:
        length = len(row)
        if length != required_length:
            bot.warning('Row should have length %s (not %s)' %(required_length,
                                                               length))
            bot.warning(row) 
            row = None

    return row


def _parse_row(row, sep=','):
    '''parse row is a helper function to simply clean up a string, and parse
       into a row based on a delimiter. If a required length is provided,
       we check for this too.

    '''
    parsed = row.split(sep)
    parsed = [x for x in parsed if x.strip()]
    return parsed


def validate_header(header, required_fields=None):
    '''validate_header ensures that the first row contains the exp_id,
       var_name, var_value, and token. Capitalization isn't important, but
       ordering is. This criteria is very strict, but it's reasonable
       to require.
 
       Parameters
       ==========
       header: the header row, as a list
       required_fields: a list of required fields. We derive the required
                        length from this list.

       Does not return, instead exits if malformed. Runs silently if OK.

    '''
    if required_fields is None:
        required_fields = ['exp_id', 'var_name', 'var_value', 'token']

    # The required length of the header based on required fields

    length = len(required_fields)

    # This is very strict, but no reason not to be

    header = _validate_row(header, required_length=length) 
    header = [x.lower() for x in header]

    for idx in range(length):
        field = header[idx].lower().strip()
        if required_fields[idx] != field:
            bot.error('Malformed header field %s, exiting.' %field)
            sys.exit(1)

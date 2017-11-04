'''
utils.py: part of expfactory package

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

import errno
import collections
from expfactory.logman import bot
import shutil
import json
import sys
import os
import re

################################################################################
# io utils
################################################################################

def get_installdir():
    return os.path.dirname(os.path.abspath(__file__))


def find_subdirectories(basepath):
    '''
    Return directories (and sub) starting from a base
    '''
    directories = []
    for root, dirnames, filenames in os.walk(basepath):
        new_directories = [d for d in dirnames if d not in directories]
        directories = directories + new_directories
    return directories

    
def find_directories(root,fullpath=True):
    '''
    Return directories at one level specified by user
    (not recursive)
    '''
    directories = []
    for item in os.listdir(root):
        # Don't include hidden directories
        if not re.match("^[.]",item):
            if os.path.isdir(os.path.join(root, item)):
                if fullpath:
                    directories.append(os.path.abspath(os.path.join(root, item)))
                else:
                    directories.append(item)
    return directories

 
def copy_directory(src, dest):
    '''
    Copy an entire directory recursively
    '''
    try:
        shutil.copytree(src, dest)
    except OSError as e:
        # If the error was caused because the source wasn't a directory
        if e.errno == errno.ENOTDIR:
            shutil.copy(src, dest)
        else:
            bot.error('Directory not copied. Error: %s' % e)
            sys.exit(1)


def get_template(template_file):
    '''
    get_template: read in and return a template file
    '''
    filey = open(template_file,"rb")
    template = "".join(filey.readlines())
    filey.close()
    return template


def sub_template(template,template_tag,substitution):
    '''
    make a substitution for a template_tag in a template
    '''
    template = template.replace(template_tag,substitution)
    return template

def save_template(output_file,html_snippet):
    filey = open(output_file,"w")
    filey.writelines(html_snippet)
    filey.close()


def read_json(filename,mode='r'):
    with open(filename,mode) as filey:
        data = json.load(filey)
    return data


def write_json(json_obj,filename,mode='w'):
    with open(filename,mode) as filey:
        filey.write(json.dumps(json_obj, sort_keys=True,indent=4, separators=(',', ': ')))
    return filename


def get_post_fields(request):
    '''parse through a request, and return fields from post in a dictionary
    '''
    fields = dict()
    for field,value in request.form.items():
        fields[field] = value
    return fields


def clone(url, tmpdir=None):
    '''clone a repository from Github'''
    if tmpdir is None:
        tmpdir = tempfile.mkdtemp()
    name = os.path.basename(url).replace('.git', '')
    dest = '%s/%s' %(tmpdir,name)
    return_code = os.system('git clone %s %s' %(url,dest))
    if return_code == 0:
        return dest
    bot.error('Error cloning repo.')
    sys.exit(error_code)


################################################################################
# environment / options
################################################################################

def convert2boolean(arg):
    '''convert2boolean is used for environmental variables
    that must be returned as boolean'''
    if not isinstance(arg, bool):
        return arg.lower() in ("yes", "true", "t", "1", "y")
    return arg


def getenv(variable_key, default=None, required=False, silent=True):
    '''getenv will attempt to get an environment variable. If the variable
    is not found, None is returned.
    :param variable_key: the variable name
    :param required: exit with error if not found
    :param silent: Do not print debugging information for variable
    '''
    variable = os.environ.get(variable_key, default)
    if variable is None and required:
        bot.error("Cannot find environment variable %s, exiting." %variable_key)
        sys.exit(1)

    if not silent:
        if variable is not None:
            bot.verbose2("%s found as %s" %(variable_key,variable))
        else:
            bot.verbose2("%s not defined (None)" %variable_key)

    return variable

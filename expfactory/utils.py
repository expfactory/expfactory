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
from subprocess import (
    Popen,
    PIPE,
    STDOUT
)
from expfactory.logger import bot
import shutil
import json
import tempfile
import sys
import os
import re

################################################################################
# io utils
################################################################################

def get_installdir():
    return os.path.dirname(os.path.abspath(__file__))

def get_templatedir():
    base = get_installdir()
    return "%s/templates" %(base)

def get_viewsdir(base=None):
    '''views might be written to a secondary expfactory install, which can
       be specified with base'''
    if base is None:
        base = get_installdir()
    return "%s/views" %(base)

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

 
def copy_directory(src, dest, force=False):
    ''' Copy an entire directory recursively
    '''
    if os.path.exists(dest) and force is True:
        shutil.rmtree(dest)

    try:
        shutil.copytree(src, dest)
    except OSError as e:
        # If the error was caused because the source wasn't a directory
        if e.errno == errno.ENOTDIR:
            shutil.copy(src, dest)
        else:
            bot.error('Directory not copied. Error: %s' % e)
            sys.exit(1)


def mkdir_p(path):
    '''mkdir_p attempts to get the same functionality as mkdir -p
    :param path: the path to create.
    '''
    try:
        os.makedirs(path)
    except OSError as e:
        if e.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            bot.error("Error creating path %s, exiting." % path)
            sys.exit(1)


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
    sys.exit(return_code)


def run_command(cmd):
    '''run_command uses subprocess to send a command to the terminal.
    :param cmd: the command to send, should be a list for subprocess
    '''
    output = Popen(cmd,stderr=STDOUT,stdout=PIPE)
    t = output.communicate()[0],output.returncode
    output = {'message':t[0],
              'return_code':t[1]}

    return output



################################################################################
# templates
################################################################################

def get_template(name, base=None):
    '''read in and return a template file
    '''
    # If the file doesn't exist, assume relative to base
    template_file = name
    if not os.path.exists(template_file):
        if base is None:
            base = get_templatedir()
        template_file = "%s/%s" %(base, name)

    # Then try again, if it still doesn't exist, bad name
    if os.path.exists(template_file):
        with open(template_file,"r") as filey:
            template = "".join(filey.readlines())
        return template
    bot.error("%s does not exist." %template_file)


def sub_template(template,template_tag,substitution):
    '''make a substitution for a template_tag in a template
    '''
    template = template.replace(template_tag,substitution)
    return template

def save_template(output_file, snippet, mode="w", base=None):
    if base is None:
        base = get_templatedir()
    with open(output_file, mode) as filey:
        filey.writelines(snippet)
    return output_file
    

################################################################################
# JSON
################################################################################


def read_json(filename,mode='r'):
    with open(filename,mode) as filey:
        data = json.load(filey)
    return data


def write_json(json_obj,filename,mode='w'):
    with open(filename,mode) as filey:
        filey.write(json.dumps(json_obj, sort_keys=True,indent=4, separators=(',', ': ')))
    return filename

def read_file(filename,mode='r'):
    with open(filename,mode) as filey:
        data = filey.read()
    return data


def write_file(filename,content,mode='w'):
    with open(filename,mode) as filey:
        filey.writelines(content)
    return filename

def get_post_fields(request):
    '''parse through a request, and return fields from post in a dictionary
    '''
    fields = dict()
    for field,value in request.form.items():
        fields[field] = value
    return fields



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

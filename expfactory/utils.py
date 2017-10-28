'''
utils.py: part of expfactory package

Copyright (c) 2016-2017 Vanessa Sochat

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.


'''

import errno
import collections
from expfactory.logman import bot
import shutil
import json
import os
import re

def get_installdir():
    return os.path.dirname(os.path.abspath(__file__))


def convert2boolean(arg):
    '''convert2boolean is used for environmental variables
    that must be returned as boolean'''
    if not isinstance(arg, bool):
        return arg.lower() in ("yes", "true", "t", "1", "y")
    return arg

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
    """
    Copy an entire directory recursively

    """

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
    """
    get_template: read in and return a template file

    """

    filey = open(template_file,"rb")
    template = "".join(filey.readlines())
    filey.close()
    return template

def sub_template(template,template_tag,substitution):
    """
    make a substitution for a template_tag in a template
    """

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


def is_type(var,types=[int,float,list]):
    """
    Check type
    """

    for x in range(len(types)):
        if isinstance(var,types[x]):
            return True
    return False

def clean_fields(mydict):
    """
    Ensure utf-8
    """

    newdict = dict()
    for field,value in mydict.iteritems():
        cleanfield = field.encode("utf-8")
        if isinstance(value,float):
            newdict[cleanfield] = value
        if isinstance(value,int):
            newdict[cleanfield] = value
        if isinstance(value,list):
            newlist = []
            for x in value:
                if not is_type(x):
                    newlist.append(x.encode("utf-8"))
                else:
                    newlist.append(x)
            newdict[cleanfield] = newlist
        else:
            newdict[cleanfield] = value.encode("utf-8")
    return newdict


def getenv(variable_key,required=False,default=None,silent=False):
    '''getenv will attempt to get an environment variable. If the variable
    is not found, None is returned.
    :param variable_key: the variable name
    :param required: exit with error if not found
    :param silent: Do not print debugging information for variable
    '''
    variable = os.environ.get(variable_key, default)
    if variable == None and required:
        bot.error("Cannot find environment variable %s, exiting." %variable_key)
        sys.exit(1)

    if silent:
        bot.verbose2("%s found" %variable_key)
    else:
        if variable is not None:
            bot.verbose2("%s found as %s" %(variable_key,variable))
        else:
            bot.verbose2("%s not defined (None)" %variable_key)

    return variable 

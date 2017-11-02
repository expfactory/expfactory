'''

validators/experiments.py: python functions to validate experiments and library
experiment objects

The MIT License (MIT)

Copyright (c) 2017 Vanessa Sochat, Stanford University

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

import os
import re
import sys
from expfactory.logman import bot
from glob import glob
from .utils import notvalid
import json


class LibraryValidator:

    def __init__(self,quiet=False):
        if quiet is True:
            bot.level = 0

    def __str__(self):
        return "expfactory.validator.LibraryValidator"

    def validate(self, jsonfile):
        bot.test('EXPERIMENT: %s' % os.path.basename(jsonfile))
        if not self._validate_extension(jsonfile):
            return False
        if not self._validate_loading(jsonfile):
            return False
        if not self._validate_content(jsonfile):
            return False
        return True

    def _print_valid(self, result):
        options = {True:'yes', False: 'no'}
        return options[result]

    def _validate_extension(self,jsonfile):
        valid = jsonfile.endswith('.json')
        bot.test("...extension json: %s" %(self._print_valid(valid))) 
        return valid

    def _validate_loading(self,jsonfile):
        with open(jsonfile,'r') as filey:
            content = json.load(filey)
        valid = isinstance(content,dict)
        bot.test("...json loadable: %s" %(self._print_valid(valid)))
        return valid


    def _validate_content(self,jsonfile):

        bot.test("Content:")
        name = os.path.basename(jsonfile)
        with open(jsonfile,'r') as filey:
            content = json.load(filey)

        # Validate name
        if "name" not in content:
            return notvalid('"name" not found in %s' %(name)) 
        bot.test("        Name: %s" % content['name'])

        if not re.match("^[a-z0-9_-]*$", content['name']): 
            return notvalid('''invalid characters in %s, only 
                               lowercase and "-" or "_" allowed.''' %(content['name'])) 
         
        # Validate Github
        if "github" not in content:
            return notvalid('"github" not found in %s' %(name)) 
        if not re.search("(\w+://)(.+@)*([\w\d\.]+)(:[\d]+){0,1}/*(.*)",content['github']):
            return notvalid('%s is not a valid URL.' %(content['github'])) 
        if not isinstance(content["github"],str):
            return notvalid("%s must be a string" %(content['github']))
        bot.test("        Github: %s" % content['github'])

        # Maintainers
        if "maintainer" not in content:
            return notvalid('"maintainer" missing in %s' %(name)) 
        bot.test("        Maintainer: %s" % content['maintainer'])

        return True

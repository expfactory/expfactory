'''

validators/runtime.py: python functions to validate deployments

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
from expfactory.logger import bot
from expfactory.utils import clone, read_file
from .utils import notvalid
import json
import requests
import tempfile
from glob import glob


class RuntimeValidator:

    def __init__(self,quiet=False):
        if quiet is True:
            bot.level = 0

    def __str__(self):
        return "expfactory.RuntimeValidator"

    def validate(self, url):
        ''' takes in a Github repository for validation of preview and 
            runtime (and possibly tests passing?
        '''

        # Preview must provide the live URL of the repository
        if not url.startswith('http') or not 'github' in url:
            bot.error('Test of preview must be given a Github repostitory.')
            return False

        if not self._validate_preview(url):
            return False

        return True

    def _print_valid(self, result):
        options = {True:'yes', False: 'no'}
        return options[result]

    def _validate_preview(self, url):

        bot.test('Experiment url: %s' %url)
        org,repo = url.split('/')[-2:]
        if repo.endswith('.git'):
            repo = repo.replace('.git','')
        github_pages =  "https://%s.github.io/%s" %(org,repo)
        bot.test('Github Pages url: %s' %github_pages)

        response = requests.get(github_pages)

        if response.status_code == 404:
            bot.error('''Preview not found at %s. You must publish a static 
                         preview from the master branch of your repository to
                         add to the library.''' % github_pages)
            return False 

        index = response.text
        tmpdir = tempfile.mkdtemp()
        repo_master = clone(url, tmpdir)
        contenders = glob('%s/*' %repo_master)
        license = False
        found = False

        for test in contenders:
            if os.path.isdir(test):
                continue
            print('...%s' %test)
            if "LICENSE" in os.path.basename(test):
                license = True
            if os.path.basename(test) == "index.html":
                bot.test('Found index file in repository.')
                found = True
                break

        if license is False:
            bot.warning("LICENSE file not found. This will be required for future experiments!")

        self._print_valid(found)
        return found

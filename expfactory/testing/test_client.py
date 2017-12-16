#!/usr/bin/python

'''
Test experiments

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

import unittest
import shutil
from expfactory.utils import *
from expfactory.experiment import *
import tempfile
import json
import os

class TestClient(unittest.TestCase):

    def setUp(self):
        self.pwd = get_installdir()
        self.battery_folder = "%s/testing/data" %self.pwd
        self.experiment = os.path.abspath("%s/testing/data/test_task/" %self.pwd)
        self.tmpdir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.tmpdir)

    def run_command(self,cmd):
        result = run_command(cmd)
        self.assertEqual(result['return_code'],0)
        return str(result['message'])
 
    def test_help(self):
        result = self.run_command(["expfactory","--help"])
        self.assertTrue('{users,list,logs,install,build}' in result)

        result = self.run_command(["expfactory","list","--help"])
        self.assertTrue('expfactory list' in result)

        result = self.run_command(["expfactory","build","--help"])
        self.assertTrue('expfactory build' in result)

        result = self.run_command(["expfactory","install","--help"])
        self.assertTrue('expfactory install' in result)

        result = self.run_command(["expfactory","users","--help"])
        self.assertTrue('expfactory users' in result)

        result = self.run_command(["expfactory","logs","--help"])
        self.assertTrue('expfactory logs' in result)

    def test_list(self):
        result = self.run_command(["expfactory"])

        # We list > 95 experiments
        self.assertTrue(len(result.split('\\n'))>95)
        self.assertTrue('test-task' in result)

    def test_install(self):
        os.chdir(self.tmpdir)
        result = self.run_command(["expfactory",
                                   "install",
                                   "https://www.github.com/expfactory-experiments/test-task"])
        self.assertTrue(os.path.exists('%s/test-task' %self.tmpdir))

if __name__ == '__main__':
    unittest.main()

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
from expfactory.validator import *

import tempfile
import json
import os

class TestExperiment(unittest.TestCase):

    def setUp(self):
        self.pwd = get_installdir()
        self.battery_folder = "%s/testing/data" %self.pwd
        self.experiment = os.path.abspath("%s/testing/data/test-task/" %self.pwd)
        self.bad_experiment = os.path.abspath("%s/testing/data/not_an_experiment/" %self.pwd)
        self.tmpdir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.tmpdir)

    def test_library(self):
        library = get_library(key='name')
        self.assertTrue(len(library)>95)

    def test_load_experiments(self):

        loaded_experiment = load_experiment(self.experiment)  
        self.assertTrue(isinstance(loaded_experiment,dict))

    def test_validate(self):
        loaded_experiment = load_experiment(self.experiment)  
        validator = ExperimentValidator()
        valid = validator.validate(self.experiment)
        not_valid = validator.validate(self.bad_experiment)
        self.assertTrue(valid)
        self.assertTrue(not not_valid)


if __name__ == '__main__':
    unittest.main()

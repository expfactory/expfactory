'''
test_experiments.py: Allow a user to test all experiments in the container. 
                     The experiments are assumed to be installed at /scif/apps

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

import os
import sys
from glob import glob
from expfactory.validator import ExperimentValidator
from unittest import TestCase

class TestExperiment(TestCase):

    def setUp(self):

        self.ExpValidator = ExperimentValidator()
        self.base = "/scif/apps"
        self.experiments = glob("%s/*" %self.base)
        self.contenders = [os.path.basename(x) for x in self.experiments]
        
    def test_experiment(self):
        '''test an experiment, including the markdown file, and repo itself
        '''
        print("...Test: Experiment Validation")

        # First priority - the user gave an experiment folder
        if "config.json" in self.contenders:
            for experiment in self.experiments:
                name = os.path.basename(experiment)
                if name == "config.json":
                    valid = self.ExpValidator.validate(experiment, validate_folder=False) 
                    self.assertTrue(valid)

        # Otherwise, the user gave a folder with subfolders
        else:
            for experiment in self.experiments:
                name = os.path.basename(experiment)
                if os.path.isdir(experiment):
                    print('Found experiment %s' %name)
                    valid = self.ExpValidator.validate(experiment) 
                    self.assertTrue(valid)


if __name__ == '__main__':
    unittest.main()

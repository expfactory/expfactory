'''
test_experiment.py: Allow a user to test a local experiment. This is intended
                    to run from the provided Expfactory container. The experiment
                    is assumed to be mounted at /scif/data

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
        self.config = "/scif/data/config.json"
        
    def test_experiment(self):
        '''test an experiment, including the markdown file, and repo itself
        '''
        if not os.path.exists(self.config):
            print('You must use --bind to bind the folder with config.json to /scif/data in the image.')
            sys.exit(1) 

        print("...Test: Experiment Validation")
        self.assertTrue(self.ExpValidator.validate(self.config,validate_folder=False))


if __name__ == '__main__':
    unittest.main()

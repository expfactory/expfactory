"""

validators/experiments.py: python functions to validate experiments and library
experiment objects

Copyright (c) 2017-2021, Vanessa Sochat
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


"""

import os
import re
import sys
import tempfile
import shutil
from expfactory.validator.utils import notvalid
from expfactory.logger import bot
from expfactory.utils import clone, read_json
from glob import glob
import json


class ExperimentValidator:
    def __init__(self, quiet=False):
        self.tmpdir = tempfile.mkdtemp()
        if quiet is True:
            bot.level = 0

    def __str__(self):
        return "expfactory.ExperimentValidator"

    def _validate_folder(self, folder=None):
        """ validate folder takes a cloned github repo, ensures
            the existence of the config.json, and validates it.
        """
        from expfactory.experiment import load_experiment

        if folder is None:
            folder = os.path.abspath(os.getcwd())

        config = load_experiment(folder, return_path=True)

        if not config:
            return notvalid("%s is not an experiment." % (folder))

        return self._validate_config(folder)

    def validate(self, folder, cleanup=False, validate_folder=True):
        """ validate is the entrypoint to all validation, for
            a folder, config, or url. If a URL is found, it is
            cloned and cleaned up.
           :param validate_folder: ensures the folder name (github repo)
                                   matches.
        """

        # Obtain any repository URL provided
        if folder.startswith("http") or "github" in folder:
            folder = clone(folder, tmpdir=self.tmpdir)

        # Load config.json if provided directly
        elif os.path.basename(folder) == "config.json":
            config = os.path.dirname(folder)
            return self._validate_config(config, validate_folder)

        # Otherwise, validate folder and cleanup
        valid = self._validate_folder(folder)
        if cleanup is True:
            shutil.rmtree(folder)
        return valid

    def _validate_config(self, folder, validate_folder=True):
        """ validate config is the primary validation function that checks
            for presence and format of required fields.

        Parameters
        ==========
        :folder: full path to folder with config.json
        :name: if provided, the folder name to check against exp_id
        """
        config = "%s/config.json" % folder
        name = os.path.basename(folder)
        if not os.path.exists(config):
            return notvalid("%s: config.json not found." % (folder))

        # Load the config
        try:
            config = read_json(config)
        except:
            return notvalid("%s: cannot load json, invalid." % (name))

        # Config.json should be single dict
        if isinstance(config, list):
            return notvalid("%s: config.json is a list, not valid." % (name))

        # Check over required fields
        fields = self.get_validation_fields()
        for field, value, ftype in fields:

            bot.verbose("field: %s, required: %s" % (field, value))

            # Field must be in the keys if required
            if field not in config.keys():
                if value == 1:
                    return notvalid(
                        "%s: config.json is missing required field %s" % (name, field)
                    )

            # Field is present, check type
            else:
                if not isinstance(config[field], ftype):
                    return notvalid(
                        "%s:%s invalid type, must be %s." % (name, field, str(ftype))
                    )

            # Expid gets special treatment
            if field == "exp_id" and validate_folder is True:
                if config[field] != name:
                    return notvalid(
                        "%s: exp_id parameter %s does not match folder name."
                        % (name, config[field])
                    )

                # name cannot have special characters, only _ and letters/numbers
                if not re.match("^[a-z0-9_-]*$", config[field]):
                    message = "%s: exp_id parameter %s has invalid characters"
                    message += "only lowercase [a-z],[0-9], -, and _ allowed."
                    return notvalid(message % (name, config[field]))

        return True

    def get_validation_fields(self):
        """get_validation_fields returns a list of tuples (each a field)
           we only require the exp_id to coincide with the folder name, for the sake
           of reproducibility (given that all are served from sample image or Github
           organization). All other fields are optional.
           To specify runtime variables, add to "experiment_variables"

                 0: not required, no warning
                 1: required, not valid
                 2: not required, warning      
                type: indicates the variable type
        """
        return [
            ("name", 1, str),  # required
            ("time", 1, int),
            ("url", 1, str),
            ("description", 1, str),
            ("instructions", 1, str),
            ("exp_id", 1, str),
            ("install", 0, list),  # list of commands to install / build experiment
            ("contributors", 0, list),  # not required
            ("reference", 0, list),
            ("cognitive_atlas_task_id", 0, str),
            ("template", 0, str),
        ]

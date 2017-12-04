'''
experiment.py: part of expfactory package

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

from expfactory.utils import (
    find_directories, 
    read_json
)

from glob import glob
import filecmp
from expfactory.defaults import EXPFACTORY_LIBRARY
from expfactory.logger import bot
import json
import requests
import re
import os


################################################################################
# Experiments
################################################################################


def get_experiments(base, load=False):
    ''' get_experiments will return loaded json for all valid experiments from an experiment folder
    :param base: full path to the base folder with experiments inside
    :param load: if True, returns a list of loaded config.json objects. If False (default) returns the paths to the experiments
    '''
    experiments = find_directories(base)
    valid_experiments = [e for e in experiments if validate(e,cleanup=False)]
    bot.info("Found %s valid experiments" %(len(valid_experiments)))
    if load is True:
        valid_experiments = load_experiments(valid_experiments)

    #TODO at some point in this workflow we would want to grab instructions from help
    # and variables from labels, environment, etc.
    return valid_experiments


def load_experiments(folders):
    '''load_experiments
    a wrapper for load_experiment to read multiple experiments
    :param experiment_folders: a list of experiment folders to load, full paths
    '''
    experiments = []
    if isinstance(folders,str):
        folders = [experiment_folders]
    for folder in folders:
        exp = load_experiment(folder)
        experiments.append(exp)
    return experiments


def load_experiment(folder, return_path=False):
    '''load_experiment:
    reads in the config.json for a folder, returns None if not found.
    :param folder: full path to experiment folder
    :param return_path: if True, don't load the config.json, but return it
    '''
    fullpath = os.path.abspath(folder)
    config = "%s/config.json" %(fullpath)
    if not os.path.exists(config):
        bot.error("config.json could not be found in %s" %(folder))
        config = None
    if return_path is False and config is not None:
        config = read_json(config)
    return config


def get_selection(available, selection, base='/scif/apps'):
    '''we compare the basename (the exp_id) of the selection and available, 
       regardless of parent directories'''

    if isinstance(selection, str):
        selection = selection.split(',')

    available = [os.path.basename(x) for x in available]
    selection = [os.path.basename(x) for x in selection]
    finalset = [x for x in selection if x in available]
    if len(finalset) == 0:
        bot.warning("No user experiments selected, providing all %s" %(len(available)))
        finalset = available
    return ["%s/%s" %(base,x) for x in finalset]


def make_lookup(experiment_list, key='exp_id'):
    '''make_lookup returns dict object to quickly look up query experiment on exp_id
    :param experiment_list: a list of query (dict objects)
    :param key_field: the key in the dictionary to base the lookup key (str)
    :returns lookup: dict (json) with key as "key_field" from query_list 
    '''
    lookup = dict()
    for single_experiment in experiment_list:
        if isinstance(single_experiment, str):
            single_experiment = load_experiment(single_experiment)
        lookup_key = single_experiment[key]
        lookup[lookup_key] = single_experiment
    return lookup


def validate(folder=None, cleanup=False):
    '''validate
    :param folder: full path to experiment folder with config.json. If path begins
                   with https, we assume to be starting from a repository.
    '''
    from expfactory.validator import ExperimentValidator
    cli = ExperimentValidator()
    return cli.validate(folder, cleanup=cleanup)




################################################################################
# Library
################################################################################

def get_library(lookup=True, key='exp_id'):
    ''' return the raw library, without parsing'''
    library = None
    response = requests.get(EXPFACTORY_LIBRARY)
    if response.status_code == 200:
        library = response.json()
        if lookup is True:
            return make_lookup(library,key=key)
    return library


'''
experiment.py: part of expfactory package
Functions to work with javascript experiments

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

from expfactory.utils import find_directories, read_json
from glob import glob
import filecmp
from expfactory.logman import bot
import json
import re
import os


def get_experiments(base, load=False, warning=True):
    ''' get_experiments will return loaded json for all valid experiments from an experiment folder
    :param base: full path to the base folder with experiments inside
    :param load: if True, returns a list of loaded config.json objects. If False (default) returns the paths to the experiments
    '''
    experiments = find_directories(base)
    valid_experiments = [e for e in experiments if validate(e,warning)]
    bot.info("Found %s valid experiments" %(len(valid_experiments)))
    if load is True:
        valid_experiments = load_experiments(valid_experiments)
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


def load_experiment(folder):
    '''load_experiment:
    reads in the config.json for an
    :param folder: full path to experiment folder
    '''
    fullpath = os.path.abspath(folder)
    config = "%s/config.json" %(fullpath)
    if not os.path.exists(config):
        return notvalid("config.json could not be found in %s" %(folder))
    return read_json(config)
    

def notvalid(reason):
    bot.error(reason)
    return False

def dowarning(reason):
    bot.warning(reason)


def get_selection(available, selection, base='/scif/apps'):
    '''we compare the basename (the exp_id) of the selection and available, 
       regardless of parent directories'''

    if isinstance(selection,str):
        selection = selection.split(' ')

    available = [os.path.basename(x) for x in available]
    selection = [os.path.basename(x) for x in selection]
    return ["%s/%s" %(base,x) for x in selection if x in available]


def get_validation_fields():
    '''get_validation_fields returns a list of tuples (each a field)

    we only require the exp_id to coincide with the folder name, for the sake
    of reproducibility (given that all are served from sample image or Github
    organization). All other fields are optional.

    To specify runtime variables, add to "experiment_variables"

                 0: not required, no warning
                 1: required, not valid
                 2: not required, warning      
                type: indicates the variable type
    '''

    return [("run",0,list),
            ("name",0,str), 
            ("contributors",0,str),
            ("time",0,int), 
            ("notes",0,str),
            ("reference",0,str), 
            ("exp_id",1,str),
            ("cognitive_atlas_task_id",0,str),
            ("experiment_variables",0,list),
            ("publish",0,str),
            ("deployment_variables",0,str),
            ("template",0,str)]



def validate(folder=None, warning=True):
    '''validate
    :param experiment_folder: full path to experiment folder with config.json
    :param warning: issue a warning for empty fields with level 2 (warning)
    '''

    if folder is None:
        folder=os.path.abspath(os.getcwd())

    try:
        meta = load_experiment(folder)
        if meta is False:
            return notvalid("%s is not an experiment." %(folder))
        experiment_name = os.path.basename(folder)

    except:
        return notvalid("%s: config.json is not loadable." %(folder))

    if isinstance(meta, list):
        return notvalid("%s: config.json is a list, not valid." %(folder))

    fields = get_validation_fields()

    for field,value,ftype in fields:

        # Field must be in the keys if required
        if field not in meta.keys():
            if value == 1:
                return notvalid("%s: config.json is missing required field %s" 
                                %(experiment_name,field))

            elif value == 2 and warning is True:
                dowarning("WARNING: config.json is missing field %s: %s" 
                          %(field,experiment_name))

        # Tag must correspond with folder name
        if field == "exp_id":
            if meta[field] != experiment_name:
                return notvalid("%s: exp_id parameter %s does not match folder name." 
                                %(experiment_name,meta[field]))

            # name cannot have special characters, only _ and letters/numbers
            if not re.match("^[a-z0-9_-]*$", meta[field]): 
                message = "%s: exp_id parameter %s has invalid characters" 
                message += "only lowercase [a-z],[0-9], -, and _ allowed."
                return notvalid(message %(experiment_name,meta[field]))
                
    return True



def make_lookup(experiment_list, key='exp_id'):
    '''make_lookup returns dict object to quickly look up query experiment on exp_id
    :param experiment_list: a list of query (dict objects)
    :param key_field: the key in the dictionary to base the lookup key (str)
    :returns lookup: dict (json) with key as "key_field" from query_list 
    '''
    lookup = dict()
    for single_experiment in experiment_list:
        if isinstance(single_experiment,str):
            single_experiment = load_experiment(single_experiment)
        lookup_key = single_experiment[key]
        lookup[lookup_key] = single_experiment
    return lookup

#!/bin/env python

'''
survey.py: plugin to work with expfactory package to generate survey

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
    write_file,
    get_template,
    sub_template
)
from expfactory.logger import bot
from expfactory.experiment import load_experiment
import argparse
import pandas
import json
import sys
import re
import os


def get_question_types():
   '''get_question_types returns a list of possible question types
   '''
   return ["radio","checkbox","textfield","textarea",
           "numeric","table","instruction"]


# CREATION FUNCTIONS ###########################################################

def create_instruction(text,id_attribute,tag="h2"):
    '''creates a tag of type [tag] with some text inside
    useful for description or instructions.

    Parameters
    ==========

    text: the text to give in the instruction.
    id_attribute: the unique id for the question
    tag: the html tag for the instruction (eg, p or h2)

    '''
    return "<%s>%s</%s><br><br><br><br>" %(tag,text,tag)


def format_options_values(options,values):
    if isinstance(options,str):
        options = [options]
    if isinstance(values,str):
        values = [values]
    return options,values

def get_required_string(required_int):
    required = ""
    if required_int == 1:
        required = "required"
    return required

def parse_meta(text,options=None):
    '''return fields to include in inputs for question
    text and options, for export

    Parameters
    ==========
    text: the text of the question (required)
    options: options to include with the data (optional)

    '''
    text = text.replace('"',"'")
    if options!= None:
        options_joined =  "|".join([x.replace('"',"'") for x in options])
        return 'meta-options="%s" meta-text="%s"' %(options_joined,text)
    return 'meta-text="%s"' %(text)


def add_classes(classes,new_classes):
    '''add_classess adds a string of new classes to current, if defined

    Parameters
    ==========

    classes: string of current classes, must be defined
    new_classes: new classes to add, optional

    '''
    if new_classes != None:
        classes = "%s %s" %(classes,new_classes)
    return classes

def create_radio(text,id_attribute,options,values,classes="",required=0,validate=False):
    '''generate a material lite radio button given a text field 
       and a set of options.

    Parameters
    ==========

    text: The text (content) of the question to ask
    id_attribute: the unique id for the question
    options: a list of text options for the user to select from (not the value of the field)
    values: a list of values for corresponding options
    classes: classes to add to the default, should be a string
    required: is the question required? 0=False,1=True, default 0
    validate: throw an error in the case that number of values != number of option (for testing)

    ''' 
    class_names = "mdl-radio mdl-js-radio mdl-js-ripple-effect"       

    options,values = format_options_values(options,values)
    
    required = get_required_string(required)

    meta = parse_meta(text,options)

    # If going through validation, tell the user the question, etc.
    if validate == True:
        print("Testing question %s with text %s" %(id_attribute,text))

    # If options provided are equal to values, parse the question
    if len(options) == len(values):
        radio_html = '<p id="%s_options">%s</p>' %(id_attribute,text)
        for n in range(len(options)):
            option_id = "%s_%s" %(id_attribute,n)
            radio_html = '%s\n<label class="%s" for="option-%s">\n<input type="radio" id="option-%s" class="mdl-radio__button %s %s" name="%s_options" value="%s" %s>\n<span class="mdl-radio__label">%s</span>\n</label>' %(radio_html,class_names,option_id,option_id,required,classes,id_attribute,values[n],meta,options[n])
        return "%s<br><br><br><br>" %(radio_html)

    # Otherwise, we cannot include it
    else:   
        error_message = "ERROR: %s options provided, and only %s values. Must define one option per value." %(len(options),len(values))
        if validate == True:
            raise ValueError(error_message)
        else:
            print(error_message)

        return ""

def create_checkbox(text,id_attribute,options,classes="",required=0):
    '''generate a material lite checkbox field given a text field, 
       and a set of options.

    Parameters
    ==========

    text: The text (content) of the question to ask
    options: a list of text options for the user to select from
    id_attribute: the unique id for the question
    classes: additional classes to add to the input, should be a string
    required: is the question required? 0=False,1=True, default 0

    '''        
    class_names = "mdl-checkbox mdl-js-checkbox mdl-js-ripple-effect"

    required = get_required_string(required)

    meta = parse_meta(text,options)

    checkbox_html = '<p id="%s_options">%s</p>' %(id_attribute,text)
    for n in range(len(options)):
        option_id = "%s_%s" %(id_attribute,n)
        checkbox_html = '%s\n<label class="%s" for="checkbox-%s">\n<input type="checkbox" id="checkbox-%s" %s class="mdl-checkbox__input %s %s" name="%s_options" value="%s">\n<span class="mdl-checkbox__label">%s</span>\n</label>' %(checkbox_html,class_names,option_id,option_id,meta,classes,required,option_id,options[n],options[n])
    return "%s<br><br><br>" %(checkbox_html)
    
def base_textfield(text,id_attribute,box_text=None):
    '''parse input for a general textfield, returning base html, box_text, id.

    Parameters
    ==========

    text: Any text content to precede the question field (default is None)
    id_attribute: the unique id for the question
    box_text: text content to go inside the box (default is None)

    '''        
    if box_text == None:
        box_text = ""

    textfield_html = ""
    if text != None:
        textfield_html = '<p id="%s">%s</p>' %(id_attribute,text)

    return textfield_html,box_text


def create_textfield(text,id_attribute,box_text=None,classes="",required=0):
    '''create_textfield generates a material lite text field given a text prompt.

    Parameters
    ==========

    text: Any text content to precede the question field (default is None)
    id_attribute: the unique id for the question
    box_text: text content to go inside the box (default is None)
    classes: additional classes to add to the input, should be a string
    required: is the question required? 0=False,1=True, default 0

    '''   
    class_names = "mdl-textfield mdl-js-textfield"

    textfield_html,box_text = base_textfield(text,id_attribute,box_text)
    required = get_required_string(required)
    meta = parse_meta(text)

    return '%s\n<div class="%s">\n<input class="mdl-textfield__input %s %s" name="%s" type="text" id="%s" %s>\n<label class="mdl-textfield__label" for="%s">%s</label>\n</div><br><br><br>' %(textfield_html,class_names,classes,required,id_attribute,id_attribute,meta,id_attribute,box_text)


def create_numeric_textfield(text,id_attribute,box_text=None,classes="",required=0):
    '''create_numeric generates a material lite numeric text field given a text prompt.

    Parameters
    ==========

    text: Any text content to precede the question field (default is None)
    id_attribute: the unique id for the question
    box_text: text content to go inside the box (default is None)
    id_attribute: an id to match to the text field
    classes: classes to add to the input. Must be a string.
    required: is the question required? 0=False,1=True, default 0

    '''   
    class_names = "mdl-textfield mdl-js-textfield"  

    required = get_required_string(required)
    textfield_html,box_text = base_textfield(text,id_attribute,box_text)
    meta = parse_meta(text)

    return '%s\n<div class="%s">\n<input class="mdl-textfield__input %s %s" type="number" id="%s" name="%s" %s>\n<label class="mdl-textfield__label" for="%s">%s</label>\n<span class="mdl-textfield__error">Input is not a number!</span>\n</div><br><br><br>' %(textfield_html,class_names,classes,required,id_attribute,id_attribute,meta,id_attribute,box_text)


def create_select_table(text,id_attribute,df,classes="",required=0):
    '''create_select_table generates a material lite table from a pandas data frame.

    Parameters
    ==========

    df: A pandas data frame, with column names corresponding to columns, and rows
    id_attribute: the unique id for the question
    text: A text prompt to put before the table
    classes: the classes to apply to the input. If none, default will be used.
    required: is the question required? 0=False,1=True, default 0

    '''        
    if isinstance(df,pandas.DataFrame):
    
        
        class_names = "mdl-data-table mdl-js-data-table mdl-data-table--selectable mdl-shadow--2dp %s" %(required)

        required = get_required_string(required)
        table_html = '<p>%s</p>\n<table id="%s" class="%s %s">\n<thead>\n<tr>' %(text,id_attribute,class_names,classes)
        meta = parse_meta(text)

        # Parse column names
        column_names = df.columns.tolist()
        for column_name in columns_names:
            table_html = '%s\n<th class="mdl-data-table__cell--non-numeric">%s</th>' %(table_html,column_name)
        table_html = "%s\n</tr>\n</thead>\n<tbody>" %(table_html)

        # Parse rows
        for row in df.iterrows():
            row_id = row[0]
            table_html = "%s\n<tr>" %(table_html)
            values = row[1].tolist()
            for value in values:
                if isinstance(value,str) or isinstance(value,unicode):
                    table_html = '%s\n<td class="mdl-data-table__cell--non-numeric">%s</td>' %(table_html,str(value))
                else:
                    table_html = '%s\n<td>%s</td>' %(table_html,value)
            table_html = "%s\n</tr>" %(table_html)
        return "%s\n</tbody>\n</table><br><br><br>" %(table_html)
 
    print("ERROR: DataFrame (df) must be a pandas.DataFrame")


def create_textarea(text,id_attribute,box_text=None,classes="",rows=3,required=0):
    '''create_textarea generates a material lite multi line text field with a text prompt.

    Parameters
    ==========

    text: A text prompt to put before the text field
    id_attribute: the unique id for the question
    classes: classes to add to the text field (optional) should be string.
    rows: number of rows to include in text field (default 3)
    required: is the question required? 0=False,1=True, default 0

    '''        
    textfield_html,box_text = base_textfield(text,id_attribute,box_text)
    meta = parse_meta(text)

    class_names = "mdl-textfield mdl-js-textfield"

    return '%s\n<div class="%s"><textarea class="mdl-textfield__input %s %s" type="text" rows="%s" id="%s" name="%s" %s ></textarea>\n<label class="mdl-textfield__label" for="%s">%s</label></div><br><br><br>' %(textfield_html,class_names,classes,required,rows,id_attribute,id_attribute,meta,id_attribute,box_text)


# EXPORT FUNCTIONS ##############################################################################

def export_instruction(text,id_attribute,required=0):
    return {"text":text,"id":id_attribute,"required":required}

def export_radio(text,id_attribute,options,values,required=0):
    '''export_radio returns a json data structure of the question

    Parameters
    ==========

    text: The text (content) of the question to ask
    id_attribute: the unique id for the question
    options: a list of text options for the user to select from (not the value of the field)
    values: a list of values for corresponding options
    required: is the question required? 0=False,1=True, default 0

    ''' 
    options,values = format_options_values(options,values)    
    question_list = {}

    if len(options) == len(values):
        question_list["id"] = "%s_options" %(id_attribute)
        question_list["required"] = required
        question_list["text"] = text
        option_list = []
        for n in range(len(options)):
            option_id = "%s_%s" %(id_attribute,n)
            option_list.append({"id":option_id,"value":values[n],"text":options[n]})
        question_list["options"] = option_list
    return question_list

def export_checkbox(text,id_attribute,options,required=0):
    '''export_checkbox returns json data structure to describe checkbox

    Parameters
    ==========

    text: The text (content) of the question to ask
    options: a list of text options for the user to select from
    id_attribute: the unique id for the question
    required: is the question required? 0=False,1=True, default 0

    '''        
    new_questions = []

    option_list = []
    for n in range(len(options)):
        option_id = "%s_%s" %(id_attribute,n)
        option_list.append({"id":option_id,"text":options[n]})

    for n in range(len(options)):
        option_id = "%s_%s" %(id_attribute,n)
        option_entry = {"id":"%s_options" %(option_id),
                        "required":required,
                        "text":text,
                        "options":option_list,
                        "value":options[n]}
        new_questions.append(option_entry)
    return new_questions


def export_textfield(text,id_attribute,required=0):
    '''create_textfield generates a material lite text field given a text prompt.
    text: Any text content to precede the question field (default is None)
    id_attribute: the unique id for the question
    required: is the question required? 0=False,1=True, default 0
    '''   
    question_list = {}
    question_list["id"] = id_attribute
    question_list["required"] = required
    question_list["text"] = text
    return question_list


# PARSING FUNCTIONS ############################################################################

def parse_validation(required_counts):
    '''parse_validation parses code to validate each step
    page_count: the total number of pages for the survey (called "steps")
    '''
    validation = ""
    current_page = 1
    pages = list(required_counts.keys())
    pages.sort()
    for page_number in pages:
        if current_page == 1:
            validation = "%s if ( state.stepIndex === %s ) {\n" %(validation,page_number)
        else:
            validation = "%s else if ( state.stepIndex === %s ) {\n" %(validation,page_number)
        validation = '%s if (($.unique($(`.page%s.required[type=number],.page%s.required:text`).map(function(){return $(this).attr(`meta-text`)})).map(function() {return $(`[meta-text*="` + this + `"].required[type=number], [meta-text*="` + this + `"].required:text`).filter(function() { return $(this).val();}).length > 0}).get().indexOf(false) != -1) || ($.unique($(`.page%s.required:not([type=number]):not(:text)`).map(function(){return $(this).attr(`meta-text`)})).map(function() {return $(`[meta-text*="` + this + `"].required:checked`).length > 0}).get().indexOf(false) != -1)){\nis_required($(`.page%s.required:not(checked)`));\nreturn false;\n' % (validation, page_number, page_number, page_number, page_number)

	# If we are at the last page, passing validation should enable the submit
        if page_number == pages[-1]:
            validation = '%s } else {\nexpfactory_finished=true;\n' %(validation)
        validation = '%s}}' %(validation)
        current_page+=1
    return validation



def read_survey_file(question_file,delim="\t"):
    ''''read in a survey file, and returns a DataFrame with columns. 
        If there is an error, None is returned, and the error is printed to the screen.

    Parameters
    ==========

    question_file: the survey.tsv (or other) questions file
    delim: the delimiter of the question_file

    '''
    df = pandas.read_csv(question_file,sep=delim)
    required_columns = ["question_type","question_text","page_number","option_text","option_values","required"]
    optional_columns = ["variables"]
    acceptable_types = get_question_types()

    # Parse column names, ensure lower case, check that are valid
    column_names = [x.lower() for x in df.columns.tolist()]
    acceptable_columns = []
    for column_name in column_names:
        if column_name in required_columns + optional_columns:
            acceptable_columns.append(column_name)

    # Make sure all required columns are included
    if len([x for x in required_columns if x in acceptable_columns]) == len(required_columns):
        df.columns = acceptable_columns
        return df
    else:
        missing_columns = [x for x in required_columns if x not in acceptable_columns]
        print("Question file is missing required columns %s" %(",".join(missing_columns)))
        return None


def parse_questions(question_file,exp_id,delim="\t",return_requiredcount=True,validate=False):
    '''read in a text file, separated by delim, into a pandas data frame, 
       checking that all column names are provided.

    Parameters
    ==========

    question_file: a TAB separated file to be read with experiment questions.
                   Will also be validated for columns names.
    exp_id: the experiment unique id, to be used to generate question ids
    return_requiredcount: if True, will return questions,page_count where 
                  page_count is a dictionary to look up the number of required 
                  questions on each page {1:10}
    validate: throw an error in the case that number of values != # options

    '''
    df = read_survey_file(question_file,delim=delim)
    acceptable_types = get_question_types()
    required_counts = dict()

    if isinstance(df,pandas.DataFrame):
 
        # Each question will have id [exp_id][question_count] with appended _[count] for options
        question_count = 0
        questions = []
        current_page_number = 1
        current_page = '<div class="step">'
        for question in df.iterrows():

            question_type = question[1].question_type
            question_text = question[1].question_text
            page_number = question[1].page_number
            page_class = "page%s" %(page_number)
            options = question[1].option_text
            values = question[1].option_values
            required = int(question[1].required)
            unique_id = "%s_%s" %(exp_id,question_count)
            new_question = None
            if required == 1:
                if page_number not in required_counts:
                    required_counts[page_number] = 1
                else:
                    required_counts[page_number] = required_counts[page_number] + 1

            if question_type in acceptable_types:

                # Instruction block / text
                if question_type == "instruction":
                    new_question = create_instruction(question_text,tag="h3",id_attribute=unique_id)
                
                # Radio button
                elif question_type == "radio":
                    if not str(options) == "nan" and not str(values) == "nan":
                        new_question = create_radio(text=question_text,
                                                    options=options.split(","),
                                                    values = values.split(","),
                                                    required=required,
                                                    id_attribute=unique_id,
                                                    classes=page_class,
                                                    validate=validate)
                    else:
                        print("Radio question %s found null for options or values, skipping." %(question_text))
 
                # Checkbox
                elif question_type == "checkbox":
                    if not str(options) == "nan":
                        new_question = create_checkbox(text=question_text,
                                                       options=options.split(","),
                                                       required=required,
                                                       id_attribute=unique_id,
                                                       classes=page_class)
                    else:
                        print("Checkbox question %s found null for options, skipping." %(question_text))

                # Textareas and Textfields, regular and numeric
                elif question_type == "textarea":
                    new_question = create_textarea(question_text,
                                                   required=required,
                                                   id_attribute=unique_id,
                                                   classes=page_class)

                elif question_type == "textfield":
                    new_question = create_textfield(question_text,
                                                    required=required,
                                                    id_attribute=unique_id,
                                                    classes=page_class)

                elif question_type == "numeric":
                    new_question = create_numeric_textfield(question_text,
                                                            required=required,
                                                            id_attribute=unique_id,
                                                            classes=page_class)


                # Table
                elif question_type == "table":
                    print("Table option not yet supported! Coming soon.")
 
                question_count+=1
            
            if new_question != None:
                # Add the new question to the current page
                if page_number == current_page_number:                 
                    current_page = "%s\n%s" %(current_page,new_question)
                # Save the current page, add the current question to the next page
                else:
                    questions.append("%s</div>" %current_page)
                    current_page = '<div class="step">\n%s' %new_question
                    current_page_number = page_number

        # Add the last page
        questions.append("%s</div>" %current_page)

        if return_requiredcount == True:
            return questions,required_counts
        return questions
    else:
        return None


def generate_survey(config, form_action="#", survey_file="survey.tsv", get_validation=True):

    '''generate_survey takes a list of questions and outputs html
       for an expfactory survey, and validation code

    Parameters
    ==========

    experiment: The experiment loaded config.json
    form_action: the form action to take at the bottom of the page
    survey_file: the survey file, should be survey.tsv for a valid survey experiment
    get_validation: get code for validation, default is True
    csrf_token: if true, include django code for csrf_token ({% csrf_token %})

    '''       
    classes = "experiment-layout mdl-layout mdl-layout--fixed-header mdl-js-layout mdl-color--grey-100"

    # We will generate unique ids for questions based on the exp_id
    exp_id = config["exp_id"]
    questions,required_count = parse_questions(survey_file,exp_id=exp_id)

    validation = parse_validation(required_count)

    if questions is not None:
        survey = '<div class="%s">\n<div class="experiment-ribbon"></div>\n<main class="experiment-main mdl-layout__content">\n<div class="experiment-container mdl-grid">\n<div class="mdl-cell mdl-cell--2-col mdl-cell--hide-tablet mdl-cell--hide-phone">\n</div>\n<div class="experiment-content mdl-color--white mdl-shadow--4dp content mdl-color-text--grey-800 mdl-cell mdl-cell--8-col">\n\n<div id="questions">\n\n<form name="questions" action="%s", method="POST">' %(classes,form_action)

        for question in questions:
            survey = "%s\n%s" %(survey,question)       
        if get_validation == True:
            return survey,validation    
        return survey
    else:
        print("ERROR: parsing input text file survey.tsv. Will not generate survey HTML")


def export_questions(experiment,experiment_folder,survey_file="survey.tsv",delim="\t"):
    '''reads in a text file, separated by delim, and returns 
       a json data structure with questions to look up


    Parameters
    ==========

    question_file: a TAB separated file to be read with experiment questions. Will also be validated for columns names.
    exp_id: the experiment unique id, to be used to generate question ids
    experiment_folder: should contain survey.tsv, a TAB separated file with question data. Will be read into a pandas data frame, and columns must follow expfactory standard. Data within columns is separated by commas.
    survey_file: the survey file, should be survey.tsv for a valid survey experiment

    '''
    exp_id = experiment[0]["exp_id"]
    question_file = "%s/%s" %(experiment_folder,survey_file)
    df = read_survey_file(question_file,delim=delim)
    acceptable_types = get_question_types()

    if isinstance(df,pandas.DataFrame):
 
        # Each question will have id [exp_id][question_count] with appended _[count] for options
        question_count = 0
        questions = dict()
        for question in df.iterrows():

            question_type = question[1].question_type
            question_text = question[1].question_text
            page_number = question[1].page_number
            page_class = "page%s" %(page_number)
            options = question[1].option_text
            values = question[1].option_values
            required = int(question[1].required)
            unique_id = "%s_%s" %(exp_id,question_count)
            new_question = None

            if question_type in acceptable_types:

                # Instruction block / text
                if question_type == "instruction":
                    new_question = export_instruction(question_text,
                                                      id_attribute=unique_id,
                                                      required=required)
                
                # Radio button
                elif question_type == "radio":
                    if not str(options) == "nan" and not str(values) == "nan":
                        new_question = export_radio(text=question_text,
                                                    options=options.split(","),
                                                    values = values.split(","),
                                                    required=required,
                                                    id_attribute=unique_id)
                    else:
                        print("Radio question %s found null for options or values, skipping." %(question_text))
 
                # Checkbox
                elif question_type == "checkbox":
                    if not str(options) == "nan":
                        new_question = export_checkbox(text=question_text,
                                                       options=options.split(","),
                                                       required=required,
                                                       id_attribute=unique_id)
                    else:
                        print("Checkbox question %s found null for options, skipping." %(question_text))

                # Textareas and Textfields, regular and numeric
                elif question_type in ["textarea","textfield","numeric"]:
                    new_question = export_textfield(question_text,
                                                   required=required,
                                                   id_attribute=unique_id)
 
                question_count+=1
                if isinstance(new_question,dict):
                    questions[new_question["id"]] = new_question
                elif isinstance(new_question,list):
                    for nq in new_question:
                        questions[nq["id"]] = nq

        return questions
    else:
        return None



## MAIN ########################################################################

def get_parser():

    parser = argparse.ArgumentParser(
    description="expfactory: generate survey from config.json and question file")

    # Experiment Runtime Arguments
    parser.add_argument('--force', '-f',dest="force",
                         help="force overwrite when index.html already exists",
                         default=False, action='store_true')

    parser.add_argument("--folder", dest='folder', 
                         help="folder with config.json and survey.tsv", 
                         type=str, default=None)

    parser.add_argument("--action", "-a",dest='action', 
                         help="form action (default is #)",
                         type=str, default="#")

    parser.add_argument("--output","-o", dest='output', 
                         help="output file for survey index (defaults to index.html)",
                         type=str, default=None)


    return parser

def main():

    parser = get_parser()

    try:
        args = parser.parse_args()
    except:
        sys.exit(0)


    folder = args.folder
    if folder is None:
        folder = os.getcwd()
    folder = os.path.abspath(folder)    

    survey = "%s/survey.tsv" %folder
    if not os.path.exists(survey):
        bot.error("Cannot find %s, required to generate survey." %survey)
        sys.exit(1)

    config = load_experiment(folder)    
    html,validation = generate_survey(config=config,
                                      survey_file=survey,
                                      form_action=args.action)

    output = args.output
    if output is None:
        output = folder

    output_index = "%s/index.html" %folder

    if os.path.exists(output_index) and args.force is False:
        bot.error("%s already exists, use --force to overwrite." %output_index)
        sys.exit(1)

    bot.info("Writing output files to %s" %output_index)

    template = get_template('survey/index.html')
    template = sub_template(template, "{{html}}", html)
    template = sub_template(template, "{{exp_id}}", config['exp_id'])
    template = sub_template(template, "{{validation}}", validation)

    write_file(output_index, template)

if __name__ == '__main__':
    main()    

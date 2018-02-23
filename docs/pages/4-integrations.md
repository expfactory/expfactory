---
layout: default
title: Integrations
pdf: true
permalink: /integrations
---

# Contribute a Survey
A survey is (for now) just an experiment that is primarily questions. Since this is a common need for 
researchers, we have developed a simple means to turn a tab separated file into a web-ready experiment.
We will be using the Experiment Factory survey generator to convert a tab delimited file of questions (called `survey.tsv`)
with a standard [experiment factory config.json](#the-experiment-config) (detailed above) to generate a folder with web content to serve your experiment.

## Usage

First, generate your questions and config. As linked above, the configuration file
has the same requirements as an experiment in the Experiment Factory. For template,
you should put `"survey"`. The survey file should have the following fields in the 
first row, the header:

 - `question_type`: can be one of textfield, numeric (a numeric text field), radio, checkbox, or instruction. These are standard form elements, and will render in the Google Material Design Lite style.
 - `question_text`: is the text content of the question, e.g., How do you feel when you wake up in the morning?
 - `required`: is a boolean (0 or 1) to indicate if the participant is required to answer the question (1) or not (0) before moving on in the survey.
 - `page_number`: determines the page that the question will be rendered on. If you look at an example survey you will notice that questions are separated by Next / Previous tabs, and the final page has a Finish button. It was important for us to give control over pagination to preserve how some “old school” questionnaires were presented to participants.
 - `option_text`: For radio and checkboxes, you are asking the user to select from one or more options. These should be the text portion (what the user sees on the screen), and separated by commas (e.g, Yes,No,Sometimes. Note: these fields are not required for instructions or textbox types, and can be left as empty tabs.
 - `option_values`: Also for radio and checkboxes, these are the data values that correspond to the text. For example, the option_text Yes,No may correspond to 1,0. This field is typically blank for instructions or textbox types.

We have provided an folder with examples ([state-mindfulness-survey](https://github.com/expfactory-experiments/state-mindfulness-survey)) that you can use to generate a new survey.

## Run the Container
To generate the survey, we will run the container from the folder where our two files are.
If we run without specifying `start` we will get a help prompt. But really we don't need to look at it,
because most of the arguments are set in the image. We just need to make sure that 

 - 1. the `config.json` and `survey.tsv` are in the present working directory
 - 2. we specify `start`
 - 3. we map the `$PWD` (or where our survey and config are) to `/data` in the container

```
cd state-mindfulness-survey
ls 
config.json    survey.tsv
```

The output is minimal, but when we finish, our survey is ready!

```
$ docker run -v $PWD:/data vanessa/expfactory-survey start
Writing output files to /data/index.html
index.html
js
css
LICENSE
README.md

$ ls
config.json  css  index.html  js  LICENSE  README.md  survey.tsv
```

Now we can easily test it by opening a web browser:

```
python -m http.server 9999
```

If you need to generate the `index.html` again and force overwrite, use `--force`.

```
docker run -v $PWD:/data vanessa/expfactory-survey start --force
```

## Development
If you want to build the image:

```
docker build -t vanessa/expfactory-survey .
```

# Expfactory Robots
The Experiment Factory robots are a set of scripts (and associated containers) that provide an automated means to run through a set of experiments or surveys. We currently have support for experiments with a predictable structure, including jspsych and the surveys produced by the experiment factory generator tool above.
 
[![asciicast](https://asciinema.org/a/153497.png)](https://asciinema.org/a/153497?speed=3)

For complete setup and usage, see the most updated docs in the [Github repository](https://www.github.com/expfactory/expfactory-robots). Here we will review a "quick start" with a Singularity image.


## Singularity Usage
While the primary software is not yet ported into Singularity, we provide tools for you to use for Singularity containers as well. You will need to [install Singularity](https://singularityware.github.io/install-linux) first. Singularity is ideal for this use case because of the seamless nature between the container and host. We have a [pre-built image](https://www.singularity-hub.org/collections/380) on Singularity Hub for your use:

```
singularity pull --name expfactory-robots.simg shub://expfactory/expfactory-robots
./expfactory-robots.simg --help
```

To run the image, you will basically want to bind the *parent* folder where your task is to `/data` in the container, and specify the path to the experiment *relative to `data`* In the example below, we have cloned the [test-task](https://www.github.com/expfactory-experiments/test-task) folder in `/tmp` (`/tmp/test-task`).


```
cd /tmp && git clone https://www.github.com/expfactory-experiments/test-task
```

and now you can run the robot:

```
singularity run --bind /tmp:/data expfactory-robots.simg /data/test-task
Recruiting jspsych robot!
[folder] /data/test-task
LOG STARTING TEST OF EXPERIMENT
127.0.0.1 - - [17/Dec/2017 06:52:47] "GET / HTTP/1.1" 200 -
127.0.0.1 - - [17/Dec/2017 06:52:47] "GET /jspsych.css HTTP/1.1" 200 -
127.0.0.1 - - [17/Dec/2017 06:52:47] "GET /default_style.css HTTP/1.1" 200 -
127.0.0.1 - - [17/Dec/2017 06:52:47] "GET /style.css HTTP/1.1" 200 -
127.0.0.1 - - [17/Dec/2017 06:52:47] "GET /js/jquery.min.js HTTP/1.1" 200 -
127.0.0.1 - - [17/Dec/2017 06:52:47] "GET /js/math.min.js HTTP/1.1" 200 -
127.0.0.1 - - [17/Dec/2017 06:52:47] "GET /js/jspsych/jspsych.js HTTP/1.1" 200 -
127.0.0.1 - - [17/Dec/2017 06:52:47] "GET /js/jspsych/plugins/jspsych-text.js HTTP/1.1" 200 -
127.0.0.1 - - [17/Dec/2017 06:52:47] "GET /js/jspsych/poldrack_plugins/jspsych-poldrack-text.js HTTP/1.1" 200 -
127.0.0.1 - - [17/Dec/2017 06:52:47] "GET /js/jspsych/poldrack_plugins/jspsych-poldrack-instructions.js HTTP/1.1" 200 -
127.0.0.1 - - [17/Dec/2017 06:52:47] "GET /js/jspsych/poldrack_plugins/jspsych-attention-check.js HTTP/1.1" 200 -
127.0.0.1 - - [17/Dec/2017 06:52:47] "GET /js/jspsych/poldrack_plugins/jspsych-poldrack-single-stim.js HTTP/1.1" 200 -
127.0.0.1 - - [17/Dec/2017 06:52:47] "GET /js/jspsych/plugins/jspsych-survey-text.js HTTP/1.1" 200 -
127.0.0.1 - - [17/Dec/2017 06:52:47] "GET /js/jspsych/plugins/jspsych-call-function.js HTTP/1.1" 200 -
127.0.0.1 - - [17/Dec/2017 06:52:47] "GET /js/jspsych/poldrack_plugins/poldrack_utils.js HTTP/1.1" 200 -
127.0.0.1 - - [17/Dec/2017 06:52:47] "GET /experiment.js HTTP/1.1" 200 -
127.0.0.1 - - [17/Dec/2017 06:52:48] "GET /%3Cdiv%20class%20=%20%22shapebox%22%3E%3Cdiv%20id%20=%20%22cross%22%3E%3C/div%3E%3C/div%3E HTTP/1.1" 404 -
127.0.0.1 - - [17/Dec/2017 06:52:48] "GET /favicon.ico HTTP/1.1" 200 -
127.0.0.1 - - [17/Dec/2017 06:52:58] "POST /save HTTP/1.1" 501 -
LOG FINISHING TEST OF EXPERIMENT
LOG [done] stopping web server...
```

The same can be done for a survey folder (e.g., [bis11](https://www.github.com/expfactory-experiments/bis11-survey)), but specify the `--robot`

```
singularity run --bind /tmp:/data expfactory-robots.simg /data/bis11-survey
Recruiting survey robot!
[folder] /data/bis11-survey
LOG STARTING TEST OF SURVEY
127.0.0.1 - - [17/Dec/2017 07:09:38] "GET / HTTP/1.1" 200 -
127.0.0.1 - - [17/Dec/2017 07:09:38] "GET /css/material.blue-red.min.css HTTP/1.1" 200 -
127.0.0.1 - - [17/Dec/2017 07:09:38] "GET /css/surveys.css HTTP/1.1" 200 -
127.0.0.1 - - [17/Dec/2017 07:09:38] "GET /css/jquery-ui-1.10.4.custom.min.css HTTP/1.1" 200 -
127.0.0.1 - - [17/Dec/2017 07:09:38] "GET /css/style.css HTTP/1.1" 200 -
127.0.0.1 - - [17/Dec/2017 07:09:38] "GET /js/jquery-2.1.1.min.js HTTP/1.1" 200 -
127.0.0.1 - - [17/Dec/2017 07:09:38] "GET /js/material.min.js HTTP/1.1" 200 -
127.0.0.1 - - [17/Dec/2017 07:09:38] "GET /js/jquery-ui-1.10.4.custom.min.js HTTP/1.1" 200 -
127.0.0.1 - - [17/Dec/2017 07:09:38] "GET /js/jquery.wizard.js HTTP/1.1" 200 -
127.0.0.1 - - [17/Dec/2017 07:09:38] "GET /js/jquery.form-3.50.js HTTP/1.1" 200 -
127.0.0.1 - - [17/Dec/2017 07:09:38] "GET /js/jquery.validate-1.12.0.min.js HTTP/1.1" 200 -
127.0.0.1 - - [17/Dec/2017 07:09:38] "GET /css/images/ui-bg_flat_75_ffffff_40x100.png HTTP/1.1" 200 -
127.0.0.1 - - [17/Dec/2017 07:09:38] "GET /css/images/ui-bg_highlight-soft_75_cccccc_1x100.png HTTP/1.1" 200 -
127.0.0.1 - - [17/Dec/2017 07:09:38] "GET /favicon.ico HTTP/1.1" 200 -
LOG Testing page 1
LOG Testing page 2
LOG Testing page 3
LOG Testing page 4
LOG Testing page 5
LOG FINISHING TEST OF SURVEY
LOG [done] stopping web server...
```

<div>
    <a href="/expfactory/contribute.html"><button class="previous-button btn btn-primary"><i class="fa fa-chevron-left"></i> </button></a>
    <a href="/expfactory/"><button class="next-button btn btn-primary"><i class="fa fa-chevron-right"></i> </button></a>
</div><br>

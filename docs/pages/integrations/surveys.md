---
layout: default
title: Surveys Integrations
pdf: true
permalink: /integration-surveys
---

# Contribute a Survey

A survey is (for now) just an experiment that is primarily questions. Since this is a common need for 
researchers, we have developed a simple means to turn a tab separated file into a web-ready experiment.
We will be using the Experiment Factory survey generator (a [Docker container](https://hub.docker.com/r/vanessa/survey-generator/)) to convert a tab delimited file of questions (called `survey.tsv`) with a standard [experiment factory config.json](https://expfactory.github.io/expfactory/contribute#the-experiment-config) to generate a folder with web content to serve your experiment.

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
 - `option_values`: For radio buttons, these are the data values that correspond to the text. For example, the option_text Yes,No may correspond to 1,0. For checkboxes, the value will be a copy of the question if (and only if) the box is checked. This field is typically blank for instructions or textbox types.

We have provided an folder with examples ([state-mindfulness-survey](https://github.com/expfactory-experiments/state-mindfulness-survey)) that you can use to generate a new survey.

## Run the Container
To generate the survey, we will run [the container](https://hub.docker.com/r/vanessa/survey-generator/) from the folder where our two files are.
If we run without specifying `start` we will get a help prompt. But really we don't need to look at it,
because most of the arguments are set in the image. We just need to make sure that 

 1. the `config.json` and `survey.tsv` are in the present working directory
 2. we specify `start`
 3. we map the `$PWD` (or where our survey and config are) to `/data` in the container

Let's just wget the needed survey.tsv and config.json, because the repository has the completed survey.

```
mkdir -p /tmp/mindfulness-survey
cd /tmp/mindfulness-survey
wget https://raw.githubusercontent.com/expfactory-experiments/state-mindfulness-survey/master/config.json
wget https://raw.githubusercontent.com/expfactory-experiments/state-mindfulness-survey/master/survey.tsv
```
```
ls 
config.json    survey.tsv
```

Make a README to describe your survey!

```
echo "My Awesome Survey!" >> README.md
```

The output is minimal, but when we finish, our survey is ready!

```
$ docker run -v $PWD:/data vanessa/survey-generator start
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
python3 -m http.server 9999
```

If you need to generate the `index.html` again and force overwrite, use `--force`.

```
docker run -v $PWD:/data vanessa/survey-generator start --force
```

## Development
If you want to build the image:

```
docker build -t vanessa/survey-generator .
```

<div>
    <a href="/expfactory/integrations"><button class="previous-button btn btn-primary"><i class="fa fa-chevron-left"></i> </button></a>
    <a href="/expfactory/integration-robots"><button class="next-button btn btn-primary"><i class="fa fa-chevron-right"></i> </button></a>
</div><br>

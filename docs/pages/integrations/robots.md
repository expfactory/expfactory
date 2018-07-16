---
layout: default
title: Experiment Factory Robots
pdf: true
permalink: /integration-robots
---


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
    <a href="/expfactory/integration-surveys"><button class="previous-button btn btn-primary"><i class="fa fa-chevron-left"></i> </button></a>
    <a href="/expfactory/integration-labjs"><button class="next-button btn btn-primary"><i class="fa fa-chevron-right"></i> </button></a>
</div><br>

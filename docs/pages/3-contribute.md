---
layout: default
title: Contribute an Experiment
pdf: true
permalink: /contribute
---

This guide will walk you through contribution of an experiment. We are still developing these steps, and there may be small changes as we do.


# The general steps
The general steps are the following:

 1. create an experiment repository
 2. write a metadata `config.json` file to describe it
 3. make a pull request to this library repository to request addition of your experiment

Each of these steps is outlined in detail below.

## The experiment repository
You will want to first make an experiment repository. The repository should contain all required files (css style sheets, javascript, and other image and media) that are required to run your experiment. If you cd into the folder and run:

```
python -m http.server 9999
```

And open your browser to [localhost:9999](localhost:9999) your experiment should run. For a static experiment, that means presence of an `index.html` file. We will discuss more complicated setups that might require variables and/or building later. For now, let's discuss the simplest use case, this static experiment with HTML and CSS that can submit some JSON result when the participant finishes.


## The experiment config
In order to make your experiment programatically accessible, we require a configuration file, a `config.json` file that lives in the root of the experiment repository. A `config.json` should look like the following:

```
{
    "name": "Test Task",
    "description": "A short test task to press spacebar when you see the X.",
    "exp_id": "test-task",
    "url": "https://www.github.com/expfactory-experiments/test-task",
    "template":"jspsych",
    "cognitive_atlas_task_id": "tsk_4a57abb949dc8",
    "contributors": [
                     "Ian Eisenberg",
                     "Zeynep Enkavi",
                     "Patrick Bissett",
                     "Vanessa Sochat",
                     "Russell Poldrack"
                    ], 
    "time":1,
    "reference": "http://www.sciencedirect.com/science/article/pii/0001691869900651"
}
```

 - `exp_id`: is the experiment factory unique identifier. It must be unique among other experiment factory-provided experiments *[required]*.
 - `name`: Is a human friendly name for the experiment *[required]*.
 - `description`: A brief description of your experiment.
 - `contributors`: is a list of names, emails, or Github names for people that have contributed to the generation of the experiment. 
 - `time`: is an integer value that gives the estimated time for the experiment to run *[required]*
 - `reference`: is an article, link to documentation, or other resource to provide more information on the experiment.
```

You should not keep a version in this metadata file, but instead use Github tags and commits. This information will be added automatically upon build of your experiment container.


## Add the Experiment
When your experiment is ready to go, you should fork this repository, and in the [experiments](experiments) folder, create a file named equivalently to the main identifier (`exp_id`) of your experiment. An example is shown below. The following file should then be submit via a pull request.

### Experiment Metadata File
If my experiment is called `tower-of-london`, then my `exp_id` (the identifier) is `tower-of-london` and I probably have a Github repository called `tower-of-london`. I would add a file called `experiments/tower-of-london.json` that has the following content:


```
{

   "name": "tower-of-london",
   "maintainer": "@vsoch",
   "github":     "https://github.com/expfactory-experiments/tower-of-london.git"

}
```

 - `maintainer`: is a contact for when an issue arises with the expeiment. In the example we use a Github username, and you could also use an email.
 - `name`: is the same identifier for the experiment, the `exp_id`.
 - `github`: Is the most important metadata - the location of the experiment


# Experiment Requirements
This section will be expanded as we develop. We try to keep requirements minimal to allow you maximum flexibility to use the libraries of your choosing. The minimum requirements are the following:

 - the experiment runs statically. When it finishes, it posts to `localhost/finish`, and on successful POST redirects to `localhost/next`.
 - an `index.html` file and `config.json` in the root of the folder.
 - (optional) documentation about any special variables that can be set in the Singularity build recipe environment section for it (more on this later).
 - an associated repository to clone from, (optionally) registered in the library.

# Testing Experiments
Each contribution is tested for the conditions above when the pull request is issued. When tests pass, your experiment is added to the library, and available for discovery by anyone that uses the expfactory software. This means availability in the [library](https://expfactory.github.io/library/index.json), and the various tools that use it.

# Deploying Experiments
approved merged will make it available in the [library](https://expfactory.github.io/library/index.json). More information will be added about using the library as it is developed.

<div>
    <a href="/expfactory/usage.html"><button class="previous-button btn btn-primary"><i class="fa fa-chevron-left"></i> </button></a>
    <a href="/expfactory/development.html"><button class="next-button btn btn-primary"><i class="fa fa-chevron-right"></i> </button></a>
</div><br>

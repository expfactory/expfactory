---
layout: default
title: Contribute an Experiment
pdf: true
permalink: /contribute
---

# Contribute an Experiment

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
    "exp_id": "test-task",
    "description": "A short test task to press spacebar when you see the X.",
    "instructions": "Press the spacebar. Derp.",
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
    "reference": ["http://www.sciencedirect.com/science/article/pii/0001691869900651"]
}
```

 - `name`: Is a human friendly name for the experiment *[required]*.
 - `exp_id`: is the experiment factory unique identifier. It must be unique among other experiment factory-provided experiments *[required]*. It must also correspond to the repository name that houses the experiment *[required]*. 
 - `description`: A brief description of your experiment *[required]*.
 - `instructions`: What should the participant do? *[required]*.
 - `url`: is the Github full url of the repository. The experiment must be served (for preview) via Github pages (easiest is to serve "master").
 - `template`: is an old legacy term that described experiment types for version 1.0 of the Experiment Factory. It doesn't hurt to keep it.
 - `contributors`: is a list of names, emails, or Github names for people that have contributed to the generation of the experiment. 
 - `cognitive_atlas_task_id`: is an identifier for the [Cognitive Atlas](http://cognitiveatlas.org/) task for the experiment, if applicable.
 - `time`: is an integer value that gives the estimated time for the experiment to run *[required]*
 - `reference`: is a list of articles, link to documentation, or other resource to provide more information on the experiment.
```

You can add whatever metadata you want to the config.json, and you can also add labels to the container to be programatically accessible (more later on this). You should not keep a version in this metadata file, but instead use Github tags and commits. This information will be added automatically upon build of your experiment container.


## Add the Experiment
When your experiment is ready to go, you should fork the [library repository](https://expfactory.github.io/library), and in the `experiments` folder, create a file named equivalently to the main identifier (`exp_id`) of your experiment in the folder `docs/_library`. For example, for the test task I would create:

```
touch docs/_library/test-task.md
```

and it's contents would be:

```
---
layout: experiment
name:  "test-task"
maintainer: "@vsoch"
github: "https://www.github.com/expfactory-experiments/test-task"
preview: "https://expfactory-experiments.github.io/test-task"
tags:
- test
- jspsych
- experiment
---

This was a legacy experiment that has been ported into its Experiment Factory Reproducible Container version. If you'd like to make the experiment, it's documentation, or use better, please contribute at the repositories
linked below.
```

The layout should remain `experiment` (this just determines how to render the page, in case we want to add other kinds of rendering in the future). The `name` should correspond with the `exp_id` (test-task) and both Github and Repo are required (this is a sanity check to ensure that, when we test, the repository you are claiming to have the task has a config.json that claims the same thing). For tags, add any terms that you think would be useful to search (they are generated automatically in the experiment table).

The content on the bottom can be anything that you want to say about the experiment. You can include links, background, or even custom content like video. This input will render markdown into HTML, and also accepts HTML, so feel free to add what you need to describe your experiment. An example of the rendered page above can be [seen here](https://expfactory.github.io/experiments/e/test-task/).

The following file should then be submit via a pull request. The pull request will use the metadata to clone and test the experiment, along with your repository. When it is merged, it will appear automatically in teh web interface and be [available programmatically](https://expfactory.github.io/experiments/library.json).


# Experiment Requirements
This section will be expanded as we develop. We try to keep requirements minimal to allow you maximum flexibility to use the libraries of your choosing. The minimum requirements are the following:

 - the experiment runs statically. When it finishes, it posts to `localhost/finish`, and on successful POST redirects to `localhost/next`.
 - an `index.html` file and `config.json` in the root of the folder, as described above.
 - (optional) documentation about any special variables that can be set in the Singularity build recipe environment section for it (more on this later).
 - an associated repository to clone from, with a preview on Github pages.

# Testing Experiments
Each contribution is tested for the conditions above when the pull request is issued. When tests pass, your experiment is added to the library, and available for discovery by anyone that uses the expfactory software. This means availability in the [library](https://expfactory.github.io/experiments/library.json), and the various tools that use it.

# Deploying Experiments
Approved and merged experiments will be made available in the [library](https://expfactory.github.io/experiments/library.json). More information will be added about using the library as it is developed.

<div>
    <a href="/expfactory/usage.html"><button class="previous-button btn btn-primary"><i class="fa fa-chevron-left"></i> </button></a>
    <a href="/expfactory/development.html"><button class="next-button btn btn-primary"><i class="fa fa-chevron-right"></i> </button></a>
</div><br>

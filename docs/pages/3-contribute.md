---
layout: default
title: Contribute an Experiment
pdf: true
permalink: /contribute
---

# Contribute an Experiment

This guide will walk you through contribution of an experiment. We are still developing these steps, and there may be small changes as we do. 

## Prerequisites

### Developer Pre-reqs
You should understand basic html and css (or another web syntax of your choice) and how to create some form of web application that collects data and then can submit via a POST. If you are developing a web experiment, you should also understand how to bring up a basic web server to test your experiment. This is a very different approach from the first version of the Experiment Factory that expected a predictable template, and performed generation of an experiment behind the scenes. If you don't have all this knowledge, it's ok! Just [post an issue on our board](https://www.github.com/expfactory/expfactory/issues) and we will help. It's both fun to learn, and fun to participate in open source development.

### Experiment Pre-reqs
The most basic experiment contribution could be a web form, an intermediate contribution might be using a tool like jspsych to generate an experiment, and a more substantial contribution would use some web framework that requires "compiling" a final application (e.g., nodejs). Minimally, your final experiment must meet the following criteria:

 - **all dependencies can be included in a folder**: While content delivery networks (CDNs) are great for obtaining resources, you can be more assured of having a file if you download it locally.
 - **the experiment runs via a single file**: The server will be authenticating pages based on sessions and CSRF. For now, your experiment is required to run on a single page, meaning that the `POST` to save data comes from the same page where the experiment started.
 - **the experiment runs statically** When it finishes, it posts to `/finish`, and on successful POST redirects to `/next`.
 - (optional) documentation about any special variables that can be set in the Singularity build recipe environment section for it (more on this later).
 - **experiment completion** should have a POST of json data (`{"data": data}`) to `/save`. If successful, it navigates to `/next`. If not successful, data should be saved locally in the format of your choice (for preview and testing purposes).


# The general steps
The general steps are the following:

 1. create an experiment repository
 2. write a metadata `config.json` file to describe it
 3. test your experiment locally
 4. make a pull request to this library repository to request addition of your experiment


Each of these steps is outlined in detail below.

## The experiment repository
You will want to first make an experiment repository. The repository should contain all required files (css style sheets, javascript, and other image and media) that are required to run your experiment. If you've never used Github before, it's ok! There are plenty of [guides available](https://guides.github.com/activities/hello-world/) to learn, and this is a good time to start. So you will want to:

 - if you don't have one, create a Github account
 - create a remote repository in the Github interface
 - clone your repository to your local machine
 - create your experiment in the repository folder, add files, and push!

**Important** make sure that once you have pushed your experiment, you go into the settings and have github pages render on the **master** branch. This means that a preview of your experiment will always be available on the web, served directly from your repository. For this example, we clicked the "Settings" tab from the main repository branch, and then scrolled (very far down!) to set the following:

<div>
    <img src="/expfactory/img/contribute/github-pages.png"><br>
</div>

It's also helpful to copy paste this address and add it to the main repository description along with meaningful "topic tags" so other users can preview it easily.

<div>
    <img src="/expfactory/img/contribute/preview.png"><br>
</div>


Now let's pretend we created out Github remot, and have our experiment in our local repository (a folder on your machine with the `.git` hidden directory). We need to bring up a web server, and open our browser to the port we are using to see our experiment. The easiest way to bring up a server is by using python. If you cd into the folder and run:

```
cd my-experiment/

python -m http.server 9999         # python 3
python2 -m SimpleHTTPServer 9999   # python 2
Serving HTTP on 0.0.0.0 port 9998 ...
```

The last number (9999) is the port. The modules are actually the same, but the python2 version was migrated to be part of `http.server` in Python 3. When you see the message that the experiment is being served, open your browser to [localhost:9999](localhost:9999) your experiment should run. For a static experiment, that means presence of an `index.html` file. If you require building or compiling, do this before you run the server, and have the final result be an `index.html`. We will discuss more complicated setups that might require variables and/or building later. For now, let's discuss the simplest use case, this static experiment with HTML and CSS that can submit some JSON result when the participant finishes. At this point you should test that your experiment runs as you would expect.

**My experiment isn't running!**
The most common issues have to do with missing dependencies (js or css files) and you can debug by looking in the console of your browser. In Chrome/Firefox this means right clicking on the window, clicking "Inspect" and then you see the developers console pop up. if you look at the "Console" tab you will likely see the issue. For example, here is an early test where I had forgotten to update paths for a series of files:

<div>
    <img src="/expfactory/img/contribute/debugging.png"><br>
</div>

I could then change the paths, and refresh the page, and see the experiment!

<div>
    <img src="/expfactory/img/contribute/fixed.png"><br>
</div>


Note that you don't need to restart the python web server to see changes, you can just refresh the page. This is the beauty of statically served content!

## The experiment config
Great! Once you are here, you have a folder with a working experiment. This is no small task! In order to make your experiment programatically accessible, we require a configuration file, a `config.json` file that lives in the root of the experiment repository. A `config.json` should look like the following:

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

You can add whatever metadata you want to the config.json, and you can also add labels to the container to be programatically accessible (more later on this). You should not keep a version in this metadata file, but instead use Github tags and commits. This information will be added automatically upon build of your experiment container. We also **strongly** encourate you to add a LICENSE file to your work.


## Test the Experiment
Your experiment will be tested when you submit a pull request (as we just showed above). However you can run the tests before filing the PR. There are two kinds of tests, testing an **experiment** and testing a **contribution**:

 - an **experiment** is a single folder with static content to serve an experiment. Usually
this means an `index.html` file and associated style (css) and javascript (js), and the config.json
we just talked about above. This test is appropriate if you've prepared an experiment folder but haven't yet pushed to Github.
 - a **contribution** is a submission of one or more experiments to the [library](https://www.github.com/expfactory/experiments),  meaning one or more markdown file intended to be added to the `_library` folder. The contribution tests also test the experiments, but retrieves them from your repository on Github. Thus, this test is useful when you've pushed your experiment to Github, and want to (locally) test if it's ready for the library.

For both cases above, we provide a prebuilt container so you don't need to install the expfactory software locally.

```
singularity pull --name expfactory.test shub://expfactory/expfactory:test
```

What tests are included?

```
singularity apps expfactory.test
test-contribution
test-experiment
``` 

You can ask for help for either with `singularity help --app <appname>`

### Test an Experiment
If you run without binding your folder with the experiment, you will get an error message:

```
singularity run --app test-experiment expfactory.test 
You must use --bind to bind the folder with config.json to /scif/data in the image.
```

You need to bind the folder with your experiment (containing the config.json) to `/scif/data` in the image.

```
singularity run --app test-experiment --bind $PWD:/scif/data expfactory.test 
...Test: Experiment Validation
.
----------------------------------------------------------------------
Ran 1 test in 0.001s

OK
```

### Test a Contribution
This set of tests is more stringent in that the test starts with one of more submissions (markdown files that you will ask to be added to the `_library` folder via a pull request) and goes through Github cloning to testing of your preview. Specifically it includes:

     - discovery of any markdown files in the bound folder
     - parsing of the files for required fields
     - download of the Github repositories to temporary locations
     - testing of the Github repository config.json, and preview in Github pages


You need to bind the folder with markdown files for the library to `/scif/data` this time around. These tests have a lot more output because they are more substantial:

```
$ singularity run --app test-contribution --bind _library/:/scif/data expfactory.test

...Test: Global Library validation
preview: https://expfactory-experiments.github.io/test-task
github: https://www.github.com/expfactory-experiments/test-task
maintainer: @vsoch
name: test-task
layout: experiment
tags: ['test', 'jspsych', 'experiment']
Cloning into '/tmp/tmpzbfh2w44/test-task'...
remote: Counting objects: 62, done.
remote: Compressing objects: 100% (49/49), done.
remote: Total 62 (delta 20), reused 55 (delta 13), pack-reused 0
Unpacking objects: 100% (62/62), done.
Checking connectivity... done.
Checking connectivity... done.
.../tmp/tmpmy0dlc0j/test-task/config.json
.../tmp/tmpmy0dlc0j/test-task/experiment.js
.../tmp/tmpmy0dlc0j/test-task/default_style.css
.../tmp/tmpmy0dlc0j/test-task/README.md
.../tmp/tmpmy0dlc0j/test-task/style.css
.../tmp/tmpmy0dlc0j/test-task/LICENSE
.../tmp/tmpmy0dlc0j/test-task/index.html
True
...
```

You can also use any of the expfactory software inside the image, the runscript provides the command line executable `expfactory list` by default so
you can easily see experiments available.

```
$ singularity run expfactory.test
Expfactory Version: 3.0
Experiments
1  adaptive-n-back	https://www.github.com/expfactory-experiments/adaptive-n-back
2  breath-counting-task	https://www.github.com/expfactory-experiments/breath-counting-task
3  test-task	https://www.github.com/expfactory-experiments/test-task
4  tower-of-london	https://www.github.com/expfactory-experiments/tower-of-london
```

or you can execute a custom command to the image:

```
singularity exec expfactory.test ls /opt/expfactory
LICENSE  MANIFEST.in  README.md  build	dist  docs  expfactory	expfactory.egg-info  script  setup.py
```

We will soon be adding a command line `build` function to generate a recipe on the fly, without using the interface. Stay tuned!


### Local Testing
If you do decide to test on your local machine (without the container) you will need to clone the repository first, and you can use the tests under `/script/singularity/tests` or with the library in the `tests` folder as follows:

```
python -m pip install git+https://github.com/expfactory/expfactory.git@master
python -m unittest tests.test_library
```

Any issues with your recipe will be spit out on the screen. When you are confident in your submission, then go ahead and fo the PR. What happens during the PR is the same as on your local machine - the pull request will use the metadata to clone and test the experiment, along with your repository. When it is merged, it will appear automatically in the web interface and be [available programmatically](https://expfactory.github.io/experiments/library.json).


## Add the Experiment
When your experiment is ready to go, you should fork the [library repository](https://expfactory.github.io/library), and in the `experiments` folder, create a file named equivalently to the main identifier (`exp_id`) of your experiment in the folder `docs/_library`. For example, after I've cloned the fork of my repo, I might check out a new branch for my task:


```
$ git checkout -b add/breath-counting-task
Switched to a new branch 'add/breath-counting-task'
```

and then I would create a new file:

```

touch docs/_library/breath-counting-task.md

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

The content on the bottom can be anything that you want to say about the experiment. You can include links, background, or even custom content like video. This input will render markdown into HTML, and also accepts HTML, so feel free to add what you need to describe your experiment. An example of the rendered page above can be [seen here](https://expfactory.github.io/experiments/e/test-task/). When you are done, add the newly created file with a commit to your local repository:

```
git add docs/_library/breath-counting-task.md
git commit -m "adding the breath counting task to library"
 1 file changed, 14 insertions(+)
 create mode 100644 docs/_library/breath-counting-task.md
```

and then push!

```
git push origin add/breath-counting-task
```

You should then be able to go to the [expfactory library](https://www.github.com/expfactory/experiments) interface and click the button to do a **pull request** that is **across forks** to the **expfactory master branch**. Github is usually pretty clever in knowing when you've recently submit to a branch associated with a repository. For example, when I browsed to the expfactory experiments library main repo, I saw:

<div>
    <img src="/expfactory/img/contribute/pull-request.png"><br>
</div>



# Deploying Experiments
Once you get here, you've probably had your experiment pull required approved and merged! After this, your experiment will be made available in the [library](https://expfactory.github.io/experiments/library.json). More information will be added about using the library as it is developed. You can then add your experiment to a Reproducible Experiments Container, along with any of the other selection in the library. Read about [usage](/expfactory/usage.html) for your different options if you haven't yet.

<div>
    <a href="/expfactory/usage.html"><button class="previous-button btn btn-primary"><i class="fa fa-chevron-left"></i> </button></a>
    <a href="/expfactory/development.html"><button class="next-button btn btn-primary"><i class="fa fa-chevron-right"></i> </button></a>
</div><br>

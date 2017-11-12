---
layout: default
title: Usage
pdf: true
permalink: /usage
---

# Using your Experiments Container
If you've just finished [generating your experiments container](/expfactory/generate.html) (whether a custom build or pull of an already existing container) then you are ready to use it! Here we assume that the container is running, and will look quickly at the experience of running a participant through a selection of experiments. 

## The Experiment Factory Portal
When you start your container instance, browsing to your localhost will show the entrypoint, a user portal that lists all experiments installed in the container:

<div>
    <img src="/expfactory/img/generate/portal.png"><br>
</div>


This is where the experiment administrator would select one or more experiments, either with the single large checkbox ("select all") or smaller individual checkboxes. When you make a selection, the estimated time and exeperiment count on the bottom of the page are adjusted. 

<div>
    <img src="/expfactory/img/generate/selected.png"><br>
</div>

You can make a selection and then start your session. I would recommend the `test-task` as a first try, because it finishes quickly. When you click on `proceed` you can (optionally) enter a subject name:

<div>
    <img src="/expfactory/img/generate/proceed.png"><br>
</div>

This name is currently is only used to say hello to the participant. The actual experiment identifier is based on a study id defined in the build recipe.  After proceeding, there is a default "consent" screen that you must agree to (or disagree to return to the portal):

<div>
    <img src="/expfactory/img/generate/welcome.png"><br>
</div>


Once the session is started, the user is guided through each experiment (with random selection) until no more are remaining.

<div>
    <img src="/expfactory/img/generate/preview.png"><br>
</div>


When you finish, you will see a "congratulations" screen

<div>
    <img src="/expfactory/img/generate/finish.png"><br>
</div>

and the data you will find in the mounted directory:

```
$ tree /tmp/data/expfactory/00001/

    /tmp/data/expfactory/00001/
       └── test-task-results.json

0 directories, 1 file
```

You can then stop the container, and the data will persist.


### Feedback Wanted!
A few questions for you!

 - Would password protection of the portal be desired?
 - Is a user allowed to redo an experiment? Meaning, if a session is started and the data is written (and the experiment done again) is it over-written? 
 - Is some higher level mechanism for generating user ids in advance, and then validating them with an individual, desired?

Right now, this setup is optimized for a low volume of user's in a local lab. To best develop the software for different deployment, it's important to discuss these issues. Please [post an issue](https://www.github.com/expfactory/expfactory/issues) to give feedback.


<br>
<div>
    <a href="/expfactory/generate.html"><button class="previous-button btn btn-primary"><i class="fa fa-chevron-left"></i> </button></a>
    <a href="/expfactory/contribute.html"><button class="next-button btn btn-primary"><i class="fa fa-chevron-right"></i> </button></a>
</div><br>

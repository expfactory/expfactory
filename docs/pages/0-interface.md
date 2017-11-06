---
layout: default
title: The Expfactory Interface
pdf: true
permalink: /interface
---

# The Experiment Factory Portal
When you start your container instance, browsing to your localhost will show the entrypoint, a user portal that lists all experiments installed in the container:

<div>
    <img src="/expfactory/img/generate/portal.png"><br>
</div>

This is where the experiment administrator would select one or more experiments, either with the single large checkbox or smaller individual:

<div>
    <img src="/expfactory/img/generate/selected.png"><br>
</div>

and then click on `proceed` to (optionally) enter a subject id:

<div>
    <img src="/expfactory/img/generate/proceed.png"><br>
</div>

The id is optional, and currently is only used to say hello to the participant. The actual experiment identifier is based on a study id defined in the build recipe. Once the session is started, the user is guided through each experiment (with random selection) until no more are remaining.

<div>
    <img src="/expfactory/img/generate/preview.png"><br>
</div>


### Feedback Wanted!
A few questions for you!

 - Would password protection of the portal be desired?
 - Is a user allowed to redo an experiment? Meaning, if a session is started and the data is written (and the experiment done again) is it over-written? 
 - Is some higher level mechanism for generating user ids in advance, and then validating them with an individual, desired?

Right now, this setup is optimized for a low volume of user's in a local lab. To best develop the software for different deployment, it's important to discuss these issues. Please [post an issue](https://www.github.com/expfactory/expfactory/issues) to give feedback.

<div>
    <a href="/expfactory/"><button class="previous-button btn btn-primary"><i class="fa fa-chevron-left"></i> </button></a>
    <a href="/expfactory/usage.html"><button class="next-button btn btn-primary"><i class="fa fa-chevron-right"></i> </button></a>
</div><br>

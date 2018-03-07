---
layout: default
title: Background
pdf: true
permalink: /background
toc: false
---

# Background
Behavioral research can be challenging because of software dependencies. For example, if I have a stroop task that needs a web browser and a set of system libraries to run, if I were to try and share that task with a colleague that does not have that software on his computer, it might not work. This is a huge problem for validating scientific claims that are founded on these experiments, because it means that the work cannot be reproduced. It becomes even more challenging when we need to consider things like storage of data, and how to easily generate customized experiments.

This set of tools, software called "The Experiment Factory" was made for this purpose. A user interested in deploying a behavioral assessment can simply select a grouping of paradigms from the web interface, and build a container to serve them. Once the particular set of paradigms is generated, it (along with dependencies and important settings) are carried forward with the container.

## What is a container?
A container is an encapsulated environment that includes all of these dependencies. It follows that, if we can put our software in containers that run anywhere, it is reproducible. If we make it easy to create and customize containers, we empower scientists and users to do so. Thus, the Experiment Factory takes the following approach. The base software is written in Python, and provided for you to use to generate other experiment containers. It looks like this:

```
# Base python software   # Builder container (or other tool)
[expfactory (python)]    --> [expfactory-builder (container)]  --> [your experiment (container)]
```

This general workflow using the experiment factory builder means that you could do any of the following:

 - run your experiment container across computers with Docker without worrying about dependencies
 - share you experiments container with a colleague that can reproduce the battery
 - go back and use the same version of the builder to re-create your experiment container, or a slight derivation of it
 - (developers) contribute to the core expfactory Python software to enhance the builder, or [another integration or tool](/expfactory/integrations).

If you have not heard of Docker we recommend that you [read about it first](https://www.docker.com/what-container) and go through a [getting started](https://docs.docker.com/get-started/) tutorial. When you are ready, come back here and try out the quick start. If you have any questions, [please don't hesitate to ask](https://www.github.com/expfactory/expfactory/issues).

Do you have more questions? Please [post an issue](https://www.github.com/expfactory/expfactory/issues).

<div>
    <a href="/expfactory/"><button class="previous-button btn btn-primary"><i class="fa fa-chevron-left"></i> </button></a>
    <a href="/expfactory/generate"><button class="next-button btn btn-primary"><i class="fa fa-chevron-right"></i> </button></a>
</div><br>

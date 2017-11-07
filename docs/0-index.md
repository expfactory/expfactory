---
layout: default
title: {{ site.name }}
pdf: true
permalink: /
---

<div style="float:right; margin-bottom:50px; color:#666">
Version: {{ site.version }}<br>
</div>

<div>
    <img src="img/expfactoryticketyellow.png" style="float:left">
</div><br><br>

> Nobody ever comes in... and nobody ever comes out...

<p>And that's the way that reproducible behavioral experiments should be: designed, captured, and used again with assurance of running the same thing.
The Experiment Factory software will help you create a reproducible container to deploy behavioral experiments. <span style="font-style:italic; color:darkmagenta">we are under development for this new container-based version, and will update this documentation base as we go!</span></p> Want to jump right in? Pull a demo container, start an instance named `web1`, and browse to `localhost`::

```
singularity pull --name expfactory.simg shub://expfactory/expfactory
sudo singularity instance.start --bind /tmp/data:/scif/data expfactory.simg web1
```

Read more about custom [1. generation](pages/1-generate.md) and then [2. usage](pages/2-usage.md).


## User Guide

 - [Interface](pages/0-interface.md) the user interface, if you are just looking around.
 - [Building](pages/1-generate.md) your battery means creating and configuring your image.
 - [Running](pages/2-usage.md) an obtained or newly built experiment factory container

## Library

 - [Browse](https://expfactory.github.io/experiments/) our available experiments [[json]](https://expfactory.github.io/experiments/library.json).
 - [Generate](https://expfactory.github.io/experiments/generate) a custom container from our Library, or
 - [Recipes](https://expfactory.github.io/experiments/recipes) view a pre-generated recipe based on tags in the library.

## Development Guide

 - [Contribute](pages/3-contribute.md) an experiment to the [library](https://www.github.com/expfactory/library) for others to use.
 - [Interactive](pages/4-development.md) Examples for how I (@vsoch) developed the software


<div>
    <a href="/expfactory/generate"><button class="next-button btn btn-primary"><i class="fa fa-chevron-right"></i> </button></a>
</div><br>

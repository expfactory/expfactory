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
The Experiment Factory software will help you create a reproducible container to deploy behavioral experiments. Want to jump right in? Run a demo container, and browse to localhost:</p>


```
docker run -p 80:80 vanessa/experiments start
```

Next, read more about [generation](pages/1-generate.md) of your own experiment container. Please [give feedback](https://www.github.com/expfactory/expfactory/issues) about your needs to further develop the software. The [experiments portal](https://expfactory.github.io/experiments/) will be updated as we migrate experiments from [the legacy Expfactory](https://www.github.com/expfactory/expfactory-experiments) soon. Your contributions and feedback are greatly appreciated!


## User Guide

 - [Building](pages/1-generate.md) your battery means creating and configuring your image.
 - [Using](pages/2-usage.md) an experiment factory container.
 - [Contribute](pages/3-contribute.md) an experiment to the [library](https://www.github.com/expfactory/experiments) for others to use.

## Library

 - [Browse](https://expfactory.github.io/experiments/) our available experiments [[json]](https://expfactory.github.io/experiments/library.json).
 - [Generate](https://expfactory.github.io/experiments/generate) a custom container from our Library, or
 - [Recipes](https://expfactory.github.io/experiments/recipes) view a pre-generated recipe based on tags in the library.


<div>
    <a href="/expfactory/generate"><button class="next-button btn btn-primary"><i class="fa fa-chevron-right"></i> </button></a>
</div><br>

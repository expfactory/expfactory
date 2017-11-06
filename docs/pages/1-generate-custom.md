---
layout: default
title: Customize Experiments
pdf: true
permalink: /generate-custom
toc: true
---

### Browse Experiments
Along with the recipe generator table above, you can browse experiments from your local machine. The experiments each have their own repository maintained under the Organization Expfactory Experiments ([https://www.github.com/expfactory-experiments](https://www.github.com/expfactory-experiments)). If you are interested in all the experiments available to you, you can look at the library manifest:

```
curl https://expfactory.github.io/experiments/library.json

[
    {
        "name": "adaptive-n-back",
        "github": "https://www.github.com/expfactory-experiments/adaptive-n-back",
        "preview": "https://expfactory-experiments.github.io/adaptive-n-back",
        "maintainer": "@vsoch",
        "tags": ["jspsych","experiment"]
  },

    {
        "name": "test-task",
        "github": "https://www.github.com/expfactory-experiments/test-task",
        "preview": "https://expfactory-experiments.github.io/test-task",
        "maintainer": "@vsoch",
        "tags": ["test","jspsych","experiment"]
  },

    {
        "name": "tower-of-london",
        "github": "https://www.github.com/expfactory-experiments/tower-of-london",
        "preview": "https://expfactory-experiments.github.io/tower-of-london",
        "maintainer": "@vsoch",
        "tags": ["jspsych","experiment"]
  }
]

```
or just the names

```
curl https://expfactory.github.io/experiments/library.json | grep name
        "name": "adaptive-n-back",
        "name": "test-task",
        "name": "tower-of-london",
```

You can also run the software locally to browse experiments:

```
git clone https://www.github.com/expfactory/expfactory
cd expfactory && python setup.py install
```

Note that if you install expfactory with pip you will still get the Legacy version. To see available experiments, meaning they are provided in the [experiments](https://www.github.com/expfactory/experiments) library, just type:

```
$ expfactory

Expfactory Version: 3.0
Experiments
1  adaptive-n-back	https://github.com/expfactory-experiments/adaptive-n-back.git
2  tower-of-london	https://github.com/expfactory-experiments/tower-of-london.git
3  test-task	https://www.github.com/expfactory-experiments/test-task
```


### Customizing Experiments
The reason that we are showing you how the experiments are installed is because you don't need a generator to write the Singularity Recipe for you, and you don't necessarily need to use an experiment in the library (although we advocate that you contribute for the community to work on together!). Once you've seen the experiments available above, you might find yourself in the following scenarios:

 - you want to use a local (custom) experiment that cannot be on Github or public
 - you want to use an existing template, but customize it first
 - you need to issue some "build" to generate the experiment first

Singularity containers generated from build recipes are ideal for these use cases, and we can customize the experiments to our heart's content.

**1. Customize Experiments**
if you look inside the recipe, you will see an "app" section for each experiment. We are installing each experiment as a [Standard Container Integration Format (SCI-F)](https://containers-ftw.github.io/SCI-F/) app. The high level idea is that it gives easy accessibility to multiple different internal modules in our container. In our case, an internal module is an experiment. All the `expfactory install` command does is clone the repository content, and the experiment is installed by the expfactory software:

```
%appinstall test-task
    cd .. && expfactory install -f -b /opt/expfactory/expfactory https://github.com/expfactory-experiments/test-task
```

The install routine is basically ensuring that the experiment folder (for the above, the directory we are sitting in is `/scif/apps/test-task` is populated with the experiment static files from Github, and that corresponding metadata is written. Minimally, an experiment requies:

 1. an `index.html` in this folder that serves the experiment
 2. resources (css and js files) are relatively linked to it
 3. submission of data as a `POST` to the url `/save`
 4. after post, go to the url `/next`

That's it! In terms of installing a custom experiment, it means the following:

 - You can do the same thing, cloning from Github or elsewhere
 - If have some custom build routine to produce the files for your experiment, you can write your own `%appinstall` section to do that, and install all dependencies. E.g.,

```
%appinstall custom-task
    # install jekyll / gem here
    git clone https://github.com/expfactory-experiments/test-task
    cd test-task && bundle exec jekyll build
    mv _site/* ../  
```

You can even add files and folders from your local machine, although this is generally discouraged if it breaks reproducibility of building the image.

```
%appfiles custom-task
/path/to/index.html index.html
```

It's also possible to build a writable container sandbox if you want to develop a battery (meaning have write ability in the image before producing a production image). See our [development](4-development.md) notes for how to do this.

### Expfactory wants Your Feedback!
The customization process is very important, because it will mean allowing you to select variable stimuli, lengths, or anything to make a likely general experiment specific to your use case. To help with this, @vsoch is looking for feedback about:

 - what kind of experiments (those provided in the library? generated with a build tool?) do you want to use
 - what variables do you want to customize? Do you have preference for how you would want to go about this?
 - if there is a build, when and how does it happen?

A reasonable feature would be to have the experiment manifests capture variables that are "allowed" to be changed (e.g., a stimulus number or similar) and then a snippet added to metadata about how to do the build, given that the user has set the `%applabel` that is looked for. CUrrently, It's important to remember that your experiment to be truly reproducible, other than introducing planned randomness (e.g., presentation of stimuli) it shouldn't be the case that a lot of the experiment details are required to be set at runtime. They must be frozen into the container so that when a colleague tries to reproduce your study, the exact thing is used.

With this in mind, please [let us know](https://www.github.com/expfactory/expfactory/issues) your thoughts.

[< bacl tp generate](1-generate.md)

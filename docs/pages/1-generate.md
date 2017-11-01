---
layout: default
title: Generate your Experiment Container
pdf: true
permalink: /generate
toc: true
---

# Generate your Experiment Container

### Database

**files**
The default (simplest) method for a database is flat files, meaning that results are written to a mapped folder on the local machine, and each participant has their own results folder. This option is provided as many labs are accustomed to providing a battery locally, and want to save output directly to the filesystem without having any expertise with setting up a database.

**MySQL**
For labs that wish to deploy the container on a server, you are encouraged to use a more substantial database. We will provide instructions for setting this configuration (under development).


### Write your recipe
A Singularity Recipe is a file that details how you want your container to build. In our case, we want to give instructions about which experiments to install. You can use the [example recipe provided](https://github.com/expfactory/expfactory/blob/master/Singularity) or if you haven't cloned the repo:

```
wget https://raw.githubusercontent.com/expfactory/expfactory/master/Singularity
```

This will place the build recipe `Singularity` in your present working directory, and by fault we will install two experiments, adaptive-n-back and tower-of-london. The experiments each have their own repository maintained at [https://www.github.com/expfactory-experiments](https://www.github.com/expfactory-experiments). If you are interested in all the experiments available to you, you can look at the library manifest:

```
curl https://expfactory.github.io/library/index.json

[
    {
        "maintainer": "@vsoch",
        "github": "https://github.com/expfactory-experiments/tower-of-london.git",
        "name": "tower-of-london"
    },
    {

       "name": "adaptive-n-back",
       "maintainer": "@vsoch",
       "github":   "https://github.com/expfactory-experiments/adaptive-n-back.git"

   }
]
```
or just the names

```
curl https://expfactory.github.io/library/index.json | grep name
```

If you look inside the recipe, you will see an "app" section for each experiment. All it does is clone the repository content:

```
git clone https://github.com/expfactory-experiments/adaptive-n-back
mv adaptive-n-back/* .
```

We are installing each experiment as a [Standard Container Integration Format (SCI-F)](https://containers-ftw.github.io/SCI-F/) app. The high level idea is that it gives easy accessibility to multiple different internal modules in our container. In our case, an internal module is an experiment. 


### Configure your Battery
The Experiment Factory will generate a new unique ID for each participant with some study idenitifier prefix. The default is `expfactory`, meaning that my participants will be given identifiers `expfactory_1` through `expfactory_n`. If you want to change this, just customize the variable under the `%environment` section:


```
%environment
    EXPFACTORY_STUDY_ID=expfactory
    export EXPFACTORY_STUDY_ID
```

In the future we will have an online recipe generator. At this time you would also specify your preference for a database, or any runtime variables for the experiments. We will add these notes later. Let's move on the building your battery.


### Build the Battery Container
Let's build the image, and we are going to create a development (tester) image called a "sandbox" first:


```
sudo singularity build --sandbox exp-box Singularity
```

Where `exp-box` is referring to a sandbox environment for your image. Let's break down the above. We are asking the singularity command line software to `build` an image, specifically a `--sandbox` (folder) kind for development, **from** the recipe file `Singularity`.

Once building is done, we can see what experiments are installed:


```
singularity apps expfactory
adaptive-n-back
tower-of-london
```

You can also ask for help:

```
singularity help expfactory
```

In the future I will likely make an automatic "recipe generator" that uses the config.jsons to help, for now it's just a game of copy pasting :)

<div>
    <a href="/expfactory/"><button class="previous-button btn btn-primary"><i class="fa fa-chevron-left"></i> </button></a>
    <a href="/expfactory/usage.html"><button class="next-button btn btn-primary"><i class="fa fa-chevron-right"></i> </button></a>
</div><br>

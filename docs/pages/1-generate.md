---
layout: default
title: Generate your Experiment Container
pdf: true
permalink: /generate
toc: false
---

# Really Quick Start
Pull our pre-generated example containers, and start! Your experiment portal is at [http://127.0.0.1](http://127.0.0.1) in your browser.

```
docker run -p 80:80 vanessa/experiments start
```

or if you want to see the entire set of surveys or experiments:

```
docker run -p 80:80 vanessa/expfactory-experiments start
docker run -p 80:80 vanessa/expfactory-surveys start
docker run -p 80:80 vanessa/expfactory-games start
```

# Quick Start

Make a folder. This will be a place to generate your Dockerfile.

```
mkdir -p /tmp/my-experiment/data
cd /tmp/my-experiment
```

What experiments do you want in your container? Let's see the ones that are available!
```
docker run vanessa/expfactory-builder list
```

Cool, I like `digit-span`, `spatial-span`, `test-task`, and `tower-of-london`.

```
docker run -v $PWD:/data vanessa/expfactory-builder build digit-span spatial-span tower-of-london test-task 
```

Let's build the container from the Dockerfile!

```
docker build -t expfactory/experiments .

```

Now let's start it.

```
docker run -v /tmp/my-experiment/data/:/scif/data \
           -d -p 80:80 \
           expfactory/experiments start 
```

Open your browser to localhost ([http://127.0.0.1](http://127.0.0.1)) to see the portal [portal](/expfactory/usage.html). For specifying a different database or study identifier, read the detailed start, specifically how to [customize your container runtime](#customize-your-container). 



# Detailed Start
The generation of a container comes down to adding the experiments to a text file that records all the commands to generate your container. Since we are using Docker, this file will be the Dockerfile, and you should [install Docker](https://docs.docker.com/engine/installation/) first and be comfortable with the basic usage. In these sections, we will be building your container from a customized file. You will be doing the following:

 - generating a recipe with (reproducible) steps to build a custom container
 - building the container!


## The Expfactory Builder Image
Both of these steps start with the expfactory builder container. 
We've [provided an image](https://hub.docker.com/r/vanessa/expfactory-builder) that will generate a Dockerfile,
and from it you can build your Docker image.  We don't build the image within the same 
container for the explicit purpose that you should keep a copy of the recipe
Dockerfile at hand. The basic usage is to run the image, and you can either build, test, or list.

```
$ docker run vanessa/expfactory-builder

Usage:

          docker run vanessa/expfactory-builder list
          docker run vanessa/expfactory-builder build experiment-one experiment-two ...
          docker run -v experiments:/scif/apps vanessa/expfactory-builder test
          docker run -v $PWD/_library:/scif/apps vanessa/expfactory-builder test-library
```

We will discuss each of these commands in more detail.

## Experiment Selection
The first we've already used, and it's the only required argument. We need to give the
expfactory builder a list of `experiments`. You can either [browse
the table](https://expfactory.github.io/experiments/) or see a current library list with `list.`

```
docker run vanessa/expfactory-builder list

Expfactory Version: 3.0
Experiments
1  adaptive-n-back	https://www.github.com/expfactory-experiments/adaptive-n-back
2  breath-counting-task	https://www.github.com/expfactory-experiments/breath-counting-task
3  dospert-eb-survey	https://www.github.com/expfactory-experiments/dospert-eb-survey
4  dospert-rp-survey	https://www.github.com/expfactory-experiments/dospert-rp-survey
5  dospert-rt-survey	https://www.github.com/expfactory-experiments/dospert-rt-survey
6  test-task	https://www.github.com/expfactory-experiments/test-task
7  tower-of-london	https://www.github.com/expfactory-experiments/tower-of-london
```

Try using grep if you want to search for a term in the name or url

```
docker run vanessa/expfactory-builder list | grep survey
2  alcohol-drugs-survey	https://www.github.com/expfactory-experiments/alcohol-drugs-survey
4  dospert-eb-survey	https://www.github.com/expfactory-experiments/dospert-eb-survey
5  dospert-rp-survey	https://www.github.com/expfactory-experiments/dospert-rp-survey
6  dospert-rt-survey	https://www.github.com/expfactory-experiments/dospert-rt-survey
```

## Recipe Generation
To generate a Dockerfile to build our custom image, we need to run expfactory in the container,
and mount a folder (`my-experiment`) to retrieve the image that is built. The folder
should not already contain a Dockerfile, and most appropriate is a new folder that you
intend to set up with version control (a.k.a. Github). That looks like this:

```
mkdir -p /tmp/my-experiment/data
docker run -v /tmp/my-experiment:/data \
              vanessa/expfactory-builder \
              build tower-of-london

Expfactory Version: 3.0
LOG Recipe written to /data/Dockerfile

To build, cd to recipe and:
              docker build -t expfactory/experiments .
```

Before you generate your recipe, in the case that you want "hard coded" defaults (e.g., set as defaults for future users) read the [custom build](#custom-build) section below to learn about the variables that you can customize. If not, then rest assured that these values can be specified when a built container is started.


## Container Generation
Now we would go to the folder (`/tmp/my-experiment`) to bulid our experiments container. We
could actually do this in the container for you, but it's better to generate the file first
(and save to a repository like Github for version control) than not. You have a Dockerfile and a script to run 
when it's used:

```
cd /tmp/my-experiments
ls
Dockerfile  startscript.sh
```

At this point we recommend you add `LABELS` to your Dockerfile. A label can be any form of
metadata to describe the image. Look at the [label.schema](http://label-schema.org/rc1/) for
inspiration. Then build the image, and replace `vanessa/experiment` with whatever namespace/container you
want to give to the image. It's easy to remember to correspond to your Github repository (`username/reponame`).

```
docker build -t vanessa/experiment .

# if you don't want to use cache
docker build --no-cache -t vanessa/experiment .
```

Don't forget the `.` at the end! It references the present working directory with the Dockerfile.


## Start your Container
After you do the above steps, your custom container will exist on your local machine.
First, let's pretend we haven't a clue what it does, and just run it:

```
docker run vanessa/experiment

Usage:
    
         docker run vanessa/expfactory-builder [help|list|test-experiments|start]
         docker run -p 80:80 -v /tmp/data:/scif/data vanessa/expfactory-builder start

         Commands:
                help: show help and exit
                list: list experiments in the library
                test: test experiments installed in container
                start: start the container to do the experiments*
                env: search for an environment variable set in the container
         
         *you are required to map port 80, otherwise you won't see the portal at localhost

         Options [start]:
                --database: specify a database to override the default
                --studyid: specify a studyid to override the default
```

The important command is the second usage example - we want to start the server to run experiments. The important (Docker) arguments are the following:

- `port`: The `-p 80:80` is telling Docker to map port 80 (the nginx web server) in the container to port 80 on our local machine. If we don't do this, we won't see any experiments in the browser!
- `volumes`: The second command `-v` is telling Docker we want to see the output in the container at `/scif/data` to appear in the folder `/tmp/data` on our local machine. If you are just testing and don't care about saving or seeing data, you don't need to specify this.

For this first go, we aren't going to map the data folder. This way I can show you how to shell inside an interactive container.

```
docker run -p 80:80 vanessa/experiment start

Starting Web Server

 * Starting nginx nginx
   ...done.
==> /scif/logs/gunicorn-access.log <==

==> /scif/logs/gunicorn.log <==
[2017-11-11 16:28:42 +0000] [1] [INFO] Starting gunicorn 19.7.1
[2017-11-11 16:28:42 +0000] [1] [INFO] Listening at: http://0.0.0.0:5000 (1)
[2017-11-11 16:28:42 +0000] [1] [INFO] Using worker: sync
[2017-11-11 16:28:42 +0000] [35] [INFO] Booting worker with pid: 35
```

The above is telling us that the webserver is writing output to logs in `/scif/logs`
in the image, and we are viewing the main log. The port `5000` that is running the Flask
server is being served via gunicorn at localhost.

This means that if you open your browser to localhost ([http://127.0.0.1](http://127.0.0.1)) you will
see your experiment interface! When you select an experiment, the general url will look 
something like `http://127.0.0.1/experiments/tower-of-london`. Now try hitting "Control+C" in the terminal where the server is running. You will see it exit. Refresh the browser, and see that the experiment is gone too. What we actually want to do is run the server in `detached` mode. After you've Control+C, try adding a `-d` to the original command. This means detached.


```
docker run -d -p 80:80 vanessa/experiment start
2c503ddf6a7a0f2a629fa2e55276e220246320291c14f6393a33ef54ab5d512a
```

The long identifier spit out is the container identifier, and we will reference it by the first 12 digits.
Try running `docker ps` to list your active containers - you will see it is the first one! And look at the 
`CONTAINER_ID`:

```
$ docker ps
CONTAINER ID        IMAGE                COMMAND                  CREATED             STATUS              PORTS                          NAMES
2c503ddf6a7a        vanessa/experiment   "/bin/bash /starts..."   10 minutes ago      Up 10 minutes       0.0.0.0:80->80/tcp, 5000/tcp   zealous_raman
```

## Customize Your Container

It's most likely the case that your container default is to save data to the file system, and use a study id of expfactory. You can set this to be custom at runtime, if you intend to have it change (or want to distribute a general container that is amenable to different databases and/or study identifiers). First, here is how you would specify a different studyid:

```
docker run -v /tmp/my-experiment/data/:/scif/data \
           -d -p 80:80 \
           expfactory/experiments  --studyid dns start
```

Here is how to specify a different database, like sqlite3


```
docker run -v /tmp/my-experiment/data/:/scif/data \
           -d -p 80:80 \
           expfactory/experiments  --database sqlite start
```


## Shell into your Container
It's important that you know how to shell into your container for interactive debugging, and 
general knowledge about Docker. First, open up a new terminal. As we did above, we used `docker ps`
to see our running container:

```
$ docker ps
CONTAINER ID        IMAGE                COMMAND                  CREATED             STATUS              PORTS                          NAMES
2c503ddf6a7a        vanessa/experiment   "/bin/bash /starts..."   10 minutes ago      Up 10 minutes       0.0.0.0:80->80/tcp, 5000/tcp   zealous_raman
```

The cool part is that it shows us what we already know - port 80 in the container is mapped to 80 on our local machine, and the application served at port 5000 is exposed. And it has QUITE a fantastic name (`zealous_raman`). Note that docker assigns these automatically, you could have easily added a `--name` argument to specify your own when you issued the run command. I like the fun of having a surprise name :)

To shell and work interactively in the image:

```
docker exec -it 2c503ddf6a7a bash
root@2c503ddf6a7a:/scif/apps# 
```

We shell into the `/scif/apps` directory - we are inside the container, with our installed experiments! Take a look!

```
$ ls
   tower-of-london
```

Here are the logs we were looking at:

```
$ ls /scif/logs
gunicorn-access.log  gunicorn.log
```

Importantly, our data is to be saved under `/scif/data`, which we would map to our local machine (so the generated data doesn't disappear when we remove the container)

```
ls /scif/data/
expfactory
```

Right now the folder is empty because we haven't had anyone do the experiment yet. Try navigating back to ([http://127.0.0.1](http://127.0.0.1)) in
your browser, and completing a round of the task. Here I am from outside the container. Remember I've mapped `/tmp/my-experiment/data` to `/scif/data` in the image. My study id is `expfactory` and the first participant has just finished:

```
$ ls data/expfactory/00000/
test-task-results.json
```

## Stopping your Container
For the first example that we did without detached (`-d`) if you pressed Control+C for the terminal with the container started, you will kill the process and remove the container. This would happen regardless if you were shelled in another container, because the start script exits. However, now that we have it running in this detached state, we need to stop it using the docker daemon:

```
docker stop 2c503ddf6a7a
```

I find that using the container identifier (alphanumeric string) that you find with `docker ps` works better than the name. I've seen inconsistent behavior between the two and I'm not sure why.

## Adding Experiments
While we encourage you to re-generate the file with the `vanessa/expfactory-builder` so generation of your
container is reproducible, it's possible to install experiments into your container after it's generated. You
should only do this for development, as changes that you make to your container that are not recorded in the Dockerfile
are not reproducible. Let's say that we have an experiment container that has one task, `tower-of-london`, and we want to install
`test-task` to it.

First let's create our container fresh, find the name, and shell into it:

```
$ docker run -p 80:80 vanessa/experiment start

# What's the name?
$ docker ps
9e256e1b1473        vanessa/experiment   "/bin/bash /starts..."   3 seconds ago       Up 2 seconds        0.0.0.0:80->80/tcp, 5000/tcp   vigorous_lovelace

# Let's shell inside!
docker exec -it 9e256e1b1473 bash
```

We can see the one experiment installed, it was the one in our Dockerfile:

```
$ docker exec -it vigorous_lovelace bash
root@9e256e1b1473:/scif/apps# ls
tower-of-london
```

Now let's install a new one! Remember we need to be in `/scif/apps` to install the experiment there. What was the Github 
url again? Let's ask...

```
expfactory list
Expfactory Version: 3.0
Experiments
1  adaptive-n-back	https://www.github.com/expfactory-experiments/adaptive-n-back
2  alcohol-drugs-survey	https://www.github.com/expfactory-experiments/alcohol-drugs-survey
3  breath-counting-task	https://www.github.com/expfactory-experiments/breath-counting-task
4  digit-span	https://www.github.com/expfactory-experiments/digit-span
5  dospert-eb-survey	https://www.github.com/expfactory-experiments/dospert-eb-survey
6  dospert-rp-survey	https://www.github.com/expfactory-experiments/dospert-rp-survey
7  dospert-rt-survey	https://www.github.com/expfactory-experiments/dospert-rt-survey
8  spatial-span	https://www.github.com/expfactory-experiments/spatial-span
9  test-task	https://www.github.com/expfactory-experiments/test-task
10 tower-of-london	https://www.github.com/expfactory-experiments/tower-of-london
```

Ah yes, let's install test-task:

```
$ expfactory install https://www.github.com/expfactory-experiments/test-task
Expfactory Version: 3.0
Cloning into '/tmp/tmp5xn6oc4v/test-task'...
remote: Counting objects: 62, done.
remote: Compressing objects: 100% (49/49), done.
remote: Total 62 (delta 20), reused 55 (delta 13), pack-reused 0
Unpacking objects: 100% (62/62), done.
Checking connectivity... done.
LOG Installing test-task to /scif/apps/test-task
LOG Preparing experiment routes...
```

Now you are probably navigating to your web interface at ([http://127.0.0.1](http://127.0.0.1)) and confused that the new experiment
isn't there. The easiest way to restart all the moving pieces is to (from outside the container) restart it. Let's exit, and do that.

```
$ exit
docker restart 9e256e1b1473
```

You then should have the new experiment installed in the container! Remember, you would want to go back and (properly) produce this:

```
docker run -v $PWD:/data vanessa/expfactory-builder build digit-span test-task 
```

## Summary
This is a quick preview of running a quick server with gunicorn, Flask, and Docker. While this implementation isn't
perfect for production, it will work reasonable well for a local lab that needs to run participants through a 
behavioral paradigm. Do you have a use case that warrants a different kind of database, experiment, or deployment? 
Please [get in touch](https://www.github.com/expfactory/issues) as I am looking to develop this.


# Custom Configuration
If you want more specificity to configure your container, you might want to customize the database or experiment variables. There are **two** kinds of customization, the customization that happens **before** you build the container (akin to setting defaults for future users of it) and the customization that happens at runtime (meaning defining the database type when you start the container).

If you change the defaults, this means that any users that run your container (without specifying these variables) will get these as default. If you want your container to be most usable by others, we recommend that you don't do this, and keep the defaults as the most flexible types - a flat file system database and general study id (expfactory). 

If you leave these defaults, you (and the future users of your container) can then easily customize these variables when the container is started in the future. The risk of setting a default database like `sql` or `postgres` is that a user that doesn't know some credential needs to be defined won't be able to use the container. 

The choice is up to you! For settings defaults, see the first section [default variables](#default-variables). For setting at runtime, see the second section [runtime variables](#runtime-variables).
 
## Default Variables
When you run a build with `vanessa/expfactory-builder` image, there are other command line options available pertaining to the database and study id. Try running `docker run vanessa/expfactory-builder build --help` to see usage. If you customize these variables, the container recipe generated will follow suit.

### database

**filesystem**
The default (simplest) method for a database is flat files, meaning that results are written to a mapped folder on the local machine, and each participant has their own results folder. This option is provided as many labs are accustomed to providing a battery locally, and want to save output directly to the filesystem without having any expertise with setting up a database. This argument doesn't need to be specified, but would coincide with:

```
docker run -v /tmp/my-experiment:/data \
              vanessa/expfactory-builder \
              build --database filesystem \
                      tower-of-london
```

**sqlite**
An sqlite database can be used instead of a flat filesytem. This will produce one file that you can move around and read with any standard scientific software (python, R) with functions to talk to sqlite databases. If you want to set a default for the container of sqlite3, then specify:

```
docker run -v /tmp/my-experiment:/data \
              vanessa/expfactory-builder \
              build --database sqlite \
                      tower-of-london
```

**sql**
For labs that wish to deploy the container on a server, you are encouraged to use a more substantial database, such as a traditional relational database like sql. To use sql, you need to specify the database type for the Dockerfile, and then you will need to...

#TODO: how to specify username and password? 

**MySQL/Postgres/Mongo/Other**
We haven't yet developed this, and if you are interested, please [file an issue](https://github.com/expfactory/expfactory).

For any of the above, if you generate a Dockerfile and then change your mind, you can easily edit the Dockerfile instead of re-generating with the builder. In fact, this applies to make **any changes** to the Dockerfile. You can clone your own repos not in the library, add different images, or change the templates.

## Identifiers

**studyid**
The Experiment Factory will generate a new unique ID for each participant with some study idenitifier prefix. The default is `expfactory`, meaning that my participants will be given identifiers `expfactory/0` through `expfactory/n`, and for a filesystem database, it will produce output files according to that schema:

```
 /scif/data/
      expfactory/
           00000/
            tower-of-london-result.json
```

To ask for a different study id:

```
docker run -v /tmp/my-experiment:/data \
              vanessa/expfactory-builder \
              build --studyid dns \
                      tower-of-london
```

**output**
You actually **don't** want to edit the recipe output file, since this happens inside the container
(and you map a folder of your choice to it.) The others, however, you can modify.


In the future, our [online recipe generator](https://expfactory.github.io/experiments/generate) will make it easy to specify all of these variables. We will add these later after getting [feedback from users like you](https://www.github.com/expfactory/expfactory/issues).

### Expfactory wants Your Feedback!
The customization process is very important, because it will mean allowing you to select variable stimuli, lengths, or anything to make a likely general experiment specific to your use case. To help with this, @vsoch is looking for feedback about:

 - what kind of experiments (those provided in the library? generated with a build tool?) do you want to use
 - what variables do you want to customize? Do you have preference for how you would want to go about this?
 - if there is a build, when and how does it happen?

A reasonable feature would be to have the experiment manifests capture variables that are "allowed" to be changed (e.g., a stimulus number or similar) and then exposing these options to the user at build time, likely with a simple configuration file. Currently, It's important to remember that your experiment to be truly reproducible, other than introducing planned randomness (e.g., presentation of stimuli) it shouldn't be the case that a lot of the experiment details are required to be set at runtime. They must be frozen into the container so that when a colleague tries to reproduce your study, the exact thing is used.

With this in mind, please [let us know](https://www.github.com/expfactory/expfactory/issues) your thoughts.

<div>
    <a href="/expfactory/"><button class="previous-button btn btn-primary"><i class="fa fa-chevron-left"></i> </button></a>
    <a href="/expfactory/usage.html"><button class="next-button btn btn-primary"><i class="fa fa-chevron-right"></i> </button></a>
</div><br>

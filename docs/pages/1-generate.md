---
layout: default
title: Generate your Experiment Container
pdf: true
permalink: /generate
toc: true
---


# Really Quick Start
Pull our pre-generated example containers, and start! Your experiment portal is at [http://127.0.0.1](http://127.0.0.1) in your browser.

```
docker run -p 80:80 vanessa/expfactory-experiments start
docker run -p 80:80 vanessa/expfactory-surveys start
docker run -p 80:80 vanessa/expfactory-games start
```

These [container recipes](/experiments/recipes) are derived from tags in our library. Feel free to use one for the examples below.

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

Let's build the container from the Dockerfile! We are going to name it `expfactory/experiments`

```
docker build -t expfactory/experiments .

```

Now let's start it.

```
docker run -v /tmp/my-experiment/data/:/scif/data \
           -d -p 80:80 \
           expfactory/experiments start 
```

Open your browser to localhost ([http://127.0.0.1](http://127.0.0.1)) to see the portal [portal](2-usage.md). For specifying a different database or study identifier, read the detailed start below, and then how to [customize your container runtime](#customize-your-container). When you are ready to run (and specify a particular database type) read [the usage docs](2-usage.md).


# Detailed Start
The generation of a container comes down to adding the experiments to a text file that records all the commands to generate your container. Since we are using Docker, this file will be the Dockerfile, and you should [install Docker](https://docs.docker.com/engine/installation/) first and be comfortable with the basic usage. In these sections, we will be building your container from a customized file. You will be doing the following:

 - generating a recipe with (reproducible) steps to build a custom container
 - building the container!

Note that if you want to deploy a container with https, you should read our [https generation](/expfactory/generate-https) page, and then come back here to read about [interaction with your container](/expfactory/generate#shell-into-your-container).


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

## Library Experiment Selection
The first we've already used, and it's the only required argument. We need to give the
expfactory builder a list of `experiments`. You can either [browse
the table](https://expfactory.github.io/experiments/) or see a current library list with `list.`
We also have some pre-generated commands in our [recipes portal](/experiments/recipes).
Here is how to list all the experiments in the library:

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

## Local Experiment Selection
If you have experiments on your local machine where an experiment is defined based on [these criteria](https://expfactory.github.io/expfactory/contribute.html#experiment-pre-reqs) or more briefly:

 - the config.json has all required fields
 - the folder is named according to the `exp_id`
 - the experiment runs via a main index.html file
 - on finish, it POSTS to `/save` and then proceeds to `/next`

Then you can treat a local path to an experiment folder as an experiment in the list to give to build. Since we will be working from a mapped folder in a Docker container, this comes down to providing the experiment name under the folder it is mapped to, `/data`. Continue reading for an example

## Recipe Generation
To generate a Dockerfile to build our custom image, we need to run expfactory in the container,
and mount a folder to write the Dockerfile. If we are installing local experiments, they should be in this folder. The folder
should not already contain a Dockerfile, and we recommend that you set this folder up with version control (a.k.a. Github). That looks like this:

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

If you are building from local experiment folders, then it is recommended to generate the Dockerfile in the same folder as your experiments. You should (we hope!) also have this directory under version control (it should have a `.git` folder, as shown in the example below). For example, let's say I am installing local experiment `test-task-two` under a version controlled directory `experiments`, along with `test-task` from the library. The structure would look like this:

```
experiments/
├── .git/
└── test-task-two
```

I would then mount the present working directory (`experiments`) to `/data` in the container, and give the build command both the path to the directory in the container `data/test-task-two` and the exp_id for `test-task`, which will be retrieved from Github.

```
docker run -v $PWD:/data \
              vanessa/expfactory-builder \
              build test-task \
                    /data/test-task-two

Expfactory Version: 3.0
local experiment /data/test-task-two found, validating...
LOG Recipe written to /data/Dockerfile
WARNING 1 local installs detected: build is not reproducible without experiment folders

To build, cd to directory with Dockerfile and:
              docker build -t expfactory/experiments .
```

Note that it gives you a warning about a local installation. This message is saying that if someone finds your Dockerfile without the rest of the content in the folder, it won't be buildable because it's not obtained from a version controlled repository (as the library experiments are). We can now see what was generated:

```
experiments/
├── .git/
├── Dockerfile
├── startscript.sh
└── test-task-two
```

This is really great! Now we can add the `Dockerfile` and `startscript.sh` to our repository, so even if we decide to not add our experiments to the official [library](https://expfactory.github.io/experiments/) others will still be able to build our container. We can also inspect the file to see the difference between a local install and a library install: 

```
########################################
# Experiments
########################################


LABEL EXPERIMENT_test-task /scif/apps/test-task
WORKDIR /scif/apps
RUN expfactory install https://www.github.com/expfactory-experiments/test-task

LABEL EXPERIMENT_test-task-two /scif/apps/test-task-two
ADD test-task-two /scif/apps/test-task-two
WORKDIR /scif/apps
RUN expfactory install test-task-two
```

The library install (top) clones from Github, and the local install adds the entire experiment from your folder first. This is why it's recommended to do the build where you develop your experiments. While you aren't required to and could do the following to build in `/tmp/another_base`:

```
docker run -v /tmp/another_base:/data \
              vanessa/expfactory-builder \
              build test-task /data/test-task-two
```

and your experiments will be copied fully there to still satisfy this condition, it is more redundant this way.

Finally, before you generate your recipe, in the case that you want "hard coded" defaults (e.g., set as defaults for future users) read the [custom build](#custom-conriguration) section below to learn about the variables that you can customize. If not, then rest assured that these values can be specified when a built container is started.

### Example: Repeated Measures Designs

A common scenario is an experiment where you use the same task multiple times.  For example, suppose you want to measure the 
effect of two different tasks on the [Attention Network Test (ANT)](https://github.com/expfactory-experiments/attention-network-task).  You want a container that runs a baseline ANT, one of the two tasks (hint: you can assign participants to each task using participant variables), and then runs the ANT for a second time.  Because each task requires a unique name, you can use local experiments to build a container that runs the ANT twice.

Generate your Dockerfile with the tasks that you want to run between the two ANT measurements.  Add the following lines to your Dockerfile to build the two ant tasks: 

```
LABEL EXPERIMENT_ant1 /scif/apps/ant1
ADD ant1 /scif/apps/ant1
WORKDIR /scif/apps
RUN expfactory install ant1

LABEL EXPERIMENT_ant1 /scif/apps/ant2
ADD ant2 /scif/apps/ant2
WORKDIR /scif/apps
RUN expfactory install ant2
```

Next, clone the repository into your build folder, and rename it:

```
$ git clone https://github.com/earcanal/attention-network-task
$ mv attention-network-task/ ant1
```

Set `exp_id` to match the folder name in `ant1/config.json`:

```
   "exp_id": "ant1",
```

Repeat this cloning/renaming process, giving the second folder the name `ant2`.

You can now build a container with two ANT tasks which you can run before and after your treatment tasks.  You can repeat this process as many times as you like in case you need more than two measurements from the same task/survey.

## Container Generation

Starting from the folder where we generated our Dockerfile, we can now build the experiment container. Note that when you have a production container you don't need to build locally each time, you can use an [automated build from a Github repository to Docker Hub](https://docs.docker.com/docker-hub/builds/) - this would mean that you can push to the repository and have the build done automatically, or that you can manually trigger it. For this tutorial, we will build locally:

```
experiments/
├── Dockerfile
└── startscript.sh

```

and if we have local experiments, we would see them as well:

```
experiments/
├── Dockerfile
├── startscript.sh
└── test-task-two/
```


At this point we recommend you add `LABELS` to your Dockerfile. A label can be any form of
metadata to describe the image. Look at the [label.schema](http://label-schema.org/rc1/) for
inspiration. Then build the image, and replace `expfactory/experiments` with whatever namespace/container you
want to give to the image. It's easy to remember to correspond to your Github repository (`username/reponame`).

```
docker build -t expfactory/experiments .

# if you don't want to use cache
docker build --no-cache -t expfactory/experiments .
```

Don't forget the `.` at the end! It references the present working directory with the Dockerfile. If you are developing and need to update your container, the fastest thing to do is to change files locally, and build again (and removing --no-cache should be OK).


## Start your Container
After you do the above steps, your custom container will exist on your local machine.
First, let's pretend we haven't a clue what it does, and just run it:

```
$ docker run expfactory/experiments

    Usage:
    
         docker run <container> [help|list|test-experiments|start]
         docker run -p 80:80 -v /tmp/data:/scif/data <container> start

         Commands:

                help: show help and exit
                list: list installed experiments
                lib: list experiments in the library
                test: test experiments installed in container
                start: start the container to do the experiments*
                env: search for an environment variable set in the container
         
         *you are required to map port 80, otherwise you won't see the portal at localhost

         Options [start]:

                --db: specify a database url to override the default filesystem
                                 [sqlite|mysql|postgresql]:///

                --studyid:  specify a studyid to override the default

         Examples:

              docker run <container> test
              docker run <container> list
              docker run <container> start
              docker run -p 80:80 <container> --database mysql+pymysql://username:password@host/dbname start
              docker run -p 80:80 <container> --database sqlite start
              docker run -p 80:80 <container> --database postgresql://username:password@host/dbname start

```

Note that you can list installed experiments with `list` and library experiments with `lib`.
The command we are interested in is `start`, and the important (Docker) arguments are the following:

- `port`: The `-p 80:80` is telling Docker to map port 80 (the nginx web server) in the container to port 80 on our local machine. If we don't do this, we won't see any experiments in the browser!
- `volumes`: The second command `-v` is telling Docker we want to see the output in the container at `/scif/data` to appear in the folder `/tmp/data` on our local machine. If you are just testing and don't care about saving or seeing data, you don't need to specify this.

For this first go, we aren't going to map the data folder. This way I can show you how to shell inside an interactive container.


**Without SSL**

Remember, the above is *without* SSL (https)! If you want to deploy an https container,
see [these docs](/expfactory/generate-https).

```
docker run -p 80:80 expfactory/experiments start

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

You can also use the name (in this example `zealous_raman`) to reference the container, or give it your own name with `--name` when you run it. For more details on how to customize your container, including the database and study id, see the [usage](/expfactory/usage.html) docs.


## Shell into your Container
It's important that you know how to shell into your container for interactive debugging, and 
general knowledge about Docker. First, open up a new terminal. As we did above, we used `docker ps`
to see our running container:

```
$ docker ps
CONTAINER ID        IMAGE                COMMAND                  CREATED             STATUS              PORTS                          NAMES
2c503ddf6a7a        vanessa/experiment   "/bin/bash /starts..."   10 minutes ago      Up 10 minutes       0.0.0.0:80->80/tcp, 5000/tcp   zealous_raman
```

The cool part is that it shows us what we already know - port 80 in the container is mapped to 80 on our local machine, and the application served at port 5000 is exposed. And it has QUITE a fantastic name (`zealous_raman`) because we didn't specify one with a `--name` argument.

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
gunicorn-access.log  gunicorn.log  expfactory.log
```

Importantly, our data is to be saved under `/scif/data`, which we would map to our local machine (so the generated data doesn't disappear when we remove the container).

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
For the first example that we did without detached (`-d`) if you pressed Control+C for the terminal with the container started, you will kill the process and stop the container. This would happen regardless if you were shelled in another container, because the start script exits. However, now that we have it running in this detached state, we need to stop it using the docker daemon, and don't forget to remove it:

```
docker stop 2c503ddf6a7a
docker rm 2c503ddf6a7a
```

You can also use the name.


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

If you have any questions about the above, or want more detail, please [get in touch](https://www.github.com/expfactory/issues) as I am looking to develop this.


Now that you are comfortable generating your container, check out how to [customize it](/expfactory/customize).

<div>
    <a href="/expfactory/background"><button class="previous-button btn btn-primary"><i class="fa fa-chevron-left"></i> </button></a>
    <a href="/expfactory/customize"><button class="next-button btn btn-primary"><i class="fa fa-chevron-right"></i> </button></a>
</div><br>

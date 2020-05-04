# Docker Builder

This is the expfactory builder image provided on Docker Hub to produce other Dockerfiles to generate custom experiment containers. **Note that updated versions of these docs are maintained at [expfactory](https://expfactory.github.io/generate).

To do a build, you will be doing the following:

 - generating a recipe with (reproducible) steps to build a custom container
 - building the container!


## The Expfactory Builder Image
Both of these steps start with the expfactory builder container. 
In [builder](Dockerfile) we've provided an image that will generate a Dockerfile,
and from it you can build your Docker image.  We don't build the image within the same 
container for the explicit purpose that you should keep a copy of the recipe
Dockerfile at hand. The basic usage is to run the image, and you will see output
from the expfactory build tool inside:

```
$ docker run quay.io/vanessa/expfactory-builder

Usage:
docker run quay.io/vanessa/expfactory-builder experiment-one experiment-two ...
Expfactory Version: 3.0
usage: expfactory build [-h] [--recipe] --output OUTPUT [--studyid STUDYID]
                        [--database {fllesystem}]
                        experiments [experiments ...]

positional arguments:
  experiments           experiments to build in image

optional arguments:
  -h, --help            show this help message and exit
  --recipe, -r          only generate a recipe
  --output OUTPUT, -o OUTPUT
                        output name for Singularity recipe
  --studyid STUDYID     study id for saving database
  --database {fllesystem}
                        database for application (default filesystem)
```

## Experiment Selection
The minimum requirement we need is a list of `experiments`. You can either [browse
the table](https://expfactory.github.io/experiments/) or see a current library list with `list.`

```
docker run quay.io/vanessa/expfactory-builder list

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
docker run quay.io/vanessa/expfactory-builder list | grep survey
2  alcohol-drugs-survey	https://www.github.com/expfactory-experiments/alcohol-drugs-survey
4  dospert-eb-survey	https://www.github.com/expfactory-experiments/dospert-eb-survey
5  dospert-rp-survey	https://www.github.com/expfactory-experiments/dospert-rp-survey
6  dospert-rt-survey	https://www.github.com/expfactory-experiments/dospert-rt-survey
```

## Recipe Generation
To generate a Dockerfile to build our custom image, we need to run expfactory in the container,
and mount a folder (`my-experiment`) to retrieve the image that is built. The folder
should not already container a Dockerfile, and most appropriate is a new folder that you
intend to set up with version control (a.k.a. Github). That looks like this:

```
mkdir -p /tmp/my-experiment
docker run -v /tmp/my-experiment:/data \
              quay.io/vanessa/expfactory-builder \
              build tower-of-london

Expfactory Version: 3.0
LOG Recipe written to /data/Dockerfile

To build, cd to recipe and:
              docker build -t expfactory/experiments .
```

## Container Generation
Now we would go to the folder (`/tmp/my-experiment`) to bulid our experiments container. We
could actually do this in the container for you, but it's better to generate the file first
(and generate for version control) than not. You have a Dockerfile and a script to run 
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
After you do the above steps, your custom container will exist on your local machine,
and you need just interact with it. To run the application (and **not save any data**), you can
just use run, and importantly, we need to map the web server port to our local machine,
otherwise it will be running and we won't see it. First, let's pretend we haven't a clue
what it does, and just run it:

```
docker run vanessa/experiment

Usage:
    docker run <container> [help|list|test-experiments|start]
    docker run -p 80:80 -v /tmp/data:/scif/data <container> start
```

The important command is the second - we want to start the server to run experiments. 

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
something like `http://127.0.0.1/experiments/tower-of-london`. Now try hitting "Control+C" in the terminal
where the server is running. You will see it exit. Refresh the browser, and see that the experiment is
gone too. What we actually want to do is run the server in `detached` mode. After you've Control+C, try adding
a `-d` to the original command. This means detached.


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
docker exec -it zealous_raman /bin/bash
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

Importantly, our data is to be saved under `/scif/data`

```
ls /scif/data/
expfactory
```

But the folder is empty because we haven't had anyone do the experiment yet. Try navigating back to ([http://127.0.0.1](http://127.0.0.1)) in
your browser, and completing a round of the task.


## Stopping your Container
For the first example that we did without detached (`-d`) if you pressed Control+C for the terminal with the container started, you will kill the process and remove the container. This would happen regardless if you were shelled in another container, because the start script exits. However, now we have it
running in this detached state, and we need to stop it using the docker daemon:

```
docker stop zealous_raman
```

or use the container identifier (alphanumeric string) that you find with `docker ps`. This was helpful for me
when I first didn't give an easy exit to running the gunicorn process.


## Adding Experiments
While we are working on a development workflow for you to install experiments interactively, for now we encourage you
to use the `quay.io/vanessa/expfactory-builder` image to generate Dockerfile to maximize reproducibility of your work. Each
change or command that you would do interactively breaks reproducibility!


### Under Development
**not ready for use**
While we encourage you to re-generate the file with the `quay.io/vanessa/expfactory-builder` so generation of your
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
docker exec -it vigorous_lovelace bash
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
docker restart vigorous_lovelace
```


## Summary
This is a quick preview of running a quick server with gunicorn, Flask, and Docker. While this implementation isn't
ideal for production, it will work reasonable well for a local lab that needs to run participants through a 
behavioral paradigm. Do you have a use case that warrants a different kind of database, experiment, or deployment? 
Please [get in touch](https://www.github.com/expfactory/issues) as I am looking to develop this.


## Building the Builder
Make sure that the branch that you want is cloned in the [Dockerfile](Dockerfile). Then cd to this directory and
build the image

```
docker build -t quay.io/vanessa/expfactory-builder .
```

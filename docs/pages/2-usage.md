---
layout: default
title: Usage
pdf: true
permalink: /usage
---

# Browsing Experiments

You don't need to build a container to browse experiments! If you'd prefer to run the software locally to browse experiments, and generate your custom recipe, you can easily install experiment factory and run it:

```
git clone https://www.github.com/expfactory/expfactory
cd expfactory && python setup.py install
```

to see available experiments, meaning they are provided in the [expfactory-experiments](https://www.github.com/expfactory/library) library, just type:

```
$ expfactory

Expfactory Version: 3.0
Experiments
1  adaptive-n-back	https://github.com/expfactory-experiments/adaptive-n-back.git
2  tower-of-london	https://github.com/expfactory-experiments/tower-of-london.git
3  test-task	https://www.github.com/expfactory-experiments/test-task
```

and you will see a list of the experiments available. If you want to grab one quickly to browse, you could easily just clone a repo address:

```
git clone https://github.com/expfactory-experiments/adaptive-n-back.git
```

or use the install command. It does the same thing, but validates the experiment as well.

```
expfactory install https://github.com/expfactory-experiments/adaptive-n-back.git
Expfactory Version: 3.0
Cloning into '/tmp/tmp3h9ug46k/adaptive-n-back'...
remote: Counting objects: 59, done.
remote: Compressing objects: 100% (47/47), done.
remote: Total 59 (delta 21), reused 49 (delta 11), pack-reused 0
Unpacking objects: 100% (59/59), done.
Checking connectivity... done.
LOG Installing adaptive-n-back to /tmp/adaptive-n-back
```
Cloning Github repos is only the start. We really need a full fledged container to run our experiments in a nice way, and preserve how they are setup if anyone wants to do it again. So next, you probably want to make your experiments container!


# Running your Experiment Container

Your container (or sandbox folder) is a file or folder sitting on your computer. When we run it, in order to give it it's own namespace to run a webserver, we are going to create an instance of it. This is [new functionality for Singularity 2.4](https://singularityware.github.io/docs-instances), and we are excited to make good use of it!

### Start/Stop the Server
We will be starting instances of the container, meaning a deployment of a web server with the expfactory software to serve a battery. This means first starting the container. In the command below, we use `instnace.start` and name our instance `web1`.

```
singularity instance.start expfactory.img web1
```

List your images:

```
singularity instance.list
DAEMON NAME      PID      CONTAINER IMAGE
web1             29903    /home/vanessa/Documents/Dropbox/Code/expfactory/experiments/expfactory
```

Stop the instance

```
singularity instance.stop web1
Stopping web1 instance of /home/vanessa/Documents/Dropbox/Code/expfactory/experiments/expfactory (PID=29903)
```

If you want a writable instance (meaning using shell with sudo) you need to also create it as sudo. The creator is the owner.

```
sudo singularity instance.start --writable expfactory web2
sudo singularity instance.start --writable expfactory web2
```


### Saving Data to the Host
When you want to run a battery and save data, you either need need a writable container or to mount a directory
on the host where you have writable. The expfactory container internal organization expects for you to mount some folder on your host to `/data`. When it finds this location is writable, it will save data. It's as easy as specifying the mount when you start the instance:

```
sudo singularity instance.start --bind /home/vanessa/data:/data expfactory/ web3
```

Now we can again list our instances, this time we have data And then list your instances

```
$ sudo singularity instance.list
DAEMON NAME      PID      CONTAINER IMAGE
web3             32708    /home/vanessa/Documents/Dropbox/Code/expfactory/experiments/expfactory
```

If you want to shell inside

```
sudo singularity shell --writable instance://web3
```

<br>
<div>
    <a href="/expfactory/generate.html"><button class="previous-button btn btn-primary"><i class="fa fa-chevron-left"></i> </button></a>
    <a href="/expfactory/contribute.html"><button class="next-button btn btn-primary"><i class="fa fa-chevron-right"></i> </button></a>
</div><br>

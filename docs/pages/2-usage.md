---
layout: default
title: Usage
pdf: true
permalink: /usage
---

# Using your Experiments Container
If you've just finished [generating your experiments container](/expfactory/generate.html) (whether a custom build or pull of an already existing container) then you are ready to use it! Here we will walk though:

 - inspecting a container instance
 - starting and stopping a container instance
 - running a participant through a selection of experiments


### Quick Start
The quick start commands are to pull the container, and start an instance, mounted to an existing directory on the host `/tmp/data` to write data output:

```
singularity pull --name expfactory.simg shub://expfactory/expfactory
singularity instance.start --bind /tmp/data:/scif/data expfactory.simg web1
```

More detailed notes are provided below.

### Container Inspection

What experiments are installed?

```
singularity apps expfactory.simg
    adaptive-n-back
    test-task
    tower-of-london
```

I forget the commands. Can I ask the container for help?  Try these commands on your local machine:

```
singularity help expfactory.simg

...

singularity inspect expfactory.simg

{
    "org.label-schema.usage.singularity.deffile.bootstrap": "docker",
    "org.label-schema.usage.singularity.deffile": "Singularity",
    "org.label-schema.usage": "/.singularity.d/runscript.help",
    "org.label-schema.schema-version": "1.0",
    "org.label-schema.usage.singularity.deffile.from": "ubuntu:14.04",
    "org.label-schema.build-date": "2017-11-06T20:42:28+00:00",
    "org.label-schema.usage.singularity.runscript.help": "/.singularity.d/runscript.help",
    "org.label-schema.usage.singularity.version": "2.4-feature-squashbuild-secbuild.g818b648",
    "org.label-schema.build-size": "545MB"
}
```

Importantly, any labels that you added to the `%labels` section of a custom recipe will appear here.

### Container Instances
You can think of the container like a template, and an "instance" as a full fledged running application that is generated based on the template. This means that you will want to start an instance of your container, which will carry it's own namespace and run the web server. The general commands that are important are to start and stop instances, we will use `singularity instance.start` and  `singularity instance.stop`. Importantly, you need to choose a folder on your local machine to put experiment data (`/tmp/data`), and bind it to the data folder in the instance (`/scif/data`). This means it will persist on our local machine even when the instance is stopped. You will also want to name your instance, we are calling it `web1`

```
mkdir -p /tmp/data
singularity instance.start --bind /tmp/data:/scif/data expfactory.simg web1
singularity instance.list
DAEMON NAME      PID      CONTAINER IMAGE
web1             22045    /home/vanessa/Desktop/expfactory.simg
```

Take note that when you interact with your instance, whether you start, stop, or a command specifically for an instance, you should refer to it by name:

```
singularity instance.stop web1
singularity instance.start web1
```

Also take note that the user that starts an instance is the owner. So if you start an instance as sudo and then run `singularity instance.list`, you won't see it.

If you are wanting to shell into your instance (`shell`) or execute a command to it (`exec`) you will need to tell Singularity that you are talking about an instance, and you can do this by using the `instance://` uri:


```
singularity shell instance://web1
singularity exec instance://web1 ls /opt/expfactory
```


### Saving Data to the Host
When you want to run a battery and save data, you either need need a writable container or to mount a directory
on the host where you have writable. The expfactory container internal organization expects for you to mount some folder on your host to `/scif/data`. When it finds this location is writable, it will save data. It's as easy as specifying the mount when you start the instance:

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

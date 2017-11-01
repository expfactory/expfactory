---
layout: default
title: Usage
pdf: true
permalink: /usage
---

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

---
layout: default
title: Development Tips
permalink: /development
pdf: true
---

# Development Quickstart

Build a development sandbox, create an instance, and shell inside:

```
sudo singularity build --sandbox [expfactory] Singularity
sudo singularity instance.start --writable --bind /tmp/data:/scif/data [expfactory] web1
sudo singularity shell --writable --bind /tmp/data:/scif/data instance://web1
```

Test an experiment in or outside of your container, either by cloning or using expfactory install:

```
git clone https://github.com/expfactory-experiments/adaptive-n-back.git /tmp

# or 

expfactory install https://github.com/expfactory-experiments/adaptive-n-back.git
Expfactory Version: 3.0
Cloning into '/tmp/tmp3h9ug46k/adaptive-n-back'...
...
LOG Installing adaptive-n-back to /tmp/adaptive-n-back
```

Start the webserver inside the container with gunicorn or expfactory, or locally with python
```
gunicorn --bind 0.0.0.0:5000 expfactory.wsgi:app
expfactory

# 
cd /tmp/adaptive-n-back
python -m http.server 9999
```

# Development Detailed

### Running Containers
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
```

### Build a Sandbox
Once you have your [Singularity](https://github.com/expfactory/expfactory/blob/master/Singularity) example recipe and a (mostly working) flask application, it's fairly simply to build an image. To develop, it's optimal to build a sandbox, and use sudo of course to have writable. Note that I'm in the same folder as the Singularity file, the root of the repository. Also note that I'm **not** calling my image expfactory, otherwise it would use the python base to dump the image. That would be bad.

```
sudo singularity build --sandbox [expfactory] Singularity
```

### Bring up an Instance
Once the image is built, you want to start it as an instance. Importantly, you want to be sure to bind a folder to write data on the host, and make the instance writable (to easily re-install the software, after you've changed something) if needed:

```
sudo singularity instance.start --writable --bind /tmp/data:/scif/data [expfactory] web1
```

To see your instance running:

```
sudo singularity instance.list
 sudo singularity instance.list
DAEMON NAME      PID      CONTAINER IMAGE
web1             22842    /home/vanessa/Documents/Dropbox/Code/expfactory/expfactory/[expfactory]
```

### Shell Inside the Instance
Remember that if you started the daemon as sudo, sudo owns it, and you need to use sudo to interact with it. When it comes time to run a container (as a user) the same applied. You should be able to go to the url `localhost` or `localhost:5000` and see the server running. If not, never fear! This is a good example of how to develop. Let's first shell inside. Note that we are shelling inside the instance (`instance://`) and we are also using `--writable` so we can change things, if necessary.

```
sudo singularity shell --writable --bind /tmp/data:/scif/data instance://web1
```

Note that you have to specify the bind **again**. If you forget to specify it at either time, it won't be bound. 


### Debugging
We could run the `expfactory` executable to open up the Flask development server, but since the application is far enough along it's a better idea to develop using something closer to the "production" server, with gunicorn. The general workflow is to do the following:


```
# install vim for quick changes / tests
apt-get install -y vim

# Start gunicorn
gunicorn --bind 0.0.0.0:5000 expfactory.wsgi:app
[2017-11-05 00:23:12 -0700] [479] [INFO] Starting gunicorn 19.7.1
[2017-11-05 00:23:12 -0700] [479] [INFO] Listening at: http://0.0.0.0:5000 (479)
[2017-11-05 00:23:12 -0700] [479] [INFO] Using worker: sync
[2017-11-05 00:23:12 -0700] [482] [INFO] Booting worker with pid: 482
```

Let's say that we tested something in the interface... and found a bug! We stop the server with Control +C. On our host we can tweak our cloned fork of the expfactory software, and then push. In the container we can then go to `/opt/expfactory` and pull from our remote branch (you will need to add it in the `.git/config`)

```
cd /opt/expfactory
git pull myremote master
```

Then you can install the software afresh, and restart the server with gunicorn, and then nginx. If you have experiments (previously) installed, you might need to issue the install command again.

```
python3 setup.py install
# install experiments
service nginx restart
```

### Moving from Development to Production
...or vice versa! You may have build a sandbox that you want to convert to an immutable image, or an immutable image that you want to keep editing. Do this at your own risk - any edits that aren't captured in the build recipe are not reproducible. You can however, move between the types easily:

```
sudo singularity build production.simg Singularity   # build production image from build recipe
sudo singularity build [sandbox] production.simg     # build sandbox (writable) from production
sudo singularity build production.v2.simg [sandbox]     # back to production (but changes not in build recipe)
```

This is an approach that can go in the other direction to - for example, you might start with a full experiment's container, and then want to re-generate your secret key every now and then.

<div>
    <a href="/expfactory/contribute.html"><button class="previous-button btn btn-primary"><i class="fa fa-chevron-left"></i> </button></a>
    <a href="/expfactory/"><button class="next-button btn btn-primary"><i class="fa fa-chevron-right"></i> </button></a>
</div><br>

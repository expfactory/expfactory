---
layout: default
title: Development Tips
permalink: /development
pdf: true
---

# Development

## Build a Sandbox
Once you have your [Singularity](https://github.com/expfactory/expfactory/blob/master/Singularity) example recipe and a (mostly working) flask application, it's fairly simply to build an image. To develop, it's optimal to build a sandbox, and use sudo of course to have writable. Note that I'm in the same folder as the Singularity file, the root of the repository. Also note that I'm **not** calling my image expfactory, otherwise it would use the python base to dump the image. That would be bad.

```
sudo singularity build --sandbox [expfactory] Singularity
```

## Bring up an Instance
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

## Shell Inside the Instance
Remember that if you started the daemon as sudo, sudo owns it, and you need to use sudo to interact with it. When it comes time to run a container (as a user) the same applied. You should be able to go to the url `localhost` or `localhost:5000` and see the server running. If not, never fear! This is a good example of how to develop. Let's first shell inside. Note that we are shelling inside the instance (`instance://`) and we are also using `--writable` so we can change things, if necessary.

```
sudo singularity shell --writable --bind /tmp/data:/scif/data --pwd /opt/expfactory instance://web1
```

Note that you have to specify the bind **again**. If you forget to specify it at either time, it won't be bound. It's also helpful to set the present working directory (`--pwd`) to be where our code base is.


## Debugging Flow
We could run the `expfactory` executable to open up the Flask development server, but since the application is far enough along it's a better idea to develop using something closer to the "production" server, with gunicorn. The general workflow is to do the following:


```
# install vim for quick changes / tests
apt-get install -y vim

# Work in the code base
cd /opt/expfactory # the code base

# Start gunicorn
gunicorn --bind 0.0.0.0:5000 expfactory.wsgi:app
[2017-11-05 00:23:12 -0700] [479] [INFO] Starting gunicorn 19.7.1
[2017-11-05 00:23:12 -0700] [479] [INFO] Listening at: http://0.0.0.0:5000 (479)
[2017-11-05 00:23:12 -0700] [479] [INFO] Using worker: sync
[2017-11-05 00:23:12 -0700] [482] [INFO] Booting worker with pid: 482

# Test something in the interface... find a bug! Stop the server with Control +C
# Make changes on the host, commit to Github, push to origin master
# then pull the updated changes in the container, restart the server with gunicorn
git pull origin master
python3 setup.py install
```

As an example, here is an error from when I was starting to develop. I tried running expfactory from `/opt` inside the container instance and got the following error:

```
Singularity expfac:~> expfactory
Traceback (most recent call last):
  File "/usr/local/bin/expfactory", line 9, in <module>
    load_entry_point('expfactory==3.0', 'console_scripts', 'expfactory')()
  File "/usr/local/lib/python3.4/dist-packages/expfactory-3.0-py3.4.egg/expfactory/cli.py", line 106, in main
    os.environ['EXPFACTORY_SUBID'] = args.subid
  File "/usr/lib/python3.4/os.py", line 638, in __setitem__
    value = self.encodevalue(value)
  File "/usr/lib/python3.4/os.py", line 706, in encode
    raise TypeError("str expected, not %s" % type(value).__name__)
TypeError: str expected, not NoneType

```

oh No! The default for the `sub_id` needs to be a string. We can edit the code (on our local machine) to fix it, then cd to where it is mounted, pull the changes and re-install. In the [Singularity](../Singularity) Recipe It's recommended to comment out the lines to start expfactory from the startscript, and then launch it manually. That way, you can Control+C to stop it.

```
cd /opt
python3 setup.py install
```

<div>
    <a href="/expfactory/contribute.html"><button class="previous-button btn btn-primary"><i class="fa fa-chevron-left"></i> </button></a>
    <a href="/expfactory/"><button class="next-button btn btn-primary"><i class="fa fa-chevron-right"></i> </button></a>
</div><br>

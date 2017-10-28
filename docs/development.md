# Development

Once you have your [Singularity](../Singularity) example recipe and a (mostly working) flask application, it's fairly simply to build an image. To develop, it's optimal to build a sandbox, and use sudo of course to have writable. Note that I'm in the same folder as the Singularity file, the root of the repository. Also note that I'm **not** calling my image expfactory, otherwise it would use the python base to dump the image. That would be bad.

```
sudo singularity build --sandbox [expfactory] Singularity
```

Once the image is built, you want to start it as an instance. Importantly, you want to be sure to bind the code base to a location in the image where you can easily re-install the software, after you've changed something.

```
sudo singularity instance.start --bind $PWD:/opt [expfactory] web1
```

If you are testing writing data, bind a folder to data for that too.

```
sudo singularity instance.start --bind $PWD:/opt --bind /tmp/data:/scif/data [expfactory] web1
```

You should be able to go to the url `localhost` or `localhost:5000` and see the server running. If not, never fear! This is a good example of how to develop. Let's first shell inside:

```
sudo singularity shell --writable --bind $PWD:/opt [expfactory]
```

Note that you have to specify the bind **again**. If you forget to specify it at either time, it won't be bound. Next, try running expfactory and get an error:

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

oh No! The default for the sub_id needs to be a string. We can edit the code (on our local machine) to fix it, then cd to where it is mounted and re-install.

```
cd /opt
python3 setup.py install
```

and since `/opt` is mounted at our code base on the host, we've just updated the software in the image. Easy!

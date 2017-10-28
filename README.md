# The Experiment Factory

The Experiment Factory is software to create a reproducible container that you can easily customize to deploy a set of web-based experiments. It's predecessor at [Expfactory.org](https://expfactory.org) was never able to open up to the public, and this went against the original goal of the software. Further, the badly needed functionality to serve a local battery was poorly met with [expfactory-python](https://www.github.com/expfactory/expfactory-python) as time progressed and dependencies changes.
 
This version is agnostic to the underlying driver of the experiments, and provides reproducible, instantly deployable "container" experiments. What does that mean?

 - You obtain (or build from scratch) one container, a battery of experiments.
 - You customize your battery
   - custom variables (e.g., a study identifier) and configurations go into the build recipe 
   - you can choose to use your own database (default output is flat files)
   - other options are available at runtime 
 - The container is a Singularity container, meaning that it's a file that can be easily moved, and shared.
 - You run the container, optionally specifying a subset and ordering


## Experiment Library
The experiments themselves are now maintained under [expfactory-experiments](https://www.github.com/expfactory-experiments), official submissions to be found by expfactory can be added to the [library](https://www.github.com/expfactory-experiments/library) to be tested for the minimum requirements:

 - an `index.html` file and `config.json` in the root of the folder.
 - (optional) documentation about any special variables that can be set in the Singularity build recipe environment section for it (more on this later).
 - an associated repository to clone from, (optionally) registered in the library.

- Please see our [documentation](http://expfactory.readthedocs.org/en/latest/getting-started.html) for more complete details.
- Jump in and [try out our experiments](http://expfactory.github.io/table.html)
- Express interest in Experiments as a Service (EaS) as [expfactory.org](http://www.expfactory.org)

The Experiment Factory code is licensed under the MIT open source license, which is a highly permissive license that places few limits upon reuse. This ensures that the code will be usable by the greatest number of researchers, in both academia and industry. 



## Quick start

You don't actually need to install the Software on your local machine, it will be installed into a container where your experiments live.

You do, however, need to install [Singularity](https://singularityware.github.io) on your local machine. This is a container technology akin to Docker, but it has support on most HPC clusters and works on old kernels, and Docker does not.


### Write your recipe
A Singularity Recipe is a file that details how you want your container to build. In our case, we want to give instructions about which experiments to install. First, copy an example recipe:


```
wget https://raw.githubusercontent.com/vsoch/expfactory-python/development/examples/Singularity
```

This will place the build recipe `Singularity` in your present working directory, and by fault we will install two experiments, adaptive-n-back and tower-of-london. The experiments each have their own repository maintained at [https://www.github.com/expfactory-experiments](https://www.github.com/expfactory-experiments).

If you look inside the recipe, you will see an "app" section for each experiment. All it does is clone the repository content:

```
git clone https://github.com/expfactory-experiments/adaptive-n-back
mv adaptive-n-back/* .
```

We are installing each experiment as a [Standard Container Integration Format (SCI-F)](https://containers-ftw.github.io/SCI-F/) app. The high level idea is that it gives easy accessibility to multiple different internal modules in our container. In our case, an internal module is an experiment. Note that here we might add different environment variables for an experiment, or specify a custom database, but since we are just developing and testing now, let's keep it simple! 


### Build the Battery Container
Let's build the image, and we are going to create a development (tester) image called a "sandbox" first:


```
sudo singularity build --sandbox expfactory Singularity
```

Let's break down the above. We are asking the singularity command line software to `build` an image, specifically a `--sandbox` (folder) kind for development, **from** the recipe file `Singularity`.

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


### Start the Server
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

or to bind a directory from the host (e.g., for writing a result)

```
sudo singularity instance.start --bind expfactory-python:/opt expfactory/ web1
```
And then list your instances

```
$ sudo singularity instance.list
DAEMON NAME      PID      CONTAINER IMAGE
web2             32708    /home/vanessa/Documents/Dropbox/Code/expfactory/experiments/expfactory
```

If you want to shell inside

```
sudo singularity shell --writable instance://web1
```



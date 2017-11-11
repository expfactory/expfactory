y# Docker Builder
In [builder](Dockerfile) we've provided an image that will generate a Dockerfile,
and from it you can build your Docker image.  We don't build the image within the same 
container for the explicit purpose that you should keep a copy of the recipe
Dockerfile at hand. The basic usage is to run the image, and you will see output
from the expfactory build tool inside:

```
$ docker run vanessa/expfactory-builder

Usage:
docker run vanessa/expfactory-builder experiment-one experiment-two ...
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

The minimum requirement we need is a list of `experiments`. You can either [browse
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

To generate a Dockerfile to build our custom image, we need to run expfactory in the container,
and mount a folder (`my-experiment`) to retrieve the image that is built. The folder
should not already container a Dockerfile, and most appropriate is a new folder that you
intend to set up with version control (a.k.a. Github). That looks like this:

```
mkdir -p /tmp/my-experiment
docker run -v /tmp/my-experiment:/data \
              vanessa/expfactory-builder \
              tower-of-london
```

To shell and work interactively in the image:

```
docker run --entrypoint /bin/bash -it vanessa/expfactory-builder
```

Note that I'm making two volumes, and the second is to make sure that my present working
directory is bound to `/data` in the container. The last line is my list of experiments.



To generate a recipe, but not ask it to build the image, we would add the `--recipe`
flag. We would also mount the container's data directory to our machine so that 
we can keep the final recipe.

```
docker run --volume vanessa/expfactory-builder --recipe tower-of-london
```

docker run \
-v /var/run/docker.sock:/var/run/docker.sock \
-v D:\host\path\where\to\output\singularity\image:/output \
--privileged -t --rm \
singularityware/docker2singularity \
ubuntu:14.04


This image is provided on Docker Hub so you shouldn't need to
build it, but if you need to:

```
docker build -t vanessa/expfactory-builder .
```

# Docker Builder (Development)

This is the expfactory builder image provided on Docker Hub for development production of other Dockerfiles to generate custom experiment containers. This image is updated with development versions that are eventually merged into the [main builder](../builder).

To do a build, you will be doing the following:

 - generating a recipe with (reproducible) steps to build a custom container
 - building the container!


## Building the Builder
Make sure that the branch that you want is cloned in the [Dockerfile](Dockerfile). Then cd to this directory and
build the image

```
docker build -t quay.io/vanessa/expfactory-builder-dev .
docker push quay.io/vanessa/expfactory-builder-dev
```

Follow instructions in the [main builder](../builder) README for using the builder. If you have questions please [get in touch](https://www.github.com/expfactory/issues).

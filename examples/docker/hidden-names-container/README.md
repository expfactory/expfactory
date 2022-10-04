# Hidden Experiment Names Container

This is how this was generated

```console
docker run -v $PWD:/data quay.io/vanessa/expfactory-builder build digit-span spatial-span tower-of-london test-task
```

And then I added this envar to say I want my experiment names concealed:

```bash
ENV EXPFACTORY_CONCEAL_NAMES=true
```

Then we can build!

```console
docker build -t vanessa/experiment .
```

This container recipe was generated with the commands shown in [the generate docs](https://expfactory.github.io/generate).  See them for building and usage.

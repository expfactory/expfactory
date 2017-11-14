# Experiments Container

This container recipe was generated with the [expfactory-generate.sh](expfactory-generate.sh) script provided via the [online generator](https://expfactory.github.io/experiments/r/survey/#), based on having the tag of "survey."

The generation comes down to the following:

- List experiments : docker run vanessa/expfactory-builder list
- Options          : docker run vanessa/expfactory-builder build --help
- Make Dockerfile  : docker run -v /tmp/my-experiment:/data vanessa/expfactory-builder build [experiment1 .. experimentn]
- Build Dockerfile : docker build -t vanessa/survey .
- Run container    : docker run -v /tmp/data:/scif/data -p 80:80 vanessa/survey start

We can start with the third, given that we don't need any custom options, and we already know the list of experiments from the library that we want. The build command is just listing the experiments:

```
docker run -v $PWD:/data vanessa/expfactory-builder build  alcohol-drugs-survey  bis-bas-survey  bis11-survey  brief-self-control-survey  cognitive-reflection-survey  demographics-survey  dickman-survey  dospert-eb-survey  dospert-rp-survey  dospert-rt-survey  eating-survey  erq-survey  five-facet-mindfulness-survey  future-time-perspective-survey  grit-scale-survey  holt-laury-survey  impulsive-venture-survey  k6-survey  leisure-time-activity-survey  mindful-attention-awareness-survey  mpq-control-survey  selection-optimization-compensation-survey  self-regulation-survey  sensation-seeking-survey  state-mindfulness-survey  ten-item-personality-survey  theories-of-willpower-survey  time-perspective-survey  treatment-self-regulation-survey  upps-impulsivity-survey 
```

And for this container, I pushed it to Docker Hub so it can be used:

```
docker run -p 80:80 -v /tmp/data:/data vanessa/expfactory-surveys start
```


See [the generate docs](https://expfactory.github.io/expfactory/generate.html) for more details.

## Development
Here is the push command, mostly for my future reference.

```
docker push vanessa/expfactory-surveys
```


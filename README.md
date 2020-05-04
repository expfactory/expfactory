# The Experiment Factory

[![DOI](http://joss.theoj.org/papers/10.21105/joss.00521/status.svg)](https://doi.org/10.21105/joss.00521)
[![DOI](https://zenodo.org/badge/108672186.svg)](https://zenodo.org/badge/latestdoi/108672186)
[![Gitter chat](https://badges.gitter.im/gitterHQ/gitter.png)](https://gitter.im/expfactory/lobby)

![expfactory/static/img/expfactoryticketyellow.png](expfactory/static/img/expfactoryticketyellow.png)

See our [documentation](https://expfactory.github.io) for getting started. If you are new to containers, read our [background](https://expfactory.github.io/generate#background) or [paper](paper) first. If you want a more guided entry, see the [detailed start](https://expfactory.github.io/generate#detailed-start)

The Experiment Factory is software to create a reproducible container that you can easily customize to deploy a set of web-based experiments. 

## Citation
If the Experiment Factory is useful to you, please cite [the paper](https://doi.org/10.21105/joss.00521) to support the software and open source development.

```
Sochat, (2018). The Experiment Factory: Reproducible Experiment Containers. Journal of Open Source Software, 3(22), 521, https://doi.org/10.21105/joss.00521
```

## Contributing
We have many ways to contribute, and will briefly provide resources here to get you started.

### How to Contribute
If you are a developer interested in working on the Experiment Factory software you should read out [contributing guidelines](.github/CONTRIBUTING.md) for details. For contributing containers and experiments, see our [user documentation](https://expfactory.github.io/contribute). If you have any questions, please don't hesitate to [ask a question](https://www.github.com/expfactory/expfactory/issues). You'll need to lint your code using black:

```bash
$ pip install black
$ black expfactory --exclude template.py
```

### Code of Conduct
It's important to treat one another with respect, and maintain a fun and respectful environment for the open source community. Toward this aim, we ask that you review our [code of conduct](.github/CODE_OF_CONDUCT.md)

## Background
It's predecessor at [Expfactory.org](https://expfactory.org) was never able to open up to the public, and this went against the original goal of the software. Further, the badly needed functionality to serve a local battery was poorly met with [expfactory-python](https://www.github.com/expfactory-python) as time progressed and dependencies changes.
 
This version is agnostic to the underlying driver of the experiments, and provides reproducible, instantly deployable "container" experiments. What does that mean?

 - You obtain (or build) one container, a battery of experiments.
 - You (optionally) customize it
   - custom variables (e.g., a study identifier) and configurations go into the build recipe 
   - you can choose to use your own database (default output is flat files)
   - other options are available at runtime 
 - The container can be easily shared.
 - You run the container, optionally specifying a subset and ordering, and collect your results
 
If you build on [Docker Hub](https://hub.docker.com/) anyone else can then pull and use your exact container to collect their own results. It is exact down to the file hash. Note
that bases for expfactory were initially provided on [Docker Hub](https://hub.docker.com/r/vanessa/expfactory-builder/tags) and have moved to [Quay.io](https://quay.io/repository/vanessa/expfactory-builder?tab=tags). Dockerfiles in the repository that use the expfactory-builder are
also updated. If you need a previous version, please see the tags on the original Docker Hub.

## Experiment Library
The experiments themselves are now maintained under [expfactory-experiments](https://www.github.com/expfactory-experiments), official submissions to be found by expfactory can be added to the [library](https://www.github.com/expfactory/library) (under development) to be tested that they meet minimum requirements.

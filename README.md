# The Experiment Factory

[![DOI](https://zenodo.org/badge/108672186.svg)](https://zenodo.org/badge/latestdoi/108672186)

![expfactory/static/img/expfactoryticketyellow.png](expfactory/static/img/expfactoryticketyellow.png)

[documentation](https://expfactory.github.io/expfactory)

The Experiment Factory is software to create a reproducible container that you can easily customize to deploy a set of web-based experiments. 

## Contributing
We have many ways to contribute, and will nriefly provide resources here to get you started.

### How to Contribute
If you are a developer interested in working on the Experiment Factory software you should read out [contributing guidelines](.github/CONTRIBUTING.md) for details. For contributing containers and experiments, see our [user documentation](https://expfactory.github.io/expfactory/contribute). If you have any questions, please don't hesitate to [ask a question](https://www.github.com/expfactory/expfactory/issues).

### Code of Conduct
It's important to treat one another with respect and maintain a fun and respectful environment for the open source community. Toward this aim, we ask that you review our [code of conduct](.github/CODE_OF_CONDUCT.md)

## Background
It's predecessor at [Expfactory.org](https://expfactory.org) was never able to open up to the public, and this went against the original goal of the software. Further, the badly needed functionality to serve a local battery was poorly met with [expfactory-python](https://www.github.com/expfactory/expfactory-python) as time progressed and dependencies changes.
 
This version is agnostic to the underlying driver of the experiments, and provides reproducible, instantly deployable "container" experiments. What does that mean?

 - You obtain (or build) one container, a battery of experiments.
 - You (optionally) customize it
   - custom variables (e.g., a study identifier) and configurations go into the build recipe 
   - you can choose to use your own database (default output is flat files)
   - other options are available at runtime 
 - The container is a Singularity container, meaning that it's a file that can be easily moved, and shared.
 - You run the container, optionally specifying a subset and ordering, and collect your results
 
If you build on [Singularity Hub](https://www.singularity-hub.org) anyone else can then pull and use your exact container to collect their own results. It is exact down to the file hash.

## Experiment Library
The experiments themselves are now maintained under [expfactory-experiments](https://www.github.com/expfactory-experiments), official submissions to be found by expfactory can be added to the [library](https://www.github.com/expfactory/library) (under development) to be tested that they meet minimum requirements.

# Existing Data

This will test existing data. You should first build the container.

```bash
$ docker build -t vanessa/experiment .
```

The existing participant data is already on the filesystem at [data](data).

```bash
$ docker run -it -p 80:80 -v $PWD/data:/scif/data vanessa/experiment start --headless
```

In the interface, try entering tokens for each of:

```bash
data/
└── expfactory
    ├── 027025c5-0f51-4158-8c70-3d4ea56fda76
    │   ├── general-self-efficacy-survey-results.json
    │   └── grit-scale-survey-results.json
    └── 0d3b978d-e779-4b8b-8eb3-7ce483365b54
        └── general-self-efficacy-survey-results.json
      
```

For `027025c5-0f51-4158-8c70-3d4ea56fda76` it should say it is finished, and the folder
should be renamed to have a finished suffix. For the other, you should be prompted to take
the git scale survey.

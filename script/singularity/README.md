# Singularity Images
These images are provided as examples and testing bases for the Experiment Factory

## Singularity.test
This is a container intended to help test experiments and contributions.

 - an **experiment** is a single folder with static content to serve an experiment. Usually
this means an `index.html` file and associated style (css) and javascript (js). For the
experiment factory, a valid experiment is required to have a config.json file. 
 - a **contribution** is a markdown file intended to be added to the `_library` folder.
You can just as easily install the Experiment Factory locally, however to make things
easier we provide the test wrapped in a container so you don't need to.

### Build Testing Image
To test an experiment or contribution, you can first build the image:

```
sudo singularity build expfactory.test Singularity.test
```

What tests are included?

```
singularity apps expfactory.test
test-experiment
test-contribution
``` 

You can ask for help for either with `singularity help --app <appname>`

### Test an Experiment
If you run without binding your folder with the experiment, you will get an error message:

```
singularity run --app test-experiment expfactory.test 
You must use --bind to bind the folder with config.json to /scif/data in the image.
```


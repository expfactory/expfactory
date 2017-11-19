---
layout: default
title: Usage
pdf: true
permalink: /usage
---

# Using your Experiments Container
If you've just finished [generating your experiments container](/expfactory/generate.html) (whether a custom build or pull of an already existing container) then you are ready to use it! Here we assume that the container is running, and will look quickly at the experience of running a participant through a selection of experiments. If you remember, we generated and started our container, and mapped it to port 80 on our machine.

```
docker run -p 80:80 vanessa/expfactory-experiments start
```

The above assumes that either we don't want to see files on the host, **or** if the image default is to save to a relational database external to the experiments container itself, we access data by querying this separate endpoint. For a filesystem or sqlite database, since the file is stored inside the container and we want access to it, we likely started with the location mapped:

```
docker run -p 80:80 -v /tmp/data:/scif/data vanessa/expfactory-experiments start
```

First, let's discuss the portal - what you see when you go to [127.0.0.1](http://127.0.0.1).

## The Experiment Factory Portal
When you start your container instance, browsing to your localhost will show the entrypoint, a user portal that lists all experiments installed in the container:

<div>
    <img src="/expfactory/img/generate/portal.png"><br>
</div>


This is where the experiment administrator would select one or more experiments, either with the single large checkbox ("select all") or smaller individual checkboxes. When you make a selection, the estimated time and exeperiment count on the bottom of the page are adjusted. 

<div>
    <img src="/expfactory/img/generate/selected.png"><br>
</div>

You can make a selection and then start your session. I would recommend the `test-task` as a first try, because it finishes quickly. When you click on `proceed` you can (optionally) enter a subject name:

<div>
    <img src="/expfactory/img/generate/proceed.png"><br>
</div>

This name is currently is only used to say hello to the participant. The actual experiment identifier is based on a study id defined in the build recipe.  After proceeding, there is a default "consent" screen that you must agree to (or disagree to return to the portal):

<div>
    <img src="/expfactory/img/generate/welcome.png"><br>
</div>


Once the session is started, the user is guided through each experiment (with random selection) until no more are remaining.

<div>
    <img src="/expfactory/img/generate/preview.png"><br>
</div>


When you finish, you will see a "congratulations" screen

<div>
    <img src="/expfactory/img/generate/finish.png"><br>
</div>

Generally, when you administer a battery of experiments you want to ensure that:

 - if a database isn't external to the container, the folder is mapped (or the container kept running to retrieve results from) otherwise you will lose the results.
 - if the container is being served on a server open to the world, you have added proper authorization (note this isn't developed yet, please file an issue if you need this)
 - you have fully tested data collection and inspected the results before administering any kind of "production" battery.


# Results 
Now let's discuss what happens after participants interact with the portal. We have results!

## Databases

### filesystem

**Where is the data?**
If you are saving data to the filesystem (`filesystem` database), given that you've mounted the container data folder `/scif/data` to the host, this means that the data will be found on the host in that location:

```
$ tree /tmp/data/expfactory/00001/

    /tmp/data/expfactory/00001/
       └── tower-of-london-results.json

0 directories, 1 file
```

If we had changed our studyid to something else (e.g., `dns`), we might see:

```
$ tree /tmp/data/dns/00001/

    /tmp/data/dns/00001/
       └── tower-of-london-results.json

0 directories, 1 file
```

If you stop the container, and the data will persist on the host. If you didn't mount to the host, then stopping the container means losing the data.

**How do I read it?**
For detailed information about how to read json strings (whether from file or database) see below. For a filesystem save, the data is saved to a json object, regardless of the string output produced by the experiment. This means that you can load the data as json, and then look at the `data` key to find the result saved by the particular experiment. Typically you will find another string saved as json, but it could be the case that some experiments do this differently.


## sqlite3
Using a sqlite3 database (`sqlite` database) means that you will also have a file database that needs to be mounted to the host, but instead of individual json files, you will find a single sqlite3 file named by the study id. This is more of a "substantial" database than a flat file, but still not ideal for any kind of production server. For example, here is my sqlite3 database under `/scif/data`:

```
ls /scif/data
    expfactory.db
```

**How do I read it?**
You can generally use any scientific programming software that has libraries for interacting with sqlite3 databases. My preference is for the [sqlite3](http://www.sqlitetutorial.net/sqlite-python/sqlite-python-select/) library, and we might read the file like this (in python):

```
import sqlite3
conn = sqlite3.connect('/scif/data/expfactory.db')

cur = conn.cursor()
cur.execute("SELECT * FROM result")
results = cur.fetchall()

for row in results:
    print(row)
```

Each result row includes the table row id, the date, result content, and participant id.

```
>>> res[0]  # table result row index
1

>>> res[1]  # date
'2017-11-18 17:26:30'

>>> res[2]  # data from experiment, json.loads needed
>>> json.loads(res[2])
[{ 
   'timing_post_trial': 100, 
   'exp_id': 'test-task', 
   'block_duration': 2000, 
   'trial_index': 0,
    ...

   'key_press': 13,
   'trial_index': 5,
   'rt': 1083, 
   'full_screen': True,
   'block_duration': 1083, 
   'time_elapsed': 14579
}]

>>> res[3] # experiment id (exp_id)
'test-task'

>>> res[4] # participant id
7
```

Since the Participant table doesn't hold anything beyond the participant id, you shouldn't need to query it. More detail is added for loading json in (see [loading results](#loading-results)) below.


## Loading Results
Whether you find your json objects in a file (`filesystem`) or saved in a text field in a relational database (`sqlite`) you will reach some point where you have a bunch of json objects to parse to work with your data. Json means "JavaScript Object Notation," and natively is found in browsers (with JavaScript, of course). It's flexibility in structure (it's not a relational database) makes it well suited to saving experiments with many different organizations of results. This also makes it more challenging for you, the researcher, given that you have to parse many experiments with different formats. Generally, experiments that use the same paradigm (e.g., jspsych or phaser) will have similar structures, and we can show you easily how to read JSON into different programming languages. Here is python:

```python
# python

import json

with open('test-task-results.json','r') as filey:
    content = json.load(filey)

# What are the keys of the dictionary?
content.keys()
dict_keys(['data'])
```

You are probably expecting another dictionary object under data. However, we can't be sure that every experiment will want to save data in JSON. For this reason, the key under `data` is actually a string:


```
type(content['data'])
str
```

And since we know jspsych saves json, it's fairly easy to load the string to get the final dictionary:

```
result = json.loads(content['data'])
```

Now our result is a list, each a json object for one timepoint in the experiment:

```
result[0]
{'focus_shifts': 0,
 'internal_node_id': '0.0-0.0-0.0',
 'full_screen': True,
 'key_press': 13,
 'exp_id': 'tower-of-london',
 'time_elapsed': 1047,
 'trial_index': 0,
 'trial_type': 'poldrack-text',
 'trial_id': 'instruction',
 'timing_post_trial': 0,
 'rt': 1042,
 'text': '<div class = centerbox><p class = center-block-text>Welcome to the experiment. This experiment will take about 5 minutes. Press <strong>enter</strong> to begin.</p></div>',
 'block_duration': 1042}
```

My preference is to parse the result like this, but if you prefer data frames, one trick I like to do is to use [pandas](https://pandas.pydata.org/) to easily turn a list of (one level) dictionary into a dataframe, and then you can save to tab delimited file (.tsv).

```
import pandas

df = pandas.DataFrame.from_dict(result)
df.to_csv('tower-of-london-result.tsv', sep="\t")
```

You should generally use a delimiter like tab, as it's commonly the case that fields have commas and quotes (so a subsequent read will not maintain the original structure).


### Feedback Wanted!
A few questions for you!

 - Would password protection of the portal be desired?
 - Is a user allowed to redo an experiment? Meaning, if a session is started and the data is written (and the experiment done again) is it over-written? 
 - Is some higher level mechanism for generating user ids in advance, and then validating them with an individual, desired?

To best develop the software for different deployment, it's important to discuss these issues. Please [post an issue](https://www.github.com/expfactory/expfactory/issues) to give feedback.


<br>
<div>
    <a href="/expfactory/generate.html"><button class="previous-button btn btn-primary"><i class="fa fa-chevron-left"></i> </button></a>
    <a href="/expfactory/contribute.html"><button class="next-button btn btn-primary"><i class="fa fa-chevron-right"></i> </button></a>
</div><br>

---
layout: default
title: Usage
pdf: true
permalink: /usage
---

# Using your Experiments Container
If you've just finished [generating your experiments container](/expfactory/generate.html) (whether a custom build or pull of an already existing container) then you are ready to use it! 

Below, we will summarize the variables that can be set at runtime:

| Variable        | Description           | Default  |
| ------------- |:-------------:| -----:|
| database      | the database to store response data | filesystem |
| randomize     | present the experiments in random order  |  flag | 
| no-randomize  | manually select the order of experiments  |  flag | 
| experiments  | comma separated list of experiments to expose |  [] | 
| studyid | set the studyid at runtime  |  expfactory |



## Start the Container
The first thing you should do is start the container. The variables listed above can be set when you do this. It's most likely the case that your container's default is to save data to the file system, and use a study id of expfactory. This coincides to running with no extra arguments, but perhaps mapping the data folder:

```
docker run -v /tmp/my-experiment/data/:/scif/data \
           -d -p 80:80 \
           expfactory/experiments start
```

Here is how you would specify a different studyid. The study id is only used for a folder name (in the case of a fileystem save) or an sqlite database name (for sqlite3 database):

```
docker run -v /tmp/my-experiment/data/:/scif/data \
           -d -p 80:80 \
           expfactory/experiments  --studyid dns start
```

Here is how to specify a different database, like sqlite

```
docker run -v /tmp/my-experiment/data/:/scif/data \
           -d -p 80:80 \
           expfactory/experiments  --database sqlite start
```

Here is how to limit the experiments exposed in the portal. For example, you may have 30 installed in the container, but only want to reveal 3 for a session:

```
docker run -v /tmp/my-experiment/data/:/scif/data \
           -d -p 80:80 \
           expfactory/experiments  --experiments test-test,tower-of-london start
```

## Start a Headless Experiment Container
"Headless" refers to the idea that you going to be running your experiment with remote participants, and you will need to send them to a different portal that has them login first. In order to do this, you need to start the container with the `--headless` flag, and then issue a command to pre-generate these users.

First we can start the container (notice that we are giving it a name to easily reference it by) with `--headless` mode.

```
docker run -p 80:80 -d --name experiments -v /tmp/data:/scif/data <container> --headless start
4f6826329e9e366c4d2fb56d64956f599861d1f0439d39d7bcacece3e88c7473
```

If we go to the portal at [127.0.0.1](http://127.0.0.1) we will see a different entrypoint, one that requires a token.

<div>
    <img src="../img/headless/portal.png"><br>
</div>

### Generate tokens
A "token" is basically a subject id that is intended to be used once, and can be sent securely to your participants to access the experiments. You will need to generate them, and we can use `exec` to execute a command to the container to do this. If we just run the general users command, we learn better how to use it:

```
docker exec experiments expfactory users
Specify number of new users:
	expfactory users --new 1
```

Let's try creating three users:

```
docker exec experiments expfactory users --new 3
FOLDER	TOKEN
/scif/data/expfactory/c4f58f85-bda0-47ee-9625-e6f70c3459e6	c4f58f85-bda0-47ee-9625-e6f70c3459e6
/scif/data/expfactory/c058ac0d-9c0a-426c-b646-3b2f29abf555	c058ac0d-9c0a-426c-b646-3b2f29abf555
/scif/data/expfactory/c65978e2-c5ce-41ff-92c8-d16edc499444	c65978e2-c5ce-41ff-92c8-d16edc499444
```

The result here will depend on the database type. The above shows a filesystem save, so a `FOLDER` is included, and remember this is internal to the container, so you might have `/scif/data` mapped to a different folder on your host. A relational database would just show the `TOKEN`. You can copy paste this from the terminal, or pipe into a file instead:

```
docker exec experiments expfactory users --new 3 >> participants.tsv
```

If you ever need to list the tokens you've generated, you can use the `users --list` command. Be careful that you specify the kind of database if you have changed from the default. In the example below, we list users saved as folders on the filesystem, and note that the command can be used for headless (token-named) users as well as traditional.

```
 expfactory users --list
DATABASE	TOKEN
/scif/data/expfactory/398f9f05-2f85-462b-8042-1b020b9c006a	398f9f05-2f85-462b-8042-1b020b9c006a
/scif/data/expfactory/50d49c45-2ca9-4797-a8e6-df41921e5ee4	50d49c45-2ca9-4797-a8e6-df41921e5ee4
/scif/data/expfactory/513ac67c-1fb5-4323-a1f0-7484c719a92c	513ac67c-1fb5-4323-a1f0-7484c719a92c

 expfactory users --list
DATABASE	TOKEN
/scif/data/expfactory/00000	00000
/scif/data/expfactory/00001	00001
/scif/data/expfactory/00002	00002
``` 

If we were to list a relational database, we would see the database index in the `DATABASE` column instead:

```
expfactory users --list
DATABASE	TOKEN
6	a2d266f7-52a5-497b-9b85-1e98febef6dc
7	a98e63c4-2ed1-4de4-a315-a9291502dd26
8	f524e1cc-6841-4417-9529-80874cf30b74
```
**Important** remember that the token is not the participant id, as it will be cleared when the participant finished the experiments. In the example above, we would care about matching the `DATABASE` id to the participant.


### Use tokens
It's up to you to maintain the linking of anonymous tokens to actual participants. What you would do is issue a token to each participant, and have him or her enter it into the web interface.

<div>
    <img src="../img/headless/enter-token.png"><br>
</div>


And of course it follows that if you enter a bad token, you cannot enter.

<div>
    <img src="../img/headless/bad-token.png"><br>
</div>

Once entry is given, the user can continue normally to complete the experiments in the protocol.


### Pre-set Experiments
For a headless experiment, you don't have the web interface to filter experiments in advance, or as for random (or not random) ordering. By default, not giving the `--experiments` argument will serve all experiments found installed in the container. If you want to limit to a smaller subset, do that with the experiments argument:

```
docker run -p 80:80 -d \
           --name experiments \ 
           -v /tmp/data:/scif/data <container> --experiments tower-of-london,test-task --headless start
```

and if you want the order typed to be maintained (and not random) add the `--no-randomize` flag.


```
docker run -p 80:80 -d \
           --name experiments \ 
           -v /tmp/data:/scif/data <container> --experiments tower-of-london,test-task --headless --no-randomize start
```

## User Management
The flow for a user session is the following:

**Headless**
 - You generate an id and token for the user in advance
 - The user starts and completes the experiments with the token associated with the id
 - The token is revoked upon finish, meaning that the user cannot go back without you refreshing it.

**Interactive**
 - The user is issued an id upon starting the experiment, without a token
 - When the user finishes, `_finished` is appended to the session folder, and so restarting the session will create a new folder.
 - If the user is revoked, the folder is appended with `_revoked`

This ensures that a participant, under headless mode, cannot go back and retake the experiments. If you want to allow him or her to do so, then you need to generate a new token. You can use these methods to either revoke or refresh tokens.

```
```


## Saving Data
Whether you choose a headless or interactive start, in both cases you can choose how your data is saved. The subtle difference for each saving method that result when you choose headless or interactive will be discussed below.


##TODO: talk about saving data for each

        # If headless with token pre-generated OR not headless
        if self.headless and os.path.exists(data_base) or not self.headless:
            do_save = True
        if data_base.endswith(('revoked','finished')):
            do_save = False  


### filesystem
Saving to the filesytem is the default (what you get when you don't specify a particular database) and means saving to a folder called `/scif/data` in the Docker image. If you are saving data to the filesystem (`filesystem` database), given that you've mounted the container data folder `/scif/data` to the host, this means that the data will be found on the host in that location. In the example below, we have mounted `/tmp/data` to `/scif/data` in the container, and we are running interactive experiments (meaning without pre-generated tokens for login):

```
$ tree /tmp/data/expfactory/00000/

    /tmp/data/expfactory/00000/
       └── tower-of-london-results.json

0 directories, 1 file
```

If we had changed our studyid to something else (e.g., `dns`), we might see:

```
$ tree /tmp/data/dns/00000/

    /tmp/data/dns/00000/
       └── tower-of-london-results.json

0 directories, 1 file
```

The subtle difference if we had done a headless start comes down to the subject identifier. If we look at output folders generated for headless start with pre-generated tokens, we see tokens instead:

```
$ tree /tmp/data/expfactory/

   /tmp/data/expfactory/745cb6ad-a0b7-4610-b4d2-4ca5acd8b6f9
    └── tower-of-london-results.json
```

In both cases, participant folders are created under the `studyid` folder.  These start at 00000 and are incremented with each participant you run. If you stop the container and had mounted a volume to the host, the data will persist on the host. If you didn't mount a volume, then you will not see the data on the host.

>> **Protip**  We generally don't recommend serving token (headless) and interactive experiments from the same container. If a study identifier can be predicted (e.g., 00001) then it also could be used as a token, and someone's previous result could be maliciously changed.

Now we will talk about interaction with the data.

#### How do I read it?
For detailed information about how to read json strings (whether from file or database) see [working with JSON](#working-with-json). For a filesystem save, the data is saved to a json object, regardless of the string output produced by the experiment. This means that you can load the data as json, and then look at the `data` key to find the result saved by the particular experiment. Typically you will find another string saved as json, but it could be the case that some experiments do this differently.


### sqlite
An sqlite database can be used instead of a flat filesytem. This will produce one file that you can move around and read with any standard scientific software (python, R) with functions to talk to sqlite databases. If you want to start your container and use sqlite3, then specify:

```
docker run -p 80:80 expfactory/experiments \
           --database sqlite \
           start
```

If you just specify `sqlite` the file will save to a default at `/scif/data/<studyid>.db` You can also specify a custom database uri that starts with sqlite, like `sqlite:////tmp/database.db` that will be generated in the container (and you can optionally map to the host).vFor example, here is my sqlite3 database under `/scif/data`, from within the container:

```
ls /scif/data
    expfactory.db
```

#### How do I read it?
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
>>> row[0]  # table result row index
1

>>> row[1]  # date
'2017-11-18 17:26:30'

>>> row[2]  # data from experiment, json.loads needed
>>> json.loads(row[2])
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

Since the Participant table doesn't hold anything beyond the participant id, you shouldn't need to query it. More detail is added for loading json in (see [loading results](#working-with-json)) below.


### mysql
For labs that wish to deploy the container on a server, you are encouraged to use a more substantial database, such as a traditional relational database like MySQL or Postgres. In all of these cases, you need to specify the full database url. For mysql, we also specify using a particular driver called `pymysql`. For example:

```
# mysql
docker run -p 80:80 expfactory/experiments \
           --database  mysql+pymysql://username:password@host/dbname", \
           start

docker run -p 80:80 vanessa/experiment \
           --database "mysql+pymysql://root:expfactory@172.17.0.3/db" \
           start
```

As an example, let's use a throw away Docker mysql container. We will start it first. You should either use an external database, or a more substantial deployment like Docker=compose, etc.

```
docker run --detach --name=expfactory-mysql --env="MYSQL_ROOT_PASSWORD=expfactory" \
                                            --env="MYSQL_DATABASE=db" \
                                            --env="MYSQL_USER=expfactory" \
                                            --env="MYSQL_PASSWORD=expfactory" \
                                             mysql
```

Note that if you ran the container -with `--publish 6603:3306` it would be mapped to your host (localhost) making it accessible to the outside world.  You should be able to see it with `docker ps`:

```
$ docker ps
CONTAINER ID        IMAGE                COMMAND                  CREATED             STATUS              PORTS                          NAMES
47f9d56f1b3f        mysql                "docker-entrypoint..."   2 minutes ago       Up 2 minutes        3306/tcp                       expfactory-mysql
```

and inspect it to get the IPAddress

```
$ docker inspect expfactory-mysql | grep '"IPAddress"'
            "IPAddress": "172.17.0.2",
```

This is good! We now have the address to give to our Expfactory container.

```
docker run -p 80:80 expfactory/experiments \
           --database "mysql+pymysql://expfactory:expfactory@172.17.0.2/db" \
           start
```

In the example above, the username is `expfactory`, the password is `expfactory`, the host is `172.17.0.2` that we inspected above, and the database name is `db`. You can now open the browser to do an experiment, and then (again) use python to inspect results. I like pymysql because it seems to work in Python 3:


```
import pymysql
conn = pymysql.connect(host='172.17.0.2',
                       user='expfactory',
                       password='expfactory',
                       db='db',
                       charset='utf8mb4',
                       cursorclass=pymysql.cursors.DictCursor)

try:
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM result")
        result = cursor.fetchone()
        print(result)
finally:
    conn.close()
```

and the above will print a nice dump of the test task that we just took!

```
{'date': datetime.datetime(2017, 11, 19, 16, 28, 50), 'exp_id': 'test-task', 'data': '[{"rt":821,"stimulus":"<div class = \\"shapebox\\"><div id = \\"cross\\"></div></div>","key_press":32,"possible_responses":[32],"stim_duration":2000,"block_duration":2000,"timing_post_trial":100,"trial_id":"test","trial_type":"poldrack-single-stim","trial_index":0,"time_elapsed":2004,"internal_node_id":"0.0-0.0","addingOnTrial":"added!","exp_id":"test-task","full_screen":true,"focus_shifts":0},{"rt":400,"stimulus":"<div class = \\"shapebox\\"><div id = \\"cross\\"></div></div>","key_press":32,"possible_responses":[32],"stim_duration":2000,"block_duration":2000,"timing_post_trial":100,"trial_id":"test","trial_type":"poldrack-single-stim","trial_index":1,"time_elapsed":4108,"internal_node_id":"0.0-1.0","addingOnTrial":"added!","exp_id":"test-task","full_screen":false,"focus_shifts":0},{"rt":324,"stimulus":"<div class = \\"shapebox\\"><div id = \\"cross\\"></div></div>","key_press":32,"possible_responses":[32],"stim_duration":2000,"block_duration":2000,"timing_post_trial":100,"trial_id":"test","trial_type":"poldrack-single-stim","trial_index":2,"time_elapsed":6209,"internal_node_id":"0.0-2.0","addingOnTrial":"added!","exp_id":"test-task","full_screen":false,"focus_shifts":0,"added_Data?":"success!"},{"trial_type":"call-function","trial_index":3,"time_elapsed":6310,"internal_node_id":"0.0-3.0","exp_id":"test-task","full_screen":false,"focus_shifts":0},{"rt":4491,"responses":"{\\"Q0\\":\\"jhjkh\\",\\"Q1\\":\\"\\"}","trial_id":"post task questions","trial_type":"survey-text","trial_index":4,"time_elapsed":10805,"internal_node_id":"0.0-5.0","exp_id":"test-task","full_screen":false,"focus_shifts":0},{"text":"<div class = centerbox><p class = center-block-text>Thanks for completing this task!</p><p class = center-block-text>Press <strong>enter</strong> to continue.</p></div>","rt":1413,"key_press":13,"block_duration":1413,"timing_post_trial":0,"trial_id":"end","exp_id":"test-task","trial_type":"poldrack-text","trial_index":5,"time_elapsed":13219,"internal_node_id":"0.0-6.0","credit_var":true,"performance_var":600,"full_screen":false,"focus_shifts":0}]', 'id': 1, 'participant_id': 1}
```

Don't forget to stop your image (control+c if it's hanging, or `docker stop <containerid>` if detached, and then remove the mysql container after that.

```
docker stop expfactory-mysql
docker rm expfactory-mysql
```

Note that this is only an example, we recommend that you get proper hosting (for example, [Stanford provides this](https://uit.stanford.edu/service/sql) for users) or use a standard cloud service (AWS or Google Cloud) to do the same. You generally want to make sure your database has sufficient levels of permissions to be sure, encryption if necessary, and redundancy (backup). Keep in mind that some experiments might give participants open boxes to type, meaning you should be careful about PHI, etc. This is also another reason that a much simpler, local save to the file system isn't such a crazy idea. Always discuss your experiment strategy with your IRB before proceeding!

### postgres
We can do similar to the above, but use postgres instead. First we will start a second container:

```
docker run --name expfactory-postgres --env POSTGRES_PASSWORD=expfactory \
                                      --env POSTGRES_USER=expfactory  \
                                      --env POSTGRES_DB=db \
                                      -d postgres 
```

Ensure that our container is running with `docker ps`

```
docker ps
CONTAINER ID        IMAGE               COMMAND                  CREATED             STATUS              PORTS               NAMES
bb748a75bd91        postgres            "docker-entrypoint..."   2 seconds ago       Up 1 second         5432/tcp            expfactory-postgres
```

and of course get the IPAddress



```
$ docker inspect expfactory-postgres | grep '"IPAddress"'
            "IPAddress": "172.17.0.2",
```

Now we can again form our complete database url to give to the experiment factory container to connect to:

```
# postgres
docker run -p 80:80 vanessa/experiment \
           --database "postgres://expfactory:expfactory@172.17.0.2/db" \
           start
```
If you leave it hanging in the screen (note no -d for detached above) you will see this before the gunicorn log:

```
Database set as postgres://expfactory:expfactory@172.17.0.2/db
```

Now let's again do the test task, and start up python on our local machine to see if we have results!

```
import psycopg2
db = "host='172.17.0.2' dbname='db' user='expfactory' password='expfactory'"
conn = psycopg2.connect(db)
cursor = conn.cursor()
cursor.execute("SELECT * FROM result")
result = cursor.fetchall()
```
And here is our row, a list with 5 indices.

```
[(1,
  datetime.datetime(2017, 11, 19, 16, 48, 51, 957224),
  '[{"rt":1294,"stimulus":"<div class = \\"shapebox\\"><div id = \\"cross\\"></div></div>","key_press":32,"possible_responses":[32],"stim_duration":2000,"block_duration":2000,"timing_post_trial":100,"trial_id":"test","trial_type":"poldrack-single-stim","trial_index":0,"time_elapsed":2005,"internal_node_id":"0.0-0.0","addingOnTrial":"added!","exp_id":"test-task","full_screen":false,"focus_shifts":0},{"rt":163,"stimulus":"<div class = \\"shapebox\\"><div id = \\"cross\\"></div></div>","key_press":32,"possible_responses":[32],"stim_duration":2000,"block_duration":2000,"timing_post_trial":100,"trial_id":"test","trial_type":"poldrack-single-stim","trial_index":1,"time_elapsed":4107,"internal_node_id":"0.0-1.0","addingOnTrial":"added!","exp_id":"test-task","full_screen":false,"focus_shifts":0},{"rt":324,"stimulus":"<div class = \\"shapebox\\"><div id = \\"cross\\"></div></div>","key_press":32,"possible_responses":[32],"stim_duration":2000,"block_duration":2000,"timing_post_trial":100,"trial_id":"test","trial_type":"poldrack-single-stim","trial_index":2,"time_elapsed":6208,"internal_node_id":"0.0-2.0","addingOnTrial":"added!","exp_id":"test-task","full_screen":false,"focus_shifts":0,"added_Data?":"success!"},{"trial_type":"call-function","trial_index":3,"time_elapsed":6309,"internal_node_id":"0.0-3.0","exp_id":"test-task","full_screen":false,"focus_shifts":0},{"rt":6904,"responses":"{\\"Q0\\":\\"bloop\\",\\"Q1\\":\\"debloop\\"}","trial_id":"post task questions","trial_type":"survey-text","trial_index":4,"time_elapsed":13217,"internal_node_id":"0.0-5.0","exp_id":"test-task","full_screen":false,"focus_shifts":0},{"text":"<div class = centerbox><p class = center-block-text>Thanks for completing this task!</p><p class = center-block-text>Press <strong>enter</strong> to continue.</p></div>","rt":916,"key_press":13,"block_duration":916,"timing_post_trial":0,"trial_id":"end","exp_id":"test-task","trial_type":"poldrack-text","trial_index":5,"time_elapsed":15135,"internal_node_id":"0.0-6.0","credit_var":true,"performance_var":676,"full_screen":false,"focus_shifts":0}]',
  'test-task',
  1)]
```

 - `row[0][0]` is the index for the result table, probably not useful
 - `row[0][1]` is a python datetime object for when the result was created
 - `row[0][2]` is the data from the experiment
 - `row[0][3]` is the experiment id (`exp_id`)
 - `row[0][4]` is the participant id

Again, you should consider a robust and secure setup when running this in production. For the example, don't forget to shut down your database after the image.

```
docker stop expfactory-postgres
docker rm expfactory-postgres
```

The reason to provide these arguments at runtime is that the particulars of the database (username, password, etc.) will not be saved with the image, but specified when you start it. Be careful that you do not save any secrets or credentials inside the image, and if you use an image with an existing expfactory config.py, you re-generate the secret first.

### CouchDB/MariaDB/Mongo/Other
We haven't yet developed this, and if you are interested, please [file an issue](https://github.com/expfactory/expfactory/issues). If you need help with more substantial or different deployments, please reach out!


## Start your Participant
Here we assume that you have chosen some database and that your container is running, and will look quickly at the experience of running a participant through a selection of experiments. From the commands above, we see that we generated and started our container, and mapped it to port 80 on our machine.

Not mapping a folder to /scif/data assumes that either we don't want to see files on the host, **or** if the image default is to save to a relational database external to the experiments container itself, we access data by querying this separate endpoint. For a filesystem or sqlite database, since the file is stored inside the container and we want access to it, we likely started with the location mapped:

```
docker run -p 80:80 -v /tmp/data:/scif/data vanessa/expfactory-experiments start
```

First, let's discuss the portal - what you see when you go to [127.0.0.1](http://127.0.0.1).

## The Experiment Factory Portal
When you start your container instance, browsing to your localhost will show the entrypoint, a user portal that lists all experiments installed in the container. If you have defined a limited subset with `--experiments` you will only see that set here:

<div>
    <img src="../img/generate/portal.png"><br>
</div>


This is where the experiment administrator would select one or more experiments, either with the single large checkbox ("select all") or smaller individual checkboxes. 
 When you make a selection, the estimated time and experiment count on the bottom of the page are adjusted, and you can inspect individual experiment times: 

<div>
    <img src="../img/generate/selected.png"><br>
</div>

You can make a selection and then start your session. I would recommend the `test-task` as a first try, because it finishes quickly. When you click on `proceed` a panel will pop up that gives you choices for ordering and an (optional) Participant name. 

<div>
    <img src="../img/generate/proceed.png"><br>
</div>

If you care about order, the order that you selected the boxes will be maintained for the session:

<div>
    <img src="../img/generate/order-manual.png"><br>
</div>

or if you want random selection, just check the box. This is the default setting.

<div>
    <img src="../img/generate/order-random.png"><br>
</div>

This name is currently is only used to say hello to the participant. The actual experiment identifier is based on a study id defined in the build recipe.  After proceeding, there is a default "consent" screen that you must agree to (or disagree to return to the portal):

<div>
    <img src="../img/generate/welcome.png"><br>
</div>


Once the session is started, the user is guided through each experiment (with random selection) until no more are remaining.

<div>
    <img src="../img/generate/preview.png"><br>
</div>


When you finish, you will see a "congratulations" screen

<div>
    <img src="../img/generate/finish.png"><br>
</div>

Generally, when you administer a battery of experiments you want to ensure that:

 - if a database isn't external to the container, the folder is mapped (or the container kept running to retrieve results from) otherwise you will lose the results.
 - if the container is being served on a server open to the world, you have added proper authorization (note this isn't developed yet, please file an issue if you need this)
 - you have fully tested data collection and inspected the results before administering any kind of "production" battery.



## Working with JSON
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

Bootstrap: docker
From: ubuntu:14.04

########################################
# Configure
########################################

%environment
    EXPFACTORY_STUDY_ID=expfactory
    EXPFACTORY_SERVER=localhost
    export EXPFACTORY_STUDY_ID \
           EXPFACTORY_SERVER


########################################
# Install No need to touch below here
########################################

    EXPFACTORY_CONTAINER=true
    EXPFACTORY_DATA=/scif/data
    EXPFACTORY_DATABASE=filesystem 
    EXPFACTORY_BASE=/scif/apps
    export EXPFACTORY_BASE EXPFACTORY_DATA \
           EXPFACTORY_DATABASE \
           EXPFACTORY_CONTAINER

%help

If you want to see experiments available:
    singularity apps expfactory.img

To build your image (sandbox for testing)
    sudo singularity build --sandbox [expfactory] Singularity

To build your image (production)
    sudo singularity build expfactory.simg Singularity

To serve your battery
    sudo singularity instance.start expfactory.simg web1

%startscript
    service nginx start
    gunicorn --bind 0.0.0.0:5000 expfactory.wsgi:app
    service nginx restart

%post
    apt-get update && apt-get install -y nginx git python3-pip python3-dev
    cd /opt && git clone https://www.github.com/expfactory/expfactory
    cd expfactory && cp script/nginx.gunicorn.conf /etc/nginx/sites-enabled/default
    cp script/nginx.conf /etc/nginx/nginx.conf
    mkdir -p /scif/apps
    python3 -m pip install gunicorn
    cp expfactory/config_dummy.py expfactory/config.py
    chmod u+x /opt/expfactory/script/generate_key.sh
    /bin/bash /opt/expfactory/script/generate_key.sh /opt/expfactory/expfactory/config.py
    python3 setup.py install


########################################
# Experiments will be auto generated
########################################

%appinstall test-task
    cd .. && expfactory install -f https://github.com/expfactory-experiments/test-task

%appinstall adaptive-n-back
    cd .. && expfactory install -f https://github.com/expfactory-experiments/adaptive-n-back

%appinstall tower-of-london
    cd .. && expfactory install -f https://github.com/expfactory-experiments/tower-of-london

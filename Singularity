Bootstrap: docker
From: ubuntu:14.04

########################################
# Configure
########################################

%environment
    EXPFACTORY_STUDY_ID=expfactory
    export EXPFACTORY_STUDY_ID


########################################
# Install No need to touch below here
########################################

    EXPFACTORY_BASE=/scif/apps
    export EXPFACTORY_BASE

%help

If you want to see experiments available:
    singularity apps expfactory.img

To build your image (sandbox for testing)
   sudo singularity build --sandbox expfac Singularity

To serve your battery
    sudo singularity instance.start expfactory.img web1

%startscript
    service nginx start && cd /opt
    #exec gunicorn --bind 0.0.0.0:5000 expfactory.wsgi:app
    #exec /usr/local/bin/gunicorn -w 2 -b :5000 expfactory.cli:main
    #exec expfactory "$@"

%post
    apt-get update && apt-get install -y nginx git python3-pip python3-dev
    cd /opt && git clone https://www.github.com/expfactory/expfactory
    cd expfactory && python3 setup.py install
    cp script/nginx.gunicorn.conf /etc/nginx/sites-enabled/default
    mkdir -p /scif/apps
    SECRET_KEY=`python3 script/generate_key.py` 
    cp expfactory/config_dummy.py expfactory/config.py
    echo "${SECRET_KEY}" >> /opt/expfactory/config.py


########################################
# Experiments will be auto generated
########################################

%appinstall test-task
    expfactory --install https://github.com/expfactory-experiments/test-task

%appinstall adaptive-n-back
    expfactory --install https://github.com/expfactory-experiments/adaptive-n-back

%appinstall tower-of-london
    expfactory --install https://github.com/expfactory-experiments/tower-of-london

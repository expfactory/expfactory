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

%help

If you want to see experiments available:
    singularity apps expfactory.img

To build your image (sandbox for testing)
   sudo singularity build --sandbox expfac Singularity

To serve your battery
    sudo singularity instance.start expfactory.img web1

%startscript
    service nginx start
    #exec /usr/local/bin/gunicorn -w 2 -b :5000 expfactory.cli:main
    #exec expfactory "$@"

%post
    apt-get update && apt-get install -y nginx git python3-pip python3-dev
    git clone https://www.github.com/expfactory/expfactory
    cd expfactory && python3 setup.py install
    cp script/nginx.conf /etc/nginx/sites-enabled/default
    mkdir -p /scif/apps && mkdir -p /opt/expfactory
    SECRET_KEY=`python script/generate_key.py` 
    echo "${SECRET_KEY}" >> /opt/expfactory/config.py
    cp script/nginx-index.html /scif/apps/index.html


########################################
# Experiments will be auto generated
########################################


%appinstall adaptive-n-back
    git clone https://github.com/expfactory-experiments/adaptive-n-back
    mv adaptive-n-back/* .

%appinstall tower-of-london
    git clone https://github.com/expfactory-experiments/tower-of-london
    mv tower-of-london/* .

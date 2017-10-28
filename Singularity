Bootstrap: docker
From: ubuntu:14.04

%help

If you want to see experiments available:
    singularity apps expfactory.img

To build your image (sandbox for testing)
   sudo singularity build --sandbox expfactory Singularity

To serve your battery
    singularity instance.start expfactory.img web1

%environment
STUDY_ID=expfactory
export STUDY_ID

%startscript
    service nginx start
    exec expfactory "$@"

%post
apt-get update && apt-get install -y nginx git python3-pip python3-dev
git clone -b development https://www.github.com/expfactory/expfactory-python
cd expfactory-python && python3 setup.py install
cp script/nginx.conf /etc/nginx/sites-enabled/default

%appinstall adaptive-n-back
    git clone https://github.com/expfactory-experiments/adaptive-n-back
    mv adaptive-n-back/* .

%appinstall tower-of-london
    git clone https://github.com/expfactory-experiments/tower-of-london
    mv tower-of-london/* .

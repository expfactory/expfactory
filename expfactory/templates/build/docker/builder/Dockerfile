FROM ubuntu:14.04

# docker build -t vanessa/expfactory-builder .

RUN apt-get update && apt-get install -y nginx git python3-pip python3-dev python
ENV DEBIAN_FRONTEND noninteractive

###################################
# Experiment Factory
###################################

WORKDIR /opt
RUN git clone -b update/docker https://www.github.com/expfactory/expfactory
WORKDIR /opt/expfactory
RUN python3 setup.py install
ADD entrypoint.sh /entrypoint.sh
RUN chmod u+x /entrypoint.sh
RUN mkdir -p /scif/apps
RUN mkdir -p /data

ENTRYPOINT ["/bin/bash","/entrypoint.sh"]

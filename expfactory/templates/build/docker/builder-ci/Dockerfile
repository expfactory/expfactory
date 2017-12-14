FROM ubuntu:16.04

# docker build -t vanessa/expfactory-builder-ci .

RUN apt-get update && apt-get install -y nginx git python3-pip python3-dev python apt-utils
ENV DEBIAN_FRONTEND noninteractive

###################################
# Experiment Factory
###################################

WORKDIR /opt
ADD . /opt
RUN ls
WORKDIR /opt/expfactory
RUN ls
RUN python3 setup.py install
RUN mv /opt/entrypoint.sh /entrypoint.sh
RUN chmod u+x /entrypoint.sh
RUN mkdir -p /scif/apps
RUN mkdir -p /data

ENTRYPOINT ["/bin/bash","/entrypoint.sh"]

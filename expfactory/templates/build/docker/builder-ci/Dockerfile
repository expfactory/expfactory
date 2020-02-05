FROM quay.io/vanessa/expfactory-builder:base

# docker build -t quay.io/vanessa/expfactory-builder-ci .

###################################
# Experiment Factory
###################################

WORKDIR /opt
ADD . /opt
WORKDIR /opt/expfactory
RUN python3 setup.py install
RUN mv /opt/entrypoint.sh /entrypoint.sh
RUN chmod u+x /entrypoint.sh
RUN mkdir -p /scif/apps
RUN mkdir -p /data

ENTRYPOINT ["/bin/bash","/entrypoint.sh"]

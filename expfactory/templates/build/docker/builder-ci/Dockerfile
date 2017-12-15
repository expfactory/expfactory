FROM vanessa/expfactory-builder:base

# docker build -t vanessa/expfactory-builder-ci .

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

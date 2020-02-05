FROM quay.io/vanessa/expfactory-builder:base

# docker build -t quay.io/vanessa/expfactory-builder-dev .

###################################
# Experiment Factory
###################################

WORKDIR /opt
RUN git clone -b add/variables https://www.github.com/expfactory/expfactory
WORKDIR /opt/expfactory
RUN python3 setup.py install
RUN python3 -m pip install pyaml
ADD entrypoint.sh /entrypoint.sh
RUN chmod u+x /entrypoint.sh
RUN mkdir -p /scif/apps
RUN mkdir -p /data

ENTRYPOINT ["/bin/bash","/entrypoint.sh"]

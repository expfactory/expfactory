FROM ubuntu:16.04

RUN apt-get update && apt-get install -y git python3-pip python3-dev
WORKDIR /opt 
RUN git clone https://www.github.com/expfactory/expfactory
WORKDIR expfactory 
RUN python3 setup.py install
RUN python3 -m pip install pandas

RUN mkdir /code  # for script
WORKDIR /code
ADD . /code
RUN chmod u+x /code/entrypoint.sh && \
    chmod u+x /code/survey.py

RUN mkdir /data  # bind survey folder to
RUN apt-get clean

ENTRYPOINT ["/bin/bash", "/code/entrypoint.sh"]

FROM quay.io/vanessa/expfactory-builder:base

########################################
# Configure
########################################

ENV EXPFACTORY_STUDY_ID expfactory
ENV EXPFACTORY_SERVER localhost
ENV EXPFACTORY_CONTAINER true
ENV EXPFACTORY_DATA /scif/data
ENV EXPFACTORY_DATABASE filesystem
ENV EXPFACTORY_HEADLESS false
ENV EXPFACTORY_BASE /scif/apps

COPY startscript.sh /startscript.sh
RUN chmod u+x /startscript.sh

WORKDIR /opt 
RUN git clone -b add/check-data-exists https://github.com/expfactory/expfactory
WORKDIR expfactory 
RUN cp script/nginx.gunicorn.conf /etc/nginx/sites-enabled/default && \
    cp script/nginx.conf /etc/nginx/nginx.conf
RUN mkdir -p /scif/data # saved data
RUN mkdir -p /scif/apps # experiments 
RUN mkdir -p /scif/logs # gunicorn logs 
RUN python3 -m pip install gunicorn
RUN cp expfactory/config_dummy.py expfactory/config.py && \
    chmod u+x /opt/expfactory/script/generate_key.sh && \
    /bin/bash /opt/expfactory/script/generate_key.sh /opt/expfactory/expfactory/config.py
RUN python3 setup.py install
RUN python3 -m pip install pyaml    pymysql psycopg2-binary
RUN apt-get clean          # tests, mysql,  postgres

########################################
# Experiments
########################################

LABEL EXPERIMENT_general-self-efficacy-survey /scif/apps/general-self-efficacy-survey
WORKDIR /scif/apps
RUN expfactory install https://github.com/expfactory-experiments/general-self-efficacy-survey

LABEL EXPERIMENT_grit-scale-survey /scif/apps/grit-scale-survey
WORKDIR /scif/apps
RUN expfactory install https://github.com/expfactory-experiments/grit-scale-survey



ENTRYPOINT ["/bin/bash", "/startscript.sh"]
EXPOSE 5000
EXPOSE 443
EXPOSE 80

#!/bin/bash

# Run this command to generate the Dockerfile that builds your container.
# Container        : docker
# Tag              : survey


# List experiments : docker run vanessa/expfactory-builder list
# Options          : docker run vanessa/expfactory-builder build --help
# Make Dockerfile  : docker run -v /tmp/my-experiment:/data vanessa/expfactory-builder build [experiment1 .. experimentn]
# Build Dockerfile : docker build -t vanessa/survey .
# Run container    : docker run -v /tmp/data:/scif/data -p 80:80 vanessa/survey start


# Here is the command to generate your Dockerfile (3rd step)
docker run -v $PWD:/data vanessa/expfactory-builder build  alcohol-drugs-survey  bis-bas-survey  bis11-survey  brief-self-control-survey  cognitive-reflection-survey  demographics-survey  dickman-survey  dospert-eb-survey  dospert-rp-survey  dospert-rt-survey  eating-survey  erq-survey  five-facet-mindfulness-survey  future-time-perspective-survey  grit-scale-survey  holt-laury-survey  impulsive-venture-survey  k6-survey  leisure-time-activity-survey  mindful-attention-awareness-survey  mpq-control-survey  selection-optimization-compensation-survey  self-regulation-survey  sensation-seeking-survey  state-mindfulness-survey  ten-item-personality-survey  theories-of-willpower-survey  time-perspective-survey  treatment-self-regulation-survey  upps-impulsivity-survey 

                




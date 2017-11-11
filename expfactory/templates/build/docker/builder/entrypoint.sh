#!/bin/bash

if [ $# -eq 0 ]; then
    echo "Usage:"
    echo "docker run vanessa/expfactory-builder build experiment-one experiment-two ..."
    expfactory build --help
    exit
fi

if [ $1 == "list" ]; then 
    expfactory list
    exit
fi

if [ $1 == "build" ]; then 

    shift
    recipe="/data/Dockerfile"

    # Don't overwrite recipe
    if [ -f "${recipe}" ]; then
        echo "Dockerfile already found under /data, will not overwrite."
        exit
    fi

    expfactory build  --output ${recipe} "$@" 

    if [ -f "${recipe}" ]; then
        cp /opt/expfactory/expfactory/templates/build/docker/startscript.sh /data
        echo "Dockerfile finished at ${recipe}!"
        echo "To build, cd to recipe and:
              docker build -t expfactory/experiments ."
    else
        expfactory build --help
        exit
    fi
else
    echo "Usage:
          docker run vanessa/expfactory-builder list
          docker run vanessa/expfactory-builder bulid experiment-one experiment-two ..."

fi

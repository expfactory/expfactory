#!/bin/bash

if [ $# -eq 0 ]; then
    echo "Usage:"
    echo "
          docker run vanessa/expfactory-builder build experiment-one experiment-two ...
          docker run -v experiments:/scif/apps vanessa/expfactory-builder test
          docker run -v _library:/scif/apps vanessa/expfactory-builder test-contribution"
    exit
fi

if [ $1 == "list" ]; then 
    expfactory list
    exit
fi

if [ $1 == "test" ]; then 
    echo "Testing experiments mounted to /scif/apps"
    cd /opt/expfactory/expfactory/templates/build
    exec python3 -m unittest tests.test_experiment
    exit
fi

if [ $1 == "test-library" ]; then 
    echo "Testing library contributions mounted to /scif/apps"
    cd /opt/expfactory/expfactory/templates/build
    exec python3 -m unittest tests.test_contribution
    exit
fi

if [ $1 == "build" ]; then 

    shift
    recipe="/data/Dockerfile"

    if [ $# -eq 0 ]; then
        expfactory build --help
        exit
    fi

    # Don't overwrite recipe
    if [ -f "${recipe}" ]; then
        echo "Dockerfile already found under /data, will not overwrite."
        exit
    fi

    expfactory build  --output ${recipe} "$@" 

    if [ -f "${recipe}" ]; then
        cp /opt/expfactory/expfactory/templates/build/docker/startscript.sh /data
        echo
        echo "To build, cd to recipe and:
              docker build -t expfactory/experiments ."
    else
        expfactory build --help
        exit
    fi
else
    echo "Usage:"
    echo "      
          docker run vanessa/expfactory-builder build experiment-one experiment-two ...
          docker run -v experiments:/scif/apps vanessa/expfactory-builder test
          docker run -v _library:/scif/apps vanessa/expfactory-builder test-contribution"

fi

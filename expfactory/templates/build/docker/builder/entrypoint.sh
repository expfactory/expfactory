#!/bin/bash

usage () {

    echo "Usage:    docker run quay.io/vanessa/expfactory-builder [list|build|test|test-library]

          LIST experiments

              docker run quay.io/vanessa/expfactory-builder list
              docker run quay.io/vanessa/expfactory-builder list | grep survey

          BUILD a container recipe (Dockerfile)

              # generate build recipe for 2 experiments in new directory /tmp/data
              docker run -v /tmp/data:/data quay.io/vanessa/expfactory-builder build test-task tower-of-london

              # generate build recipe with local experiment folder (test-task-two) in (\$PWD)
              # We reference the fullpath to the experiment in the container (/data/test-task-two).
              docker run -v \$PWD:/data quay.io/vanessa/expfactory-builder build test-task /data/test-task-two

          TEST local experiments or library folder

              # Test local experiments folder 'experiments' 
              docker run -v experiments:/scif/apps quay.io/vanessa/expfactory-builder test

              # Test local library in folder 'library'
              docker run -v library:/scif/apps quay.io/vanessa/expfactory-builder test-library
 
         https://expfactory.github.io/generate#container-generation
         "
}

if [ $# -eq 0 ]; then
    usage
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
        echo "To build, cd to directory with Dockerfile and:
              docker build --no-cache -t expfactory/experiments ."
    else
        expfactory build --help
        exit
    fi
else
    usage
fi

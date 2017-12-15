#!/bin/sh

echo "Testing builder writing to /tmp"

mkdir -p /tmp/data && cd /tmp/data
docker run -v $PWD:/data vanessa/expfactory-builder-ci build test-task

echo "Building container"
docker build -t expfactory/experiments .

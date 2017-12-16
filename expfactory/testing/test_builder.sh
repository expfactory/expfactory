#!/bin/sh

echo "Testing expfactory-builder"

mkdir -p /tmp/data && cd /tmp/data
docker run -v $PWD:/data vanessa/expfactory-builder-ci build test-task

echo "Building container"
docker build -t expfactory/experiments .

echo "Start [filesystem][sqlite]"
docker run -d -v $PWD:/scif/data -p 80:80 --name experiments-fs expfactory/experiments --headless start
docker run -d -v $PWD:/scif/data --name experiments-sqlite expfactory/experiments --database sqlite --headless start

# HTTP/1.1 200 OK
curl -I localhost | grep 200

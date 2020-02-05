#!/bin/sh

# See .circleci/config.yml for the version that is run on CircleCI

echo "Testing expfactory-builder"

mkdir -p /tmp/data && cd /tmp/data
docker run -v /tmp/data:/data quay.io/vanessa/expfactory-builder-ci build test-task

echo "Contents of /tmp/data"
ls

echo "Building container"
docker build -t expfactory/experiments .

echo "Start [filesystem][sqlite]"
docker run -d -v /tmp/data:/scif/data -p 80:80 --name experiments-fs expfactory/experiments --headless start
docker run -d -v /tmp/data:/scif/data --name experiments-sqlite expfactory/experiments --database sqlite --headless start

# HTTP/1.1 200 OK
curl -I localhost | grep 200

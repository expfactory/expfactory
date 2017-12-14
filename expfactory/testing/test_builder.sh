#!/bin/sh

echo "Testing builder writing to /tmp"
mkdir -p /tmp/data
docker run -v /tmp/data:/data vanessa/expfactory-builder build test-task

echo "Building container"
cd /tmp/data
docker build -t expfactory/experiments .

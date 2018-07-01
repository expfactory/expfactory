#!/bin/sh

# These builds should be done after a PR is merged, and master branch is
# updated with the version indicated. This should be run from the script
# directory as the PWD.

VERSION_TAG=3.13
BASE="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && cd .. && pwd )"

# Docker Builder Base
# This is the base image for the various builders

cd $BASE/expfactory/templates/build/docker/builder-base
docker build -t vanessa/expfactory-builder:base .

docker tag vanessa/expfactory-builder:base vanessa/expfactory-builder:base-v$VERSION_TAG
docker push vanessa/expfactory-builder:base
docker push vanessa/expfactory-builder:base-v$VERSION

# vanessa/expfactory-builder
# Build builder with tag, and push tag and latest
cd $BASE/expfactory/templates/build/docker/builder
docker build --no-cache -t vanessa/expfactory-builder .
docker tag vanessa/expfactory-builder vanessa/expfactory-builder:$VERSION_TAG
docker push vanessa/expfactory-builder:$VERSION_TAG
docker push vanessa/expfactory-builder

# vanessa/expfactory-surveys
cd $BASE/examples/docker/surveys-container
rm $PWD/Dockerfile
./expfactory-generate.sh
docker build --no-cache -t vanessa/expfactory-surveys .
docker tag vanessa/expfactory-surveys vanessa/expfactory-surveys:$VERSION_TAG
docker push vanessa/expfactory-surveys:$VERSION_TAG
docker push vanessa/expfactory-surveys

# vanessa/expfactory-survey (create survey)
#cd $BASE/examples/docker/create-survey
#docker build -t vanessa/expfactory-survey .
#docker tag vanessa/expfactory-survey vanessa/expfactory-survey:$VERSION_TAG
#docker push vanessa/expfactory-survey:$VERSION_TAG
#docker push vanessa/expfactory-survey

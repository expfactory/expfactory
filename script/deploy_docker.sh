#!/bin/sh

# These builds should be done after a PR is merged, and master branch is
# updated with the version indicated. This should be run from the script
# directory as the PWD.

VERSION_TAG=3.11
BASE="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && cd .. && pwd )"

# vanessa/expfactory-builder
# Build builder with tag, and push tag and latest
cd $BASE/expfactory/templates/build/docker/builder
docker build --no-cache -t vanessa/expfactory-builder .
docker tag vanessa/expfactory-builder vanessa/expfactory-builder:$VERSION_TAG
docker push vanessa/expfactory-builder:$VERSION_TAG
docker push vanessa/expfactory-builder

# vanessa/expfactory-surveys
cd $BASE/examples/docker/surveys-container
./expfactory-generate.sh
docker build --no-cache -t vanessa/expfactory-surveys .
docker tag vanessa/expfactory-surveys vanessa/expfactory-surveys:$VERSION_TAG
docker push vanessa/expfactory-surveys:$VERSION_TAG
docker push vanessa/expfactory-surveys

# vanessa/experiments (create survey)
cd $BASE/examples/docker/custom-container
docker build -t vanessa/experiments .
docker tag vanessa/experiments vanessa/experiments:$VERSION_TAG
docker push vanessa/experiments:$VERSION_TAG
docker push vanessa/experiments

# vanessa/expfactory-games
cd $BASE/examples/docker/expfactory-games
./expfactory-generate.sh
docker build -t vanessa/expfactory-games .
docker tag vanessa/expfactory-games vanessa/expfactory-games:$VERSION_TAG
docker push vanessa/expfactory-games:$VERSION_TAG
docker push vanessa/expfactory-games

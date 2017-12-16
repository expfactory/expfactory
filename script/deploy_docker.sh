#!/bin/sh

# These builds should be done after a PR is merged, and master branch is
# updated with the version indicated

VERSION_TAG=3.1
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

# vanessa/expfactory-survey (create survey)
cd $BASE/examples/docker/create-survey
docker build -t vanessa/expfactory-survey .
docker tag vanessa/expfactory-survey vanessa/expfactory-survey:$VERSION_TAG
docker push vanessa/expfactory-survey:$VERSION_TAG
docker push vanessa/expfactory-survey

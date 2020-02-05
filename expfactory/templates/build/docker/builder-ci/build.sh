#!/use/bin/bash

echo "Building CI builder for testing current PR..."
EXPFACTORY_BRANCH=$CIRCLE_BRANCH docker build --rm=false -t quay.io/vanessa/expfactory-builder-ci .

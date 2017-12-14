#!/use/bin/bash

echo "Building CI builder for testing current PR..."
docker build --rm=false -t vanessa/expfactory-builder-ci .

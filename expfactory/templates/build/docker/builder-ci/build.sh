#!/use/bin/bash

echo "Building CI builder for testing current PR..."
cp -R ../../../../../expfactory $PWD
ls
docker build --rm=false -t vanessa/expfactory-builder-ci .

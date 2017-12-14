#!/use/bin/bash

echo "Building CI builder for testing current PR..."
ls ../../../../../
cp -R ../../../../../. $PWD
cp ../builder/entrypoint.sh $PWD
ls
docker build --rm=false -t vanessa/expfactory-builder-ci .

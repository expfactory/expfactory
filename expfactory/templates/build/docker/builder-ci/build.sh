#!/use/bin/bash

echo "Building CI builder for testing current PR..."
cp -r ../../../../. $PWD/
cp ../builder/entrypoint.sh $PWD
ls
docker build --rm=false -t vanessa/expfactory-builder-ci .

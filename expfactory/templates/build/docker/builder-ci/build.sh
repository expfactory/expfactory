#!/use/bin/bash

echo "Building CI builder for testing current PR..."
mkdir -p /tmp/data
cp ../builder/entrypoint.sh /tmp/data
cp Dockerfile /tmp/data
cd /tmp/data && docker build --rm=false -t vanessa/expfactory-builder-ci .

# Docker Builder Base

This is the base image for the various builders

```bash
docker build -t quay.io/vanessa/expfactory-builder-base .
```


```bash
# Make sure expfactory version is the most recent install
VERSION=$(expfactory version)

docker tag quay.io/vanessa/expfactory-builder-base quay.io/vanessa/expfactory-builder:base
docker tag quay.io/vanessa/expfactory-builder-base quay.io/vanessa/expfactory-builder:base-v$VERSION

docker push quay.io/vanessa/expfactory-builder:base-v$VERSION
docker push quay.io/vanessa/expfactory-builder:base
```

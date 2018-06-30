# Docker Builder Base

This is the base image for the various builders

```bash
docker build -t vanessa/expfactory-builder-base .
```


```bash
# Make sure expfactory version is the most recent install
VERSION=$(expfactory version)

docker tag vanessa/expfactory-builder-base vanessa/expfactory-builder:base
docker tag vanessa/expfactory-builder-base vanessa/expfactory-builder:base-v$VERSION

docker push vanessa/expfactory-builder:base-v$VERSION
docker push vanessa/expfactory-builder:base
```

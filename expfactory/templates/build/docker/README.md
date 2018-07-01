# Builder Containers

These are builder containers to generate Experiment Factory containers. The templates
(both Singularity and Docker) in this folder will be used by [docker](docker) to
generate a docker image **just** for your experiment protocol.

 - [Docker instructions](builder/README.md)
 - [Dockerfile.template](Dockerfile.template) is the standard template used for (non-https) containers.
 - [Dockerfile.https](Dockerfile.https) is for https containers. This can be specified for a build with the `--input` argument as `bulid/docker/Dockerfile.https`.
 - [deploy_docker.sh](../../../../script/deploy_docker.sh) is used to deploy Docker containers.

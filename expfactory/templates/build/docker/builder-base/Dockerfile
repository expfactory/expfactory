FROM ubuntu:16.04

# docker build -t quay.io/vanessa/expfactory-builder:base .

RUN apt-get update && apt-get install -y nginx \
                                         git \
                                         python3-pip \
                                         python3-dev \
                                         python \
                                         libyaml-dev \
                                         libssl-dev \
                                         python-dev \
                                         libffi-dev
ENV DEBIAN_FRONTEND noninteractive

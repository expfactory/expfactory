FROM ubuntu:20.04

# docker build -t quay.io/vanessa/expfactory-builder:base .

ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y nginx \
                                         git \
                                         python3-pip \
                                         python3-dev \
                                         libyaml-dev \
                                         libssl-dev \
                                         libffi-dev
ENV DEBIAN_FRONTEND noninteractive

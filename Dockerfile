
# Specify an argument with a default value
ARG python_version=3.9-alpine

# Specify the base image
FROM --platform=linux/amd64 python:${python_version} AS subrake2
RUN echo "Version for Python: " ${python_version}

# ENV VARS
ENV DEBIAN_FRONTEND=noninteractive

# Add Data
RUN mkdir /root/subrake
COPY ./ /root/subrake

# Changing current directory
WORKDIR /root/subrake

# Installing the complete package
RUN apk update
RUN apk add git
RUN chmod +x ./installer.sh
RUN sed -i '1s|^#!/bin/bash$|#!/bin/sh|' ./installer.sh
RUN ./installer.sh --plugins
RUN python setup.py install

ENTRYPOINT [ "subrake" ]
CMD ["--help"]

# Specify an argument with a default value
ARG ubuntu_version=20.04

# Specify the base image
FROM --platform=linux/amd64 ubuntu:${ubuntu_version} AS subrake2

RUN echo "Version for ubuntu: " ${ubuntu_version}

# This doesn't actually publish the port, but is a hint to the user
EXPOSE 9090/tcp

# ENV VARS
ENV DEBIAN_FRONTEND=noninteractive
ENV CUSERNAME=subtap
ENV CPASSWORD=password

# Add Data
RUN mkdir /root/subrake
COPY ./ /root/subrake

# Changing current directory
WORKDIR /root/subrake

# Installing the complete package
RUN chmod +x /root/subrake/installer.sh
RUN /root/subrake/installer.sh

# Adding bashrunner to bashrc
RUN echo "bashrunner" >> /home/subtap/.bashrc

# Set an environment variable to be available in the container
ENV SUBRAKED_VERSION=2.0
CMD while true; do echo "Subraked version ${SUBRAKED_VERSION}"; sleep 5; done

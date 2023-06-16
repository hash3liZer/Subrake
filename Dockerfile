
# Specify an argument with a default value
ARG ubuntu_version=20.04

# Specify the base image
FROM --platform=linux/amd64 ubuntu:${ubuntu_version} AS subrake2

RUN echo "Version for ubuntu: " ${ubuntu_version}

# This doesn't actually publish the port, but is a hint to the user
EXPOSE 999/tcp

# ENV VARS
ENV CUSERNAME=subtap
ENV CPASSWORD=password

# Installing cockpit
RUN apt update && apt install -y cockpit

# Add Data
RUN mkdir /root/subrake
COPY ./ /root/subrake

RUN chmod +x /root/subrake/installer.sh
RUN /root/subrake/installer.sh

# Set an environment variable to be available in the container
ENV SUBRAKED_VERSION=2.0
CMD while true; do echo "Subraked version ${SUBRAKED_VERSION}"; sleep 5; done

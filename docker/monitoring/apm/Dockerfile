FROM python:3.6.5-slim

# install netcat, dev-tools & gcc
RUN apt-get update && apt-get -y install netcat && apt-get -y install curl && apt-get clean

# set working directory
RUN mkdir -p /usr/apm
WORKDIR /usr/apm

RUN curl -L -O https://artifacts.elastic.co/downloads/apm-server/apm-server-6.4.2-amd64.deb
RUN dpkg -i apm-server-6.4.2-amd64.deb
RUN rm apm-server-6.4.2-amd64.deb

# run apm server
COPY ./docker/monitoring/apm/entrypoint.sh /usr/apm/entrypoint.sh
CMD ["/usr/apm/entrypoint.sh"]

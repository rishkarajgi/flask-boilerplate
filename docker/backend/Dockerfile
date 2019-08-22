FROM phusion/baseimage:0.11

RUN useradd --user-group --create-home --home-dir /flask --shell /bin/false flask
RUN apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys 561F9B9CAC40B2F7
RUN curl https://www.postgresql.org/media/keys/ACCC4CF8.asc | apt-key add -
RUN add-apt-repository ppa:jonathonf/python-3.6
RUN sh -c 'echo deb https://oss-binaries.phusionpassenger.com/apt/passenger bionic main > /etc/apt/sources.list.d/passenger.list'
RUN sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt/ $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list'

RUN apt-get update

RUN apt-get install -y make gcc g++ libxml2-dev libxslt-dev libffi-dev \
  musl-dev software-properties-common postgresql-common postgresql-11 \
  tzdata ssl-cert sysstat postgresql-client-common libossp-uuid16 iputils-ping \
  python3.6 python3-pip build-essential libssl-dev libxslt1-dev netcat \
  zlib1g-dev passenger dirmngr gnupg apt-transport-https ca-certificates

RUN apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

RUN passenger-config validate-install

ENV PYTHONUNBUFFERED 1

WORKDIR /flask/src

COPY ./requirements-dev.txt requirements-dev.txt
RUN pip3 install --no-cache-dir -r requirements-dev.txt

COPY ./requirements.txt requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt

USER flask

RUN mkdir -p /flask/.cache /flask/.local/share

COPY ./docker/backend/docs-entrypoint.sh /
COPY ./docker/backend/celery-beat-entrypoint.sh /
COPY ./docker/backend/celery-worker-entrypoint.sh /
COPY ./docker/backend/flask-entrypoint.sh /flask-entrypoint.sh

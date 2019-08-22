#!/bin/sh

test -e celerybeat.pid && rm celerybeat.pid
test -e celerybeat-schedule && rm celerybeat-schedule

while ! nc -z postgres 5432; do
  echo "Waiting for postgres to be ready..."
  sleep 2
done

while ! nc -z redis 6379; do
  echo "Waiting for redis to be ready..."
  sleep 2
done

if ping -c 1 -W 1 apm; then
  while ! nc -z apm 8200; do
    echo "Waiting for apm..."
    sleep 2
  done
fi

celery beat -A passenger_wsgi.celery -l info

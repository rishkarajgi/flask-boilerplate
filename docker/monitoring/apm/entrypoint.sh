#!/bin/sh

while ! nc -z elk 9200; do
  sleep 2
  echo "Waiting for elk..."
done

echo "elk started"

apm-server -e -E apm-server.host=0.0.0.0:8200 -E output.elasticsearch.hosts=elk:9200

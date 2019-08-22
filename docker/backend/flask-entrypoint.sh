#!/bin/sh

test -e backend/config.py || (
    echo "WARNING: config.py not found, using default" &&
        cp backend/config.example.py backend/config.py
)

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

# python3 manage.py db fixtures fixtures.json --reset

# until python3 manage.py run --host 0.0.0.0 --port 5000; do
#     echo "Waiting for code to be fixed..."
#     sleep 5
# done

passenger start --port 5000 --log-file server.log

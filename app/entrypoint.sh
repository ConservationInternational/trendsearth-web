#!/bin/bash
set -e

case "$1" in
    develop)
        echo "Running Development Server"
        exec python manage.py migrate && gunicorn main.wsgi:application --bind 0.0.0.0:9000
        ;;
    start)
        echo "Running Start"
        exec gunicorn main.wsgi:application --bind 0.0.0.0:9000
        ;;
    *)
        exec "$@"
esac

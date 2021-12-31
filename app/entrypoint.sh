#!/bin/bash
set -e

case "$1" in
    develop)
        echo "Running Development Server"
        exec python manage.py migrate && gunicorn -c gunicorn.py gefapi.wsgi:application
        ;;
    start)
        echo "Running Start"
        exec gunicorn -c gunicorn.py gefapi.wsgi:application
        ;;
    *)
        exec "$@"
esac

#!/bin/bash

APP_PORT = ${PORT:-8000}
python manage.py collectstatic --no-input
python manage.py makemigrations
python manage.py migrate  --noinput
python manage.py initadmin
gunicorn config.wsgi:application --bind "0.0.0.0:${APP_PORT}" --log-level debug
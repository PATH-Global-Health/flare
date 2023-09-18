#!/bin/bash

gunicorn --workers=3 config.wsgi:application --bind "0.0.0.0:8000" --worker-tmp-dir /dev/shm --log-level info
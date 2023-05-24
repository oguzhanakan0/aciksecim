#!/bin/sh

cd /app

python manage.py migrate

gunicorn src.wsgi --bind=0.0.0.0:8000 --log-level CRITICAL
#!/bin/sh

python ./manage.py makemigrations authentication --no-input
python ./manage.py makemigrations litreview --no-input
python ./manage.py migrate --no-input
python ./manage.py collectstatic --no-input --clear

gunicorn oc_projet9_appli_web_django.wsgi:application --bind 0.0.0.0:8000

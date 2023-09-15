# original source: https://testdriven.io/blog/dockerizing-django-with-postgres-gunicorn-and-nginx/
# we use psycopg3, there is no need to pre-compile anything. Just install psycopg3 and psycopg-binary
# See: https://www.psycopg.org/psycopg3/docs/basic/install.html

# pull official base image
FROM python:3.10.1-alpine

# create directory for the app user and create the app user
RUN mkdir -p /home/app; \
    addgroup -S app; \
    adduser -S app -G app

# create the appropriate directories
ENV HOME=/home/app
ENV APP_HOME=/home/app/web
RUN mkdir $APP_HOME; \
    mkdir /var/log/gunicorn; \
    mkdir $APP_HOME/staticfiles; \
    mkdir $APP_HOME/mediafiles
WORKDIR $APP_HOME

# install dependencies
COPY ./requirements.txt .

RUN apk update; \
    apk add libpq; \
    apk add bash; \
    apk add postgresql-client; \
    pip install -U pip; \
    pip install --no-cache -r requirements.txt

# copy project
COPY . $APP_HOME

# copy media files
COPY ./media/* $APP_HOME/mediafiles

# chown all the files to the app user
RUN chown -R app:app $APP_HOME

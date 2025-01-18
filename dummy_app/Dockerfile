# original source: https://testdriven.io/blog/dockerizing-django-with-postgres-gunicorn-and-nginx/
# we use psycopg3, there is no need to pre-compile anything. Just install psycopg3 and psycopg-binary
# See: https://www.psycopg.org/psycopg3/docs/basic/install.html

# pull official base image
FROM python:3.12.8-alpine3.19

# create directory for the dummy-operator user and create the dummy-operator user
RUN mkdir -p /home/dummy-operator; \
    addgroup -S dummy-operator; \
    adduser -S dummy-operator -G dummy-operator

# create the appropriate directories
ENV HOME=/home/dummy-operator
ENV APP_HOME=/home/dummy-operator/web
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

# chown all the files to the dummy-operator user
RUN chown -R dummy-operator:dummy-operator $APP_HOME

USER dummy-operator

# syntax=docker/dockerfile:1
FROM python:3.8
ENV PYTHONUNBUFFERED=1

# create directory for the app user
# RUN mkdir -p /home/app

# create the app user
RUN groupadd -g 1000 app && useradd -g app -s /bin/sh app

# install packages
RUN apt-get update && apt-get install -y \
	python-dev \
	libsasl2-dev \
	libssl-dev
RUN apt-get update && apt-get install -y \
	binutils \
	libproj-dev \
	gdal-bin \
	postgresql-client

RUN pip install https://github.com/ConservationInternational/trends.earth-schemas/archive/refs/heads/master.zip

COPY ./requirements.txt $APP_HOME
COPY ./wait_for_postgres.sh $APP_HOME
RUN pip install -r requirements.txt

ENV HOME=/home/
ENV APP_HOME=/home/app
RUN mkdir $APP_HOME
WORKDIR $APP_HOME


COPY ./requirements.txt $APP_HOME
RUN pip install -r requirements.txt

# copy project
COPY . $APP_HOME

# chown all the files to the app user
RUN chown -R app:app $APP_HOME/*
# RUN chown -R www-data:www-data $APP_HOME/*

# change to the app user
EXPOSE 9000
USER app

ENTRYPOINT ["./wait_for_postgres.sh", "postgresdb", "./entrypoint.sh"]

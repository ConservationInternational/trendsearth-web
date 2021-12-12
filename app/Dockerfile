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
	gdal-bin

RUN pip install https://github.com/ConservationInternational/trends.earth-schemas/archive/refs/heads/master.zip

# RUN apt-get install software-properties-common -y && apt-get update
# RUN add-apt-repository ppa:ubuntugis/ppa && apt-get update
# RUN apt-get update
# RUN apt-get install -y gdal-bin
# RUN apt-get install -y libgdal-dev
# RUN export CPLUS_INCLUDE_PATH=/usr/include/gdal
# RUN export C_INCLUDE_PATH=/usr/include/gdal
# RUN pip install GDAL

COPY ./requirements.txt $APP_HOME
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
USER app


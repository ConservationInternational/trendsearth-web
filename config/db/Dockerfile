FROM postgres:15

RUN apt-get update \
    && apt-get install wget -y \
    && apt-get install postgresql-15-postgis-3 -y \
    && apt-get install postgis -y

# COPY ./populate.sql /home/populate.sql

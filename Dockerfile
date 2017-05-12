FROM ubuntu:trusty
#dockerhub
RUN apt-get update -qq
RUN apt-get install -y socat git software-properties-common python-software-properties postgresql-client-9.3 postgresql-client-common

RUN apt-get update -qq
RUN apt-get install -y python-pip python-psycopg2 libpq-dev python2.7-dev gunicorn libmagic1

RUN mkdir /code
ADD . /code/
WORKDIR /code
RUN pip install -r requirements.txt
RUN pip install -U flask-cors

EXPOSE 5000

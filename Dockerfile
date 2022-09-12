FROM python:3.10-slim-buster
MAINTAINER Jonathan Finger

ENV INSTALL_PATH /sniffr
RUN mkdir -p $INSTALL_PATH


WORKDIR $INSTALL_PATH

RUN apt-get update
RUN apt-get -y install gcc

RUN pip install --upgrade pip

RUN pip install libpq5
RUN pip install psycopg2-binary

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .


CMD gunicorn -b 0.0.0.0:8000 --access-logfile "sniffr.app:create_app()"
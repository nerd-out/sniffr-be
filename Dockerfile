FROM python:3.10-slim-buster
MAINTAINER Jonathan Finger

ENV INSTALL_PATH /sniffr
RUN mkdir -p $INSTALL_PATH

WORKDIR $INSTALL_PATH

RUN apt-get update
RUN apt-get -y install gcc

RUN pip install --upgrade pip

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

RUN flask db init
RUN flask db migrate
RUN flask db upgrade
RUN python seed_db.py

CMD gunicorn -b 0.0.0.0:8000 --access-logfile "sniffr.app:create_app()"
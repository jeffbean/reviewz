FROM python:3.3
MAINTAINER jeffreyrobertbean@gmail.com

ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
ADD requirements.txt /code/
RUN pip install -r requirements.txt

ADD . /code/
RUN python /code/manage.py collectstatic --noinput

VOLUME /code/cstatic
EXPOSE 8001

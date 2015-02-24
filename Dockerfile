FROM python:3.3
MAINTAINER jeffreyrobertbean@gmail.com
ENV http_proxy http://rproxy.mcp.com:3128
ENV https_proxy http://rproxy.mcp.com:3128
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
ADD requirements.txt /code/
RUN pip install -r requirements.txt
ENV http_proxy ""
ENV https_proxy ""
ADD . /code/
RUN python /code/manage.py collectstatic --noinput

VOLUME /code/cstatic
EXPOSE 8001
FROM python:3.9.0-alpine

# https://docs.python.org/3/using/cmdline.html#cmdoption-u
ENV PYTHONUNBUFFERED 1

RUN apk add --update --no-cache postgresql-client python3-dev

RUN apk add --update --no-cache --virtual .tmp-build-deps \
  gcc libc-dev linux-headers postgresql-dev g++

RUN mkdir /psinsightsmasscrawler
WORKDIR /psinsightsmasscrawler

ADD requirements.txt /psinsightsmasscrawler
RUN pip install -r ./requirements.txt
RUN apk del .tmp-build-deps

ADD psinsightsmasscrawler/ /psinsightsmasscrawler

RUN adduser -D user
RUN chown -R user:user .
USER user

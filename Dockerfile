FROM python:3.7-alpine
LABEL maintainer="orion@leadverticals.com"

ENV PYTHONUNBUFFERED 1
ENV PROJECT_ROOT /ccvalidate

COPY ./requirements.txt /requirements.txt
RUN apk add --update --no-cache postgresql-client
RUN apk add --update --no-cache --virtual .tmp-build-deps \
      gcc libc-dev linux-headers postgresql-dev
RUN pip install -r requirements.txt
RUN apk del .tmp-build-deps
RUN mkdir $PROJECT_ROOT
WORKDIR $PROJECT_ROOT
COPY .$PROJECT_ROOT $PROJECT_ROOT
RUN chmod 666 $PROJECT_ROOT/.coverage

RUN adduser -D user
USER user
#CMD python manage.py runserver 0.0.0.0:8000
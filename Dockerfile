# pull official base image
FROM python:3.10.5-alpine

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install psycopg2 dependencies
RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev \
    cairo-dev cairo cairo-tools

RUN apk add jpeg-dev zlib-dev freetype-dev lcms2-dev openjpeg-dev tiff-dev tk-dev tcl-dev

# install dependencies
RUN pip install --upgrade pip
COPY . .
RUN pip install pip-tools
RUN pip-compile --upgrade
RUN pip-sync
FROM python:3.8

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /Mobin

COPY requirements.txt /Mobin/

RUN pip install -r requirements.txt

COPY . /Mobin/
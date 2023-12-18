FROM python:3.10-buster

ENV PYTHONUNBUFFERED 1

WORKDIR /code
COPY . .
RUN pip3 install -r /code/requirements.txt


EXPOSE 8080

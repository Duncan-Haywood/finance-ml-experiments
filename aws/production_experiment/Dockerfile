# syntax=docker/dockerfile:1
From python:3.8-slim-buster

WORKDIR /src

COPY . .

RUN pip3 install -r requirements.txt


ENTRYPOINT ["python3", "run.sh"]
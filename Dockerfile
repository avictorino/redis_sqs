FROM python:3.9.1-slim
RUN mkdir /app
WORKDIR /app
ADD . /app

RUN \
 apt-get update -y -qq && \
 pip install --upgrade --quiet pip

RUN pip install -r requirements.txt --quiet

RUN apt-get clean
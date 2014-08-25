FROM ubuntu:14.04

MAINTAINER Dave Beckett <dave@dajobe.org>

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update
RUN apt-get -y install python

ADD receive.py /receive.py
ADD common.py /common.py

EXPOSE 5005

CMD ["python", "/receive.py"]

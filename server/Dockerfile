# Dockerfile
FROM python:3.9

WORKDIR /app
COPY *.sh /app
COPY *.py /app

RUN apt-get update && \
    apt-get install -y tcpdump && \
    chmod a+x start.sh

USER root

CMD /bin/bash -c /app/start.sh
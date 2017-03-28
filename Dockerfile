FROM debian:8.7

MAINTAINER Ivan Ermilov <ivan.s.ermilov@gmail.com>

RUN apt-get update && apt-get -y upgrade
RUN apt-get install -y python3 python3-pip git

RUN pip3 install --upgrade pip
RUN pip3 install docker
RUN pip3 install rdflib
RUN pip3 install pytz

ENV DOCKER_ENDPOINT tcp://192.168.122.2:4000
ENV TIMEZONE Europe/Berlin
ENV VIRTUOSO_ENDPOINT http://localhost:8890/sparql-auth
ENV DBA_USERNAME dba
ENV DBA_PASSWORD dba
ENV DEFAULT_GRAPH_URI http://example.com/

RUN git clone https://github.com/earthquakesan/docker-event2rdf /docker-event2rdf
WORKDIR /docker-event2rdf

CMD ["python3", "dockerevent2rdf/run.py"]

# docker-event2rdf
## Description
This application reads the event from docker engine, transform it to RDF triples and push the data to Virtuoso triplestore.

## Example Setup
```
version: "2"
services:
  event2rdf:
    restart: always
    build: .
    environment:
      - DOCKER_ENDPOINT=tcp://192.168.122.2:4000
      - TIMEZONE=Europe/Berlin
      - VIRTUOSO_ENDPOINT=http://my-virtuoso:8890/sparql-auth
      - DBA_USERNAME=dba
      - DBA_PASSWORD=dba
      - DEFAULT_GRAPH_URI=http://example.com/
  my-virtuoso:
    image: tenforce/virtuoso
    environment:
      - DBA_PASSWORD=dba
      - SPARQL_UPDATE=true
      - DEFAULT_GRAPH=http://example.com/
    volumes:
      - ./virtuoso/db:/data
    ports:
      - 1111:1111
      - 8890:8890
```
The events will be saved in http://example.com/ graph.
For TIMEZONE variable please refer to [pytz documentation](https://pypi.python.org/pypi/pytz).
DOCKER_ENDPOINT should be specified to a running docker engine endpoint (i.e. docker swarm in this case).

## Events
The RDF schema of events is described in [events.owl](./events.owl) file.
For examples of events as received from Docker Engine see [container-lifecycle.md](container-lifecycle.md).

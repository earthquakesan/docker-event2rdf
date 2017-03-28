import os

from event import Event
from event2rdf import Event2RDF
from event_listener import EventListener
from virtuoso_connector import VirtuosoConnector

docker_endpoint = os.environ["DOCKER_ENDPOINT"]
timezone = os.environ["TIMEZONE"]
event_listener = EventListener(docker_endpoint)

virtuoso_endpoint = os.environ["VIRTUOSO_ENDPOINT"]
username = os.environ["DBA_USERNAME"]
password = os.environ["DBA_PASSWORD"]
default_graph_uri = os.environ["DEFAULT_GRAPH_URI"]
virtuoso_connector = VirtuosoConnector(
    endpoint=virtuoso_endpoint,
    username=username,
    password=password,
    default_graph_uri=default_graph_uri
)

for event_bytestring in event_listener.listen():
    event = Event(event_bytestring)
    e2rdf = Event2RDF(timezone=timezone)
    e2rdf.add_event_to_graph(event.event)
    ntriples = e2rdf.serialize().decode("utf-8")
    virtuoso_connector.insert_triples(ntriples)

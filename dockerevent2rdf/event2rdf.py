import datetime
import pytz

from rdflib import Graph, Literal, BNode, RDF
from rdflib.namespace import OWL, XSD, RDFS
from rdflib.namespace import Namespace

DOCKEVENT = Namespace('http://ontology.aksw.org/dockevent/')
DOCKEVENT_TYPES = Namespace('http://ontology.aksw.org/dockevent/types/')
DOCKEVENT_ACTIONS = Namespace('http://ontology.aksw.org/dockevent/actions/')
DOCKEVENT_ACTORS = Namespace('http://ontology.aksw.org/dockevent/actors/')

class Event2RDF(object):
    def __init__(self, timezone="Europe/Berlin"):
        self.timezone = pytz.timezone(timezone)
        self.store = self.init_store()

    def init_store(self):
        store = Graph()
        store.bind("owl", OWL)
        store.bind("xsd", XSD)
        store.bind("rdfs", RDFS)
        store.bind("dockevent", DOCKEVENT)
        store.bind("dockevent_types", DOCKEVENT_TYPES)
        store.bind("dockevent_action", DOCKEVENT_ACTIONS)
        store.bind("dockevent_actors", DOCKEVENT_ACTORS)
        return store

    def add_event_to_graph(self, event):
        event_id = event.get("id", "")
        if event_id == "":
            return None

        _time = event.get("time", "")
        _timeNano = event.get("timeNano", "")
        _datetime = datetime.datetime.fromtimestamp(int(_time), self.timezone)

        event_id = "%s_%s" % (event_id, _timeNano)
        event_node = self.store.resource("dockevent:%s" % event_id)
        event_node.add(DOCKEVENT.eventId, Literal(event_id, datatype=XSD.string))
        event_node.add(DOCKEVENT.time, Literal(_time, datatype=XSD.int))
        event_node.add(DOCKEVENT.timeNano, Literal(_timeNano, datatype=XSD.int))
        event_node.add(DOCKEVENT.dateTime, Literal(_datetime.isoformat(), datatype=XSD.string))


        event_type = event.get("Type", "")
        if event_type == "container":
            event_node.add(DOCKEVENT.type, DOCKEVENT_TYPES.container)
        elif event_type == "network":
            event_node.add(DOCKEVENT.type, DOCKEVENT_TYPES.network)
        elif event_type == "plugin":
            event_node.add(DOCKEVENT.type, DOCKEVENT_TYPES.plugin)
        elif event_type == "volume":
            event_node.add(DOCKEVENT.type, DOCKEVENT_TYPES.volume)

        event_action = event.get("Action", "")
        if ":" in event_action:
            event_action_type = event_action.split(":")[0]
            event_action_extra = event_action.split(":")[-1].strip()
            event_node.add(DOCKEVENT.actionExtra, Literal(event_action_extra, datatype=XSD.string))
        else:
            event_action_type = event_action

        if event_action_type == "create":
            event_node.add(DOCKEVENT.action, DOCKEVENT_ACTIONS.create)
        elif event_action_type == "attach":
            event_node.add(DOCKEVENT.action, DOCKEVENT_ACTIONS.attach)
        elif event_action_type == "connect":
            event_node.add(DOCKEVENT.action, DOCKEVENT_ACTIONS.connect)
        elif event_action_type == "start":
            event_node.add(DOCKEVENT.action, DOCKEVENT_ACTIONS.start)
        elif event_action_type == "resize":
            event_node.add(DOCKEVENT.action, DOCKEVENT_ACTIONS.resize)
        elif event_action_type == "exec_create":
            event_node.add(DOCKEVENT.action, DOCKEVENT_ACTIONS.exec_create)
        elif event_action_type == "exec_start":
            event_node.add(DOCKEVENT.action, DOCKEVENT_ACTIONS.exec_start)
        elif event_action_type == "health_status":
            event_node.add(DOCKEVENT.action, DOCKEVENT_ACTIONS.health_status)
        elif event_action_type == "die":
            event_node.add(DOCKEVENT.action, DOCKEVENT_ACTIONS.die)
        elif event_action_type == "destroy":
            event_node.add(DOCKEVENT.action, DOCKEVENT_ACTIONS.destroy)

        actor = event.get("Actor", "")
        if actor != "":
            actor_id = actor.get("ID", "")
            actor_id = "%s_%s" % (actor_id, _timeNano)
            actor_node = self.store.resource("dockevent_actors:%s" % actor_id)
            actor_node.add(DOCKEVENT.actorId, Literal(actor_id, datatype=XSD.dateTime))
            actor_attributes = actor.get("Attributes", "")
            if actor_attributes != "":
                image = actor_attributes.get("image", "")
                actor_node.add(DOCKEVENT.image, Literal(image, datatype=XSD.string))
                name = actor_attributes.get("name", "")
                actor_node.add(DOCKEVENT.name, Literal(name, datatype=XSD.string))
                swarm_ip_port = actor_attributes.get("node.addr", "")
                actor_node.add(DOCKEVENT.nodeIpPort, Literal(swarm_ip_port, datatype=XSD.string))
                node_id = actor_attributes.get("node.id", "")
                actor_node.add(DOCKEVENT.nodeId, Literal(node_id, datatype=XSD.string))
                node_ip = actor_attributes.get("node.ip", "")
                actor_node.add(DOCKEVENT.nodeIp, Literal(node_ip, datatype=XSD.string))
                node_name = actor_attributes.get("node.name", "")
                actor_node.add(DOCKEVENT.nodeName, Literal(node_name, datatype=XSD.string))
            event_node.add(DOCKEVENT.actor, actor_node)

        _from = event.get("from", "")
        if _from != "":
            event_node.add(DOCKEVENT.source, Literal(_from))

    def serialize(self):
        return self.store.serialize(format="ntriples")

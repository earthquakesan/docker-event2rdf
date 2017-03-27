import json

class Event(object):
    def __init__(self, event_bytestring):
        self.event = self.parse_to_json(event_bytestring)

    def parse_bytestring(self, bytestring):
        return bytestring.decode("utf-8")

    def parse_to_json(self, bytestring):
        return json.loads(self.parse_bytestring(bytestring))

import docker

class EventListener(object):
    def __init__(self, docker_endpoint):
        self.api_client = docker.APIClient(base_url=docker_endpoint, timeout=None)

    def listen(self):
        for event in self.api_client.events(filters={"type":"container"}):
            yield event

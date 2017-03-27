import requests
from requests.auth import HTTPDigestAuth

class VirtuosoConnector(object):
    formats = {
        "Auto": "auto",
        "HTML": "text/html",
        "HTML (Basic Browsing Links)": "text/x-html+tr",
        "Spreadsheet": "application/vnd.ms-excel",
        "XML": "application/sparql-results+xml",
        "JSON": "application/sparql-results+json",
        "Javascript": "application/javascript",
        "Turtle": "text/turtle",
        "RDF/XML": "application/rdf+xml",
        "N-Triples": "text/plain",
        "CSV": "text/csv",
        "TSV": "text/tab-separated-values"
    }
    def __init__(
        self,
        endpoint="http://localhost:8890/sparql-auth",
        username="dba",
        password="dba",
        default_graph_uri="http://example.com/"
    ):
        self.endpoint = endpoint
        self.username = username
        self.password = password
        self.default_graph_uri = default_graph_uri

    def query(self, query):
        payload = {
            "query": query,
            "default-graph-uri": self.default_graph_uri,
            "format": self.formats["CSV"],
            "timeout": "0",
            "debug": "on"
        }
        r = requests.get(
            self.endpoint,
            auth=HTTPDigestAuth(self.username, self.password),
            params=payload
        )
        r.raise_for_status()
        return r.content

    def insert_triples(self, ntriples):
        insert_query = """INSERT {%s};""" %(ntriples,)
        response = self.query(insert_query)
        #TODO: check for failure

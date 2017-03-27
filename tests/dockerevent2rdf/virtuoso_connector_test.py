import unittest
import os

from dockerevent2rdf.virtuoso_connector import VirtuosoConnector

class VirtuosoConnectorTest(unittest.TestCase):
    def setUp(self):
        endpoint = os.environ["VIRTUOSO_ENDPOINT"]
        username = os.environ["DBA_USERNAME"]
        password = os.environ["DBA_PASSWORD"]
        default_graph_uri = os.environ["DEFAULT_GRAPH_URI"]
        self.virtuoso_connector = VirtuosoConnector(
            endpoint=endpoint,
            username=username,
            password=password,
            default_graph_uri=default_graph_uri
        )

    def testInsert(self):
        insert_query = """INSERT {  <http://example.com/dataspace/Kingsley#this>
                      <http://rdfs.org/sioc/ns#id>
                      <Kingsley> };"""
        response = self.virtuoso_connector.query(insert_query)
        print(response.decode("utf-8"))
        select_query = """SELECT * { ?s ?p ?o }"""
        response = self.virtuoso_connector.query(select_query)
        print(response.decode("utf-8"))

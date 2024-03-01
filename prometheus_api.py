import logging
import logging as LOG
from datetime import datetime


class Prometheus_Api:

    def __init__(self, queries: list, pods: list, namespaces: list):
        LOG.basicConfig(level=logging.INFO)
        LOG.info(f"{datetime.now()}| Prometheus-Api object created")
        #queries with variables for pods and namespaces
        self.queries = queries
        self.pods = pods
        self.namespaces = namespaces


    def prepare_queries(self):
        #create a list of lists in which every query is filles with namespace and pod options
        #the variations of that query are then put in a list
        refined_queries = []
        for query in self.queries:
            for namespace in self.namespaces:



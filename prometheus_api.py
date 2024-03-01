import logging
import logging as LOG
from datetime import datetime
from prometheus_api_client import PrometheusConnect
import requests


class Prometheus_Api:
    BASE_URL = "http://localhost"
    PORT = 9090
    BASE_PATH = "/api/v1/query?query="

    def __init__(self, queries: list[str], pods: list, namespaces: list[str]):
        LOG.basicConfig(level=logging.INFO)
        LOG.info(f"{datetime.now()}| Prometheus-Api object created")
        # queries with variables for pods and namespaces
        self.queries = queries
        self.pods = pods
        self.namespaces = namespaces
        self.refined_queries = None

    def prepare_queries(self):
        # create a list of lists in which every query is filles with namespace and pod options
        # the variations of that query are then put in a list
        refined_queries = []
        for query in self.queries:
            refined_queries_query = []
            for namespace in self.namespaces:
                refined_query = query.replace("$namespace", namespace)
                namespace_pods = list(filter(lambda pod: (pod.metadata.namespace == namespace), self.pods))
                for pod in namespace_pods:
                    refined_query = refined_query.replace("$pod", pod.metadata.name)
                    refined_queries_query.append(refined_query)
            refined_queries.append(refined_queries_query)
        self.refined_queries = refined_queries
        LOG.info(f"{datetime.now()}| Refined prometheus queries")

    def fetch_data(self):
        prometheus = PrometheusConnect(url=Prometheus_Api.BASE_URL+f":{Prometheus_Api.PORT}", disable_ssl=True)
        LOG.info(f"{datetime.now()}| Trying to query prometheus with: {self.refined_queries[6][0]}")
        return prometheus.custom_query(self.refined_queries[6][0])
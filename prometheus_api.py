import logging
import logging as LOG
from datetime import datetime


class Prometheus_Api:

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
            for namespace in self.namespaces:
                refined_query = query.replace("$namespace", namespace)
                namespace_pods = list(filter(lambda pod: (pod.metadata.namespace == namespace), self.pods))
                for pod in namespace_pods:
                    refined_query = refined_query.replace("$pod", pod.metadata.name)
                    refined_queries.append(refined_query)
                    LOG.info(
                        f"{datetime.now()}| created refined query for pod: {pod.metadata.name} in namespace: {namespace}")
        self.refined_queries = refined_queries


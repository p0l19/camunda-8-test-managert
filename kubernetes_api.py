from datetime import datetime
from kubernetes import client, config
import logging
import logging as LOG


class Kubernetes_Api:

    def __init__(self, namespace: str):
        LOG.basicConfig(level=logging.INFO)
        LOG.info(f"{datetime.now()}| Kubernetes-Api object created")
        self.namespace = namespace

    def getPods(self) -> list:
        config.load_kube_config()
        v1 = client.CoreV1Api()
        LOG.info(f"{datetime.now()}| Looking for pods in namespace {self.namespace}")
        ret = v1.list_namespaced_pod(namespace=self.namespace, watch=False)
        pods = []
        for i in ret.items:
            LOG.info(f"| Found Pod: {i.status.pod_ip} / {i.metadata.namespace} / {i.metadata.name}")
            pods.append(i)
        return pods


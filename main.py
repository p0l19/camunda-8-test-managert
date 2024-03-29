import logging
import requests
import json
import time
from datetime import datetime
import logging as LOG
from expression_export import get_expressions
from operate_api import Operate_Api
from kubernetes_api import Kubernetes_Api
from prometheus_api import Prometheus_Api

# 0. get the pods (their names) of namespace "camunda-platform"
#
# 1. Call the exposed api to start the test process
#
# 2. stream the data (operate, zeebe, kepler/prometheus) for a
# fixed time intervall or as long as operate has running process instances
#
# 3. parse the data from the different
# sources together in a data modele which includes a time-stamp, the number of running instances, the power metrics
#
# Api for pormetheus: localhost:9090/api/v1/query

BASE_URL = "http://localhost"
NAME_SPACE = "camunda-platform"
CAMUNDA_VERSION = "camunda_8"


def startUp() -> bool:
    port = 8080
    amount = 1
    path = f"/process/start/{amount}"
    url = BASE_URL + f":{port}" + path
    LOG.info("Starting Test")
    start_response = requests.get(url)
    start_timestamp = datetime.now()
    status_code = start_response.status_code
    success = False
    if status_code / 100 == 2:
        success = True

    LOG.info(f"{start_timestamp} | Test started, success: {success}, status code: {status_code}")
    return success


if __name__ == "__main__":
    LOG.basicConfig(level=logging.INFO)
    kube_info = Kubernetes_Api(NAME_SPACE)
    pods = kube_info.getPods()
    prometheus_api = Prometheus_Api(queries=get_expressions(), pods=pods, namespaces=[NAME_SPACE])
    prometheus_api.prepare_queries()
    operate_api = Operate_Api()
    startUp()

    # create a csv-file that will hold the data for the test run
    formatted_datetime = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    path = f"{CAMUNDA_VERSION}_test_run_{formatted_datetime}.json"
    time.sleep(5)
    with open(f"data/{path}", "a") as test_run_data:
        running = True
        test_data = {}
        while running:
            running = operate_api.processes_running()[0]
            data = prometheus_api.fetch_data()
            LOG.info(data)
            test_data[datetime.now().strftime("%Y-%m-%d_%H-%M-%S")] = data
            time.sleep(3.0)
        json.dump(test_data, test_run_data)

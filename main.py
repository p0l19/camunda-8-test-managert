import logging

import requests
import datetime
import logging as LOG
from requests.auth import HTTPBasicAuth
from requests.cookies import RequestsCookieJar

# 1. Call the exposed api to start the test process
#
# 2. stream the data (operate, zeebe, kepler/prometheus) for a
# fixed time intervall or as long as operate has running process instances
#
# 3. parse the data from the different
# sources together in a data modele which includes a time-stamp, the number of running instances, the power metrics


BASE_URL = "http://localhost"


def startUp() -> bool:
    port = 8080
    amount = 1
    path = f"/process/start/{amount}"
    url = BASE_URL + f":{port}" + path
    LOG.info("Starting Test")
    start_response = requests.get(url)
    start_timestamp = datetime.datetime.now()
    status_code = start_response.status_code
    success = False
    if status_code / 100 == 2:
        success = True

    LOG.info(f"{start_timestamp} | Test started, success: {success}, status code: {status_code}")
    return success


def operate_auth() -> RequestsCookieJar:
    login_data = "demo"
    port = 8081
    path = f"/api/login?username={login_data}&password={login_data}"
    url = BASE_URL + f":{port}" + path
    LOG.info(f"{datetime.datetime.now()} | Trying to obtain auth cookie for operate")
    auth_response = requests.post(url="http://localhost:8081/api/login?username=demo&password=demo")
    LOG.info(f'{datetime.datetime.now()} | Got operate auth with cookie')
    return auth_response.cookies


def processes_running() -> (bool, int):
    port = 8081
    path = "/v1/process-instances/search"
    body = '{"filter": {"state": "ACTIVE"}}'
    url = BASE_URL + f":{port}" + path
    headers = {"accept": "application/json", "Content-Type": "application/json"}
    operate_request = requests.post(url=url, data=body, headers=headers, cookies=operate_auth())
    active_count = operate_request.json()["total"]
    LOG.info(f"{datetime.datetime.now()}| Found {active_count} active instances")
    return active_count > 0, active_count


if __name__ == "__main__":
    LOG.basicConfig(level=logging.INFO)
    startUp()
    while processes_running():


from datetime import datetime
import logging as LOG
import logging
import requests


class Operate_Api:
    BASE_URL = "http://localhost"
    PORT = 8081

    def __init__(self):
        self.cookies = None
        LOG.basicConfig(level=logging.INFO)
        LOG.info(f"{datetime.now()}| Operate-Api object created")

    def get_auth(self):
        login_data = "demo"
        path = f"/api/login?username={login_data}&password={login_data}"
        url = Operate_Api.BASE_URL + f":{Operate_Api.PORT}" + path
        LOG.info(f"{datetime.now()} | Trying to obtain auth cookie for operate")
        auth_response = requests.post(url=url)
        LOG.info(f'{datetime.now()} | Got operate auth with cookie')
        self.cookies = auth_response.cookies

    def processes_running(self) -> (bool, int):
        path = "/v1/process-instances/search"
        body = '{"filter": {"state": "ACTIVE"}}'
        url = Operate_Api.BASE_URL + f":{Operate_Api.PORT}" + path
        headers = {"accept": "application/json", "Content-Type": "application/json"}
        operate_request = requests.post(url=url, data=body, headers=headers, cookies=self.cookies)
        if operate_request.status_code == 401:
            self.get_auth()
            operate_request = requests.post(url=url, data=body, headers=headers, cookies=self.cookies)
        active_count = operate_request.json()["total"]
        LOG.info(f"{datetime.now()}| Found {active_count} active instances")
        return active_count > 0, active_count

from businessUtils.logUtils import LogLevel, log
from businessUtils.apiUtils import http_request

import requests
from typing import Any


class Client(object):
    def __init__(self):
        pass
    
    @http_request
    def send_get_request(self, url_endpoint: str, *args, **kwargs) -> Any:
        ''' send HTTP get request to `urlendpoint`'''
        log(LogLevel.INFO, f"Sending GET request to: {url_endpoint}. With arguments: args={args} kwargs={kwargs}.")
        response = requests.get(url_endpoint, *args, **kwargs)
        log(LogLevel.INFO, f"Received response from {url_endpoint}: {response.json()}")
        return response.json()


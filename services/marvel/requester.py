import hashlib
import time

import requests

from .endpoint import Endpoint
from .exceptions import BadInputException, MarvelException


class Requester(Endpoint):
    def __init__(self, private_key, public_key):
        super().__init__()
        self.private_key = private_key
        self.public_key = public_key

    def get_query_with_authentication_params(self, params=None):
        if params is None:
            params = {}
        timestamp = str(int(time.time()))
        string = timestamp + self.private_key + self.public_key
        hash_str = hashlib.md5(string.encode("utf8")).hexdigest()
        payload = {
            "ts": timestamp,
            "apikey": self.public_key,
            "hash": hash_str,
        }
        payload.update(params)
        return payload

    def request(self, endpoint, identifier=None, sub_endpoint=None, **kwargs):
        url = self.get_endpoint(endpoint)

        if identifier is not None:
            url = "{}/{}".format(url, identifier)
        if sub_endpoint is not None:
            url = "{}/{}".format(url, sub_endpoint)

        response = requests.get(url, self.get_query_with_authentication_params(kwargs))
        status = response.status_code

        data = response.json()
        self.check_exception(status, data)
        return data

    @staticmethod
    def check_exception(status, data):
        if status == 200:
            pass
        elif status == 409 or status == 401 or status == 405 or status == 403:
            raise MarvelException("{}".format(data["message"]))
        elif status == 404:
            raise BadInputException("{}".format(data["message"]))
        else:
            raise Exception(data)

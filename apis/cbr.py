from logging import getLogger

import requests
import json

logger = getLogger(__name__)

class CbrClient(object):

    def __init__(self):
        self.base_url = "https://www.cbr-xml-daily.ru/daily_json.js"

    def __request(self, method, params):
        url = self.base_url + method

    def get_ticker(self, pair):
        params = {
            "market": pair
        }
from logging import getLogger

import requests
import json

logger = getLogger(__name__)


class CbrError(Exception):
    '''Неизвесная ошибка при запросе API Cbr'''

class CbrRequestError(CbrError):
    '''Ошибка при некоректном запросе'''

class CbrClient(object):

    def __init__(self):
        self.base_url = "https://www.cbr-xml-daily.ru/daily_json.js"

    def __request(self, method, params):
        url = self.base_url + method

        try:
            r = requests.get(url=url, params=params)
            result = r.json()
        except Exception:
            logger.exception('CbrError')
            raise CbrError

        if result.get('saccess'):
            # Успешный запрос
            return result
        else:
            # Некоректный запрос
            logger.error('Request error: %s', result.get('message'))
            raise CbrRequestError

    def get_ticker(self, currency):
        params = {
            "market": currency
        }
        return self.__request(method='/public/gettiker', params=params)

    def get_last_rate(self, currency):
        res = self.get_ticker(currency=currency)
        return res['result']['Last']
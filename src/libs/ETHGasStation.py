import json
from requests import Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
from decouple import config

class ETH:
    def __init__(self):
        self.session = Session()
        self.headers = {
            'Accepts': 'application/json',
            'api-key': 'XX' + config('ETHGS-API-KEY') + 'XX',
        }
        self.session.headers.update(self.headers)
        self.url = {
            'DEFI_PULSE':'https://data-api.defipulse.com/',
            'GAS_STATION':'https://ethgasstation.info/api/ethgasAPI.json'
        }
        self.endpoints = {
            'EXAMPLE':'api/v1/egs/api/ethgasAPI.json',
            'GAS_PRICE':'api/ethgasAPI.json',
            'PREDICTION_TABLE':'api/predictTable.json'
        }
        
    def gasPrice(self):
        try:
            response = self.session.get(self.url['GAS_STATION'] + self.endpoints['GAS_PRICE'])
            request = json.loads(response.text)
            return request
        except (ConnectionError, Timeout, TooManyRedirects) as e:
            return e
            
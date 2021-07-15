import json
from requests import Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
from decouple import config

class CMC:
    def __init__(self):
        self.session = Session()
        self.headers = {
            'Accepts': 'application/json',
            'X-CMC_PRO_API_KEY': config('CMC-API-KEY'),
        }
        self.session.headers.update(self.headers)
        self.url = 'https://pro-api.coinmarketcap.com/'
        self.endpoints = {
            'LISTING_LATEST':'v1/cryptocurrency/listings/latest',
            'QUOTES_LATEST':'v1/cryptocurrency/quotes/latest'
        }
        self.Fiat = {
                'USD' : {'NAME':'United States Dollar','SYMBOL':'$'},
                'AUD' : {'NAME':'Australian Dollar','SYMBOL':'$'},
                'BRL' : {'NAME':'Brazilian Real','SYMBOL':'R$'},
                'CAD' : {'NAME':'Canadian Dollar','SYMBOL':'$'},
                'CHF' : {'NAME':'Swiss Franc','SYMBOL':'FR'},
                'CLP' : {'NAME':'Chilean Peso','SYMBOL':'$'},
                'CNY' : {'NAME':'Chinese Yuan','SYMBOL':'¥'},
                'CZK' : {'NAME':'Czech Koruna','SYMBOL':'KČ'},
                'DKK' : {'NAME':'Danish Krone','SYMBOL':'KR'},
                'EUR' : {'NAME':'Euro','SYMBOL':'€'},
                'GBP' : {'NAME':'Pound Sterling','SYMBOL':'£'},
                'HKD' : {'NAME':'Hong Kong Dollar','SYMBOL':'$'},
                'HUF' : {'NAME':'Hungarian Forint','SYMBOL':'FT'},
                'IDR' : {'NAME':'Indonesian Rupiah','SYMBOL':'RP'},
                'ILS' : {'NAME':'Israeli New Shekel','SYMBOL':'₪'},
                'INR' : {'NAME':'Indian Rupee','SYMBOL':'₹'},
                'JPY' : {'NAME':'Japanese Yen','SYMBOL':'¥'},
                'KRW' : {'NAME':'South Korean Won','SYMBOL':'₩'},
                'MXN' : {'NAME':'Mexican Peso','SYMBOL':'$'},
                'MYR' : {'NAME':'Malaysian Ringgit','SYMBOL':'RM'},
                'NOK' : {'NAME':'Norwegian Krone','SYMBOL':'KR'},
                'NZD' : {'NAME':'New Zealand Dollar','SYMBOL':'$'},
                'PHP' : {'NAME':'Philippine Peso','SYMBOL':'₱'},
                'PKR' : {'NAME':'Pakistani Rupee','SYMBOL':'₨'},
                'PLN' : {'NAME':'Polish Złoty','SYMBOL':'ZŁ'},
                'RUB' : {'NAME':'Russian Ruble','SYMBOL':'₽'},
                'SEK' : {'NAME':'Swedish Krona','SYMBOL':'KR'},
                'SGD' : {'NAME':'Singapore Dollar','SYMBOL':'S$'},
                'THB' : {'NAME':'Thai Baht','SYMBOL':'฿'},
                'TRY' : {'NAME':'Turkish Lira','SYMBOL':'₺'},
                'TWD' : {'NAME':'New Taiwan Dollar','SYMBOL':'NT$'},
                'ZAR' : {'NAME':'South African Rand','SYMBOL':'R'}
            }
        
    def listing_latest(self, **kwargs):
        parameters = {
            'market_cap_min':100000000,
            'percent_change_24h_min':5,
            'sort':'percent_change_24h',
            'sort_dir':'desc'
        }
        for key, value in kwargs.items():
            parameters.update({key: value})

        try:
            response = self.session.get(self.url + self.endpoints['LISTING_LATEST'], params=parameters)
            request = json.loads(response.text)
            return request
        except (ConnectionError, Timeout, TooManyRedirects) as e:
            return e

    def quotes_latest(self, **kwargs):
        parameters = dict()
        for key, value in kwargs.items():
            parameters.update({str(key): value})

        try:
            response = self.session.get(self.url + self.endpoints['QUOTES_LATEST'], params=parameters)
            request = json.loads(response.text)
            return request
        except (ConnectionError, Timeout, TooManyRedirects) as e:
            return e

    def exist_fiat(self, fiat):
        return True if fiat in list(self.Fiat.keys()) else False
    
    def fiat(self, fiat):
        return {fiat:self.Fiat[fiat]} if self.exist_fiat(fiat) else None
        
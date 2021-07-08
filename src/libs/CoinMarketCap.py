from os import truncate
import discord
import datetime
import requests
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
from decouple import config
import json

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
            
class Help:
    def __init__(self):
        self.colours = {
            'STABLE':{
                'STILL':int("DCDCDC", 16),
                'LIGHT':int("ABABAB", 16)
            },
            'LOSING':{
                'FEW':int("DE7875", 16),
                'NORMAL':int("BA4A45", 16),
                'BEAR':int("9D2F29", 16)
            },
            'WINNING':{
                'FEW':int("8CBF84", 16),
                'NORMAL':int("5C8456", 16),
                'BULL':int("315C32", 16)
            },
            'INFO':{
                'AZUL':int("3861FB",16)
            }
        }
        
    def currencyColorEmbed(self, value:float):
        # Colour palatte: https://coin360.com/about/presskit
        # Precio inmovil
        if value == 0:
            return self.colours['STABLE']['STILL']
        # Precio con mov ligero
        elif -0.2 < value and value < 0.2:
            return self.colours['STABLE']['LIGHT']
        # Precio con mov+
        elif value > 0.2:
            if value > 10:					# Verde +++
                return self.colours['WINNING']['BULL']
            elif value > 5:					# Verde ++
                return self.colours['WINNING']['NORMAL']
            else:							# Verde +
                return self.colours['WINNING']['FEW']
        # Precio con mov-
        elif value < -0.2:
            if value < -10:					# Rojo ---
                return self.colours['LOSING']['BEAR']
            elif value < -5:				# Rojo --
                return self.colours['LOSING']['NORMAL']
            else:							# Rojo -
                return self.colours['LOSING']['FEW']

    def currencyUrlEmbed(self, endpoint:str):
        if endpoint.find(' '):
            endpoint = endpoint.replace(' ','-')
        url = 'https://coinmarketcap.com/currencies/'
        r = requests.get(url= url + endpoint)
        return url + endpoint if r.status_code == 200 else url

    def currencyLogoEmbed(self, id:int):
        return f'https://s2.coinmarketcap.com/static/img/coins/64x64/{id}.png'

    def currencyCircEmbed(self, cData):
        circulating_supply = "`{:,.2f}`".format(cData['circulating_supply'])
        total_supply = "`{:,.2f}`".format(cData['total_supply'])
        max_supply = "`{:,.2f}`".format(cData['max_supply']) if cData['max_supply'] != None else '`unknown%`'

        name  = ("Circulating", "Total", "Max")
        value = (circulating_supply, total_supply, max_supply)

        return tuple(zip(name, value))
        
    def currencyPercEmbed(self, cData, converter):
        percent_24h = "`{:,.2f}%`".format(cData['quote'][converter]['percent_change_24h'])
        percent_7d  = "`{:,.2f}%`".format(cData['quote'][converter]['percent_change_7d'])
        percent_30d = "`{:,.2f}%`".format(cData['quote'][converter]['percent_change_30d'])

        name  = ("Percentaje 1d", "Percentaje 7d", "Percentaje 30d")
        value = (percent_24h, percent_7d, percent_30d)
        
        return tuple(zip(name, value))	

    def currencyEmbed(self, cData, symbol, converter, fiat):
        fiat_symbol = fiat[converter]['SYMBOL']
        embed = discord.Embed(
            title= cData['name'] + ' ' + symbol,
            description= "{}is located in the number {}of CoinMarketCap,\nand has a capitalization market of: {}{:,.2f}\n".format(cData['name'],cData['cmc_rank'],fiat_symbol,cData['quote'][converter]['market_cap']),
            url= self.currencyUrlEmbed(cData['name'].lower()),
            colour= self.currencyColorEmbed(cData['quote'][converter]['percent_change_1h'])
        )
        # Referencia
        embed.set_author(
            name= 	  'CoinMarketCap',
            url= 	  'https://coinmarketcap.com/',
            icon_url= 'https://coinmarketcap.com/public/media/img/logo-square.png?_=7719c19'
        )
        # Thumbnail
        embed.set_thumbnail(url= self.currencyLogoEmbed(cData['id']))
        # Informacion actual
        value = '```c++\nPrice \t\t\t{}{:,.2f}\nTrading Volume\t{}{:,.2f}\nLast Hour%\t\t{:,.2f}%```'.format(fiat_symbol, cData['quote'][converter]['price'], fiat_symbol, cData['quote'][converter]['volume_24h'],cData['quote'][converter]['percent_change_1h'])
        embed.add_field(
            name=  symbol + ' ' + 'Price Statistics',
            value= value,
            inline= 'false'
        )
        # Circulacion - Provisional
        Circ = self.currencyCircEmbed(cData)
        embed.add_field(name= Circ[0][0], value= Circ[0][1], inline= 'true')
        embed.add_field(name= Circ[1][0], value= Circ[1][1], inline= 'true')
        embed.add_field(name= Circ[2][0], value= Circ[2][1], inline= 'true')
        # Porcentajes - Provisional
        Perc = self.currencyPercEmbed(cData, converter)
        embed.add_field(name= Perc[0][0] ,value= Perc[0][1], inline='true')
        embed.add_field(name= Perc[1][0] ,value= Perc[1][1], inline='true')
        embed.add_field(name= Perc[2][0] ,value= Perc[2][1], inline='true')
        # Footer
        embed.set_footer(
            text='Last updated: ' + datetime.datetime.now().strftime("%d %b %Y at %X"),
            icon_url='https://icon-library.com/images/verified-icon-png/verified-icon-png-11.jpg'
        )
        return embed

    def fiatEmbed(self, fiat, values):
        embed = discord.Embed(
            title= fiat,
            description= "Full Name: `{}`\nSymbol: `{}`".format(values['NAME'], values['SYMBOL']),
            colour= self.colours['INFO']['AZUL']
        )
        # Referencia
        embed.set_author(
            name= 	  'CoinMarketCap',
            url= 	  'https://coinmarketcap.com/',
            icon_url= 'https://coinmarketcap.com/public/media/img/logo-square.png?_=7719c19'
        )
        return embed

    def hotCircEmbed(self, cData, converter, fiatSym):
        price = "`{}{:,.2f}`".format(fiatSym, cData['quote'][converter]['price'])
        trading_volume  = "`{}{:,.2f}`".format(fiatSym, cData['quote'][converter]['volume_24h'])
        circulating_per = "`{:,.2f}%`".format(cData['circulating_supply']/cData['max_supply']) if cData['max_supply'] != None else '`unknown%`'

        name  = ("Price", "Trading Volume", "Circulating")
        value = (price, trading_volume, circulating_per)

        return tuple(zip(name, value))
        
    def hotPercEmbed(self, cData, converter):
        percent_1h = "`{:,.2f}%`".format(cData['quote'][converter]['percent_change_1h'])
        percent_1d = "`{:,.2f}%`".format(cData['quote'][converter]['percent_change_24h'])
        percent_7d = "`{:,.2f}%`".format(cData['quote'][converter]['percent_change_7d'])

        name  = ("Percentaje 1h", "Percentaje 1d", "Percentaje 30d")
        value = (percent_1h, percent_1d, percent_7d)
        
        return tuple(zip(name, value))	
    
    def hotEmbed(self, cData, symbol, converter, fiat):
        embed = discord.Embed(
            title= cData['name'] + ' ' + symbol,
            url= self.currencyUrlEmbed(cData['name'].lower()),
            colour= self.currencyColorEmbed(cData['quote'][converter]['percent_change_1h'])
        )
        # Referencia
        embed.set_author(
            name= 	  'CoinMarketCap',
            url= 	  'https://coinmarketcap.com/',
            icon_url= 'https://coinmarketcap.com/public/media/img/logo-square.png?_=7719c19'
        )
        # Thumbnail
        embed.set_thumbnail(url= self.currencyLogoEmbed(cData['id']))
        # Circulacion - Provisional
        Trade = self.hotCircEmbed(cData, converter, fiat)
        embed.add_field(name= Trade[0][0], value= Trade[0][1], inline= 'true')
        embed.add_field(name= Trade[1][0], value= Trade[1][1], inline= 'true')
        embed.add_field(name= Trade[2][0], value= Trade[2][1], inline= 'true')
        # Porcentajes - Provisional
        Perc = self.hotPercEmbed(cData, converter)
        embed.add_field(name= Perc[0][0] ,value= Perc[0][1], inline='true')
        embed.add_field(name= Perc[1][0] ,value= Perc[1][1], inline='true')
        embed.add_field(name= Perc[2][0] ,value= Perc[2][1], inline='true')
        # Footer
        embed.set_footer(
            text='Last updated: ' + datetime.datetime.now().strftime("%d %b %Y at %X"),
            icon_url='https://icon-library.com/images/verified-icon-png/verified-icon-png-11.jpg'
        )
        return embed
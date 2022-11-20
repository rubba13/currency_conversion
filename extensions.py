import requests
import json
from keys_config import keys


class APIException(Exception):
    pass


class Converter:
    @staticmethod
    def get_price(base: str, quote: str, amount: str):
        if quote == base:
            raise APIException(f'Валюты не могут совпадать: {base}, {quote}.')

        try:
            base_currency = keys[base]
        except KeyError:
            raise APIException(f'Некорректное имя валюты {base}.')

        try:
            quote_currency = keys[quote]
        except KeyError:
            raise APIException(f'Некорректное имя валюты {quote}.')

        try:
            volume = float(amount)
        except ValueError:
            raise APIException(f'Некорректное количество валюты {amount}.')

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={base_currency}&tsyms={quote_currency}')
        result = json.loads(r.content)[keys[quote]] * volume

        return result

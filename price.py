#!/usr/bin/env python3
"""
This script receives from coinmarcetcap.com information
about ERGO rate to USD, EUR and BTC
"""
import json
from argparse import ArgumentParser
from pprint import pprint
from urllib.parse import urlencode
from urllib.request import urlopen, Request

CMC_ERGO_ID = 1762


class CmcApi(object):
    def __init__(self, api_key):
        self.api_key = api_key

    def request(self, path, args):
        url = 'https://pro-api.coinmarketcap.com/v1/%s?%s' % (
            path.lstrip('/'),
            urlencode(args)
        )
        headers = {
            'Accepts': 'application/json',
            'X-CMC_PRO_API_KEY': self.api_key,
        }
        req = Request(url=url, headers=headers)
        res = urlopen(req).read()
        return json.loads(res.decode('utf-8'))

    def get_ergo_price(self, cur):
        res = self.request(
            '/cryptocurrency/quotes/latest',
            {'id': CMC_ERGO_ID, 'convert': cur},
        )
        return res['data'][str(CMC_ERGO_ID)]['quote'][cur]['price']


def main():
    parser = ArgumentParser()
    parser.add_argument('--cmc-key')
    opts = parser.parse_args()

    if opts.cmc_key:
        api_key = opts.cmc_key
    else:
        try:
            with open('var/config.json') as inp:
                config = json.load(inp)
        except FileNotFoundError:
            config = {}
        api_key = config['coinmarketcap_api_key']

    api = CmcApi(api_key)

    price = {}
    for cur in ('USD', 'EUR', 'BTC'):
        price[cur] = api.get_ergo_price(cur)
    pprint(price)


if __name__ == '__main__':
    main()

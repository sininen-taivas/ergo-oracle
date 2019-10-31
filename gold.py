#!/usr/bin/env python3
from argparse import ArgumentParser

import json
from urllib.parse import urljoin, urlencode
from urllib.request import Request, urlopen

METAL_PRICE_CODE = 'WGC/GOLD_DAILY_USD'

BASE_URL = 'http://www.quandl.com/api/v3/datasets/'

OZT = 31.1034768


def get_currency(api_key):
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
    }
    params = {
        'api_key': api_key
    }
    url = urljoin(BASE_URL, METAL_PRICE_CODE) + '?' + urlencode(params)
    req = Request(url=url, headers=headers)
    res = urlopen(req)  # type: http.client.HTTPResponse
    data = json.loads(res.read())
    price = data.get('dataset', {}).get('data', {})[0][1]

    return price


def parse_cli():
    parser = ArgumentParser(description='Retrieves price of gold')
    parser.add_argument('api_key', type=str, help='api key')
    opts = parser.parse_args()
    return opts


def main():
    opts = parse_cli()
    print(get_currency(opts.api_key))


if __name__ == '__main__':
    main()

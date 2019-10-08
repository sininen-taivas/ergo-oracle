#!/usr/bin/env python3

import json
import logging
import sys
from argparse import ArgumentParser

from price import CmcApi
from util import ErgoClient, setup_logger, TARGET_SERVER
from vlq import encode


def read_data_file(fname, lines_expected):
    with open(fname) as inp:
        lines = inp.read().splitlines()
    if len(lines) != 1:
        logging.error(
            'File %s contains %d lines (%d expected)' % (
                fname, len(lines), lines_expected
            )
        )
        sys.exit(1)
    else:
        return lines


def find_box_id(res, token_id):
    for out in res['outputs']:
        for asset in out['assets']:
            if asset['tokenId'] == token_id:
                return out['boxId']
    raise Exception(
        'Could not find box ID for token ID: %s' % token_id
    )


def parse_cli():
    parser = ArgumentParser()
    parser.add_argument(
        '-s', '--server',
        help='Address of RPC server in format SERVER:PORT',
    )
    parser.add_argument(
        '-n', '--network-log', action='store_true', default=False,
        help='Show network logs'
    )
    parser.add_argument(
        '-q', '--quiet', action='store_true', default=False,
        help='Do not show debug output'
    )
    parser.add_argument(
        '--api-key',
        help='API key to pass RPC node authentication',
        required=True
    )

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--mainnet', action='store_true',
                       help='Using main net, default server localhost:9053')
    group.add_argument('--testnet', action='store_true',
                       help='Using test net, default server localhost:9052')
    parser.add_argument('--cmc-key', help='coinmarketcap API key')

    return parser.parse_args()


def main():
    opts = parse_cli()
    setup_logger(stdout=not opts.quiet, network=opts.network_log)

    target_ = 'mainnet'
    if opts.testnet:
        target_ = 'testnet'

    server_ = opts.server or TARGET_SERVER[target_]
    api = ErgoClient(server_, opts.api_key)

    if opts.cmc_key:
        cmc_key = opts.cmc_key
    else:
        try:
            with open('var/config.json') as inp:
                config = json.load(inp)
        except FileNotFoundError:
            config = {}
        cmc_key = config['coinmarketcap_api_key']

    address_id = read_data_file('address.id', 1)[0]
    box_id = read_data_file('box.id', 1)[0]
    token_id = read_data_file('token.id', 1)[0]
    cmc_api = CmcApi(cmc_key)

    price = cmc_api.get_ergo_price('USD')
    logging.info('CMC price: %s' % price)

    price = encode(int(price * 1e7))

    logging.info('Address: %s' % address_id)
    logging.info('Box ID: %s' % box_id)
    logging.info('Token ID: %s' % token_id)
    logging.info('Encoded Price: %s' % price)

    tx = {
        'requests': [{
            'address': address_id,
            'value': 100000,
            'assets': [{
                'tokenId': token_id,
                'amount': 1
            }],
            'registers': {
                'R4': price
            }
        }],
        'fee': 1e6,
        'inputsRaw': []
    }

    signed_tx = api.request(
        '/wallet/transaction/generate',
        data=tx
    )

    res_box_id = find_box_id(signed_tx, token_id)
    logging.info('Second Box ID: %s' % res_box_id)

    with open('box.id', 'a') as out:
        out.write('%s\n' % res_box_id)

    api.request(
        '/wallet/transaction/send',
        data=tx
    )


if __name__ == '__main__':
    main()

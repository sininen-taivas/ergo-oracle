#!/usr/bin/env python3

import logging
import sys
from argparse import ArgumentParser

from price import CmcApi
from update import ergo_update
from util import setup_logger, TARGET_SERVER


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
    parser.add_argument('--cmc-key', help='coinmarketcap API key', required=True)

    return parser.parse_args()


def main():
    opts = parse_cli()
    setup_logger(stdout=not opts.quiet, network=opts.network_log)

    target_ = 'mainnet'
    if opts.testnet:
        target_ = 'testnet'

    server_ = opts.server or TARGET_SERVER[target_]

    cmc_api = CmcApi(opts.cmc_key)
    price = cmc_api.get_ergo_price('USD')
    logging.info('USD/ERG price: %s' % price)

    ergo_update(server_, opts.api_key, int(price*1e7))


if __name__ == '__main__':
    main()

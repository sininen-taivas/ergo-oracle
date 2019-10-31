#!/usr/bin/env python3

import logging
from argparse import ArgumentParser

from gold import get_currency, OZT
from update import ergo_update
from util import setup_logger, TARGET_SERVER


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
    parser.add_argument('--quandl-key', help='quandl API key', required=True)

    return parser.parse_args()


def main():
    opts = parse_cli()
    setup_logger(stdout=not opts.quiet, network=opts.network_log)

    target_ = 'mainnet'
    if opts.testnet:
        target_ = 'testnet'

    server_ = opts.server or TARGET_SERVER[target_]

    price = get_currency(opts.quandl_key) / OZT
    logging.info('Gold Price per Gram in USD: %s' % price)

    ergo_update(server_, opts.api_key, int(price*1e9))


if __name__ == '__main__':
    main()

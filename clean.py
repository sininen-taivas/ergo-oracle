#!/usr/bin/env python3

import logging
import sys
from argparse import ArgumentParser

from util import ErgoClient, setup_logger, ErgoApiException, TARGET_SERVER


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

    parser.add_argument(
        '--stop', action='store_true', default=False,
        help='Stop it!'
    )

    return parser.parse_args()


def is_box_spent(api, box_id):
    try:
        box_id = box_id
        api.request(
            '/utxo/byId/%s' % box_id
        )
    except ErgoApiException as ex:
        if ex.reason == 'not-found' and ex.detail is None:
            # utxo does not exist -> spent
            return True
        else:
            raise
    else:
        # utxo exists -> not spent
        return False


def main():
    opts = parse_cli()
    setup_logger(stdout=not opts.quiet, network=opts.network_log)

    target_ = 'mainnet'
    if opts.testnet:
        target_ = 'testnet'

    server_ = opts.server or TARGET_SERVER[target_]
    api = ErgoClient(server_, opts.api_key)

    with open('box.id') as inp:
        lines = inp.read().splitlines()

    if len(lines) == 1:
        logging.debug('One box ID in box.id')
        pass
    elif len(lines) != 2:
        logging.error('File box.id contains %d lines (expected 2)' % (
            len(lines)
        ))
        sys.exit(1)
    else:
        logging.debug('Two box IDs in box.id')
        id1, id2 = lines
        if not is_box_spent(api, id1):
            logging.debug('First box ID is not spent')
            if opts.stop:
                with open('box.id', 'w') as out:
                    out.write('%s\n' % id1)  # remove 2nd line
                logging.debug('Removed second box ID')
        else:
            logging.debug('! First box ID is spent')
            if not is_box_spent(api, id2):
                logging.debug('Second box ID is not spent')
                res = api.request(
                    '/wallet/boxes/unspent'
                    '?minConfirmations=30&minInclusionHeight=0'
                )
                found = any(x['box']['boxId'] == id1 for x in res)
                if found:
                    with open('box.id', 'w') as out:
                        out.write('%s\n' % id2)  # remove 1st line
                    logging.debug('Removed first box ID')
                else:
                    logging.error('Not enough confirmations yet')
                    sys.exit(1)
            else:
                logging.error(
                    'Both 1st and 2nd box IDs are spent'
                )
                sys.exit(1)


if __name__ == '__main__':
    main()

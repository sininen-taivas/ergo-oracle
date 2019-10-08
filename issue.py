#!/usr/bin/env python3

from argparse import ArgumentParser

from util import setup_logger, ErgoClient, TARGET_SERVER


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
        '--name', type=str,
        help='Name of contract',
        required=True
    )
    parser.add_argument(
        '--description', type=str,
        help='Description of contract',
        required=True
    )
    return parser.parse_args()


def main():
    opts = parse_cli()
    setup_logger(stdout=not opts.quiet, network=opts.network_log)

    target_ = 'mainnet'
    if opts.testnet:
        target_ = 'testnet'

    server_ = opts.server or TARGET_SERVER[target_]
    api = ErgoClient(server_, opts.api_key)

    # Ger first wallet address
    res = api.request(
        '/wallet/addresses',
    )
    addr = res[0]

    # Generate transaction
    tx_data = {
        'requests': [{
            'address': addr,
            'amount': 1,
            'name': opts.name,
            'description': opts.description,
            'decimals': 0,
        }],
        'fee': 1e6,
        'inputsRaw': [],
    }
    res = api.request(
        '/wallet/transaction/generate',
        data=tx_data,
    )

    out = res['outputs'][0]
    with open('address.id', 'w') as fobj:
        fobj.write(addr + '\n')
    with open('box.id', 'w') as fobj:
        fobj.write(out['boxId'] + '\n')
    with open('token.id', 'w') as fobj:
        fobj.write(out['assets'][0]['tokenId'] + '\n')

    api.request(
        '/wallet/transaction/send',
        data=tx_data,
    )


if __name__ == '__main__':
    main()

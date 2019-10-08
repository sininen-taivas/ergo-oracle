#!/usr/bin/env python3
from argparse import ArgumentParser


def zigzag(i: int):
    return (i >> 31) ^ (i << 1)


def vlq(i: int):
    ret = []
    while i != 0:
        b = i & 0x7F
        i >>= 7
        if i > 0:
            b |= 0x80
        ret.append(b)
    return ret


def encode(n: int):
    z = zigzag(n)
    v = vlq(z)
    r = '05' + ''.join(['{0:02x}'.format(i) for i in v])
    return r


def parse_cli():
    parser = ArgumentParser(description='Encode signed Long value using VLQ and zigzag')
    parser.add_argument('value', type=int, help='Signed long integer number')
    opts = parser.parse_args()
    return opts


def main():
    opts = parse_cli()
    print(encode(opts.value))


if __name__ == '__main__':
    main()

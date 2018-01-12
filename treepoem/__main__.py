# -*- encoding:utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

import os
import argparse
import sys
from textwrap import fill

from . import generate_barcode
from .data import barcode_types

supported_barcode_types = ('Supported barcode types are:\n'
    + fill(', '.join(sorted(barcode_types)), initial_indent='    ', subsequent_indent='    '))

def main():
    p = argparse.ArgumentParser(epilog=supported_barcode_types)
    p.add_argument('-t', '--type', default='qrcode', help='Barcode type (default (%(default)s))')
    p.add_argument('-f', '--fmt', help='Output format (default is based on file extension)')
    p.add_argument('-o', '--output', help='Output file (default is stdout)')
    p.add_argument('data', help='Barcode data')
    p.add_argument('options', nargs='*', type=lambda x: x.split('=', 1)[:2], help='List of BWIPP options (e.g. width=1.5)')
    args = p.parse_args()

    if args.type not in barcode_types:
        p.error('Barcode type %r is not supported. %s' % (args.type, supported_barcode_types))

    if args.output is None:
        args.output = sys.stdout.buffer
        if args.fmt is None:
            args.fmt = 'xbm'

    image = generate_barcode(args.type, args.data, dict(args.options))
    image.convert('1').save(args.output, args.fmt)

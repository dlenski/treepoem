# -*- encoding:utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

import os
import argparse
import sys

from . import generate_barcode
from .data import barcode_types

def main():
    p = argparse.ArgumentParser()
    p.add_argument('-t', '--type', default='qrcode', help='Barcode type (default (%(default)s))')
    p.add_argument('-f', '--fmt', help='Output format (default is based on file extension)')
    p.add_argument('-o', '--output', help='Output file (default is stdout)')
    p.add_argument('data', help='Barcode data')
    p.add_argument('options', nargs='*', type=lambda x: x.split('=', 1)[:2], help='List of BWIPP options (e.g. width=1.5)')
    args = p.parse_args()

    if args.output is None:
        args.output = sys.stdout.buffer
        if args.fmt is None:
            args.fmt = 'xbm'

    image = generate_barcode(args.type, args.data, dict(args.options))
    image.convert('1').save(args.output, args.fmt)

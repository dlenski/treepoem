#!/usr/bin/env python
# -*- encoding:utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

import os

BASE_DIR = os.path.dirname(__file__)
BWIPP_PATH = os.path.join(BASE_DIR, 'treepoem', 'postscriptbarcode', 'barcode.ps')
BARCODE_TYPES_PATH = os.path.join(BASE_DIR, 'treepoem', 'data.py')


def main():
    print('Loading barcode types from {}'.format(BWIPP_PATH))
    all_barcode_types = load_barcode_types()

    print('Writing out {}'.format(BARCODE_TYPES_PATH))
    write_out_barcode_types(all_barcode_types)

    print('Done')


def load_barcode_types():
    barcode_types = []
    barcode_type = barcode_desc = None
    with open(BWIPP_PATH) as fp:
        for line in fp:
            if line.startswith('% --BEGIN ENCODER ') and line.endswith('--\n'):
                barcode_type = line[:-3].split()[3]
                barcode_desc = None
            elif line.startswith('% --DESC: '):
                barcode_desc = line[:-1].split(None, 2)[2]
            elif line.startswith('% --END ENCODER ') and line.endswith('--\n'):
                barcode_types.append((barcode_type, barcode_desc))
                barcode_type = barcode_desc = None

    return sorted(barcode_types)


def write_out_barcode_types(all_barcode_types):
    with open(BARCODE_TYPES_PATH, 'w') as fp:
        fp.write('# -*- encoding:utf-8 -*-\n')
        fp.write('from __future__ import absolute_import, division, print_function, unicode_literals\n')
        fp.write('\n')
        fp.write('# All supported barcode types, extracted from barcode.ps\n')
        fp.write('barcode_types = {\n')
        for barcode_type, barcode_desc in all_barcode_types:
            fp.write('    {!r}: {!r},\n'.format(barcode_type, barcode_desc))
        fp.write('}\n')


if __name__ == '__main__':
    main()

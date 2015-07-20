#!/usr/bin/env python

#
# Copyright (c) 2015 Alexander Schrijver <alex@flupzor.nl>
#
# Permission to use, copy, modify, and distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
# WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
# ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
# ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
# OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
#

import csv
import sys

from datetime import datetime
from decimal import Decimal
from pprint import pprint

from transaction.transaction import INGTransaction

def usage():
    print "{program_name}: file [file...]".format(program_name=sys.argv[0])
    sys.exit(1)  # EXIT_FAILURE

def main():
    path_list = sys.argv[1:]

    if len(path_list) == 0:
        usage()
        # NOTREACHED

    for path in path_list:
        with open(path, 'rb') as csvfile:
            parse_ing_file(csvfile)

def parse_ing_file(file_handle):
    ing_reader = csv.reader(file_handle, delimiter=',')

    ing_reader.next()

    totals = {}

    for row in ing_reader:
        ing_transaction = INGTransaction.from_row(row)
        category = ing_transaction.category
        month = ing_transaction.date.month

        totals.setdefault(month, {})

        totals[month].setdefault(category, Decimal('0'))
        totals[month][category] += ing_transaction.amount

    pprint(totals)

if __name__ == '__main__':
    main()

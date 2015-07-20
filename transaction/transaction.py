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

from datetime import datetime
from decimal import Decimal

try:
    from .rules_local import rule_list
except ImportError:
    from .rules import rule_list


class INGTransaction(object):
    """
    One financial transaction which can be import from an ING CSV export.

    Use csv library to import the transaction, eg:

    > ing_reader = csv.reader(file_handle, delimiter=',')
    > ing_reader.next()
    > for row in ing_reader:
    >    ing_transaction = INGTransaction.from_row(row)
    """

    def __init__(self, date, description, account, contra_account,
                 mutation_type, amount, announcement, withdrawal):

        self.date = date
        self.description = description
        self.account = account
        self.contra_account = contra_account
        self.mutation_type = mutation_type
        self.amount = amount
        self.announcement = announcement
        self.withdrawal = withdrawal

    @property
    def category(self):
        """
        Return the first category that matches.
        """

        for category, match_list in rule_list:
            for match in match_list:
                if match.match(self):
                    return category

        return None

    def __str__(self):
        return "{category}: {date}: {amount} {description} {contra_account}".format(
            category=self.category, date=self.date, amount=self.amount,
            description=self.description, contra_account=self.contra_account
        )

    @classmethod
    def from_row(cls, row):
        transaction = {
            'date': datetime.strptime(row[0], "%Y%m%d").date(),
            'description': row[1],
            'account': row[2],
            'contra_account': row[3],
            'code': row[4],
            'af_bij': row[5],
            'amount': Decimal(row[6].replace(',', '.')),
            'mutation_type': row[7],
            'announcement': row[8]
        }

        mutation_types = {
            'Betaalautomaat': 'BA',
            'Diversen': 'DV',
            'Internetbankieren': 'GT',
            'Geldautomaat': 'GM',
            'Incasso': 'IC',
            'Overschrijving': 'OV',
            'Verzamelbetaling': 'VZ',
        }

        # Making sure my assumptions are correct.
        assert mutation_types[transaction['mutation_type']] == transaction['code']

        assert transaction['amount'] >= Decimal('0')

        assert transaction['af_bij'] in ['Af', 'Bij']

        if transaction['af_bij'] == 'Af':
            new_amount = -transaction['amount']
            withdrawal = True
        if transaction['af_bij'] == 'Bij':
            new_amount = transaction['amount']
            withdrawal = False

        context = {
            'date': transaction['date'],
            'description': transaction['description'],
            'account': transaction['account'],
            'contra_account': transaction['contra_account'],
            'mutation_type': transaction['mutation_type'],
            'amount': new_amount,
            'announcement': transaction['announcement'],
            'withdrawal': withdrawal,
        }

        return cls(
            **context
        )

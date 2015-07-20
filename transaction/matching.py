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

class Match(object):
    def __init__(self, mutation_type=None, string_list=None, withdrawal=None):
        self.mutation_type = mutation_type
        self.string_list = string_list
        self.withdrawal = withdrawal

    def description_matches(self, transaction, string_list):
        for string in self.string_list:
            if string in transaction.description:
                return True

        return False

    def match(self, transaction):
        if self.mutation_type:
            if self.mutation_type != transaction.mutation_type:
                return False

        if self.withdrawal:
            if self.withdrawal != transaction.withdrawal:
                return False

        if self.string_list:
            if self.description_matches(transaction, self.string_list) == False:
                return False

        return True



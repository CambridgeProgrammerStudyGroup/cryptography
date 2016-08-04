#!/usr/bin/python
# -*- coding: utf-8 -*-

import string
import codecs

from substitution import SubstitutionSolver
from ngram import NGramSet

ALPHABET = list(string.uppercase)

def get_letters(chars):
    for ch in chars:
        ch = ch.upper()
        if ch in ALPHABET:
            yield ch


def get_freq_dicts(chars, period):
    freq_dicts = []
    for i in range(period):
        freq_dicts.append(dict((ch, 0) for ch in ALPHABET))

    for i, ch in enumerate(get_letters(chars)):
        freq_dicts[i % period][ch] += 1

    return freq_dicts


def get_index_of_coincidence(chars, period):
    ics = []
    for freq_dict in get_freq_dicts(chars, period):
        counts = freq_dict.values()
        total = float(sum(counts))
        ics.append(sum(count*(count-1) for count in counts) / (total * (total-1)))
    return sum(ics) / len(ics)


class PolySubstitutionSolver(SubstitutionSolver):
    """
    Solves polysubstitution ciphers. This is not the same as polyalphabetic
    substitution ciphers, such as Vigenère. What it means is that each letter
    of plain text gets replaced with a token consisting of a number of
    letters (all the tokens having the same length).
    """
    def __init__(self, token_length, *args):
        super(PolySubstitutionSolver, self).__init__(*args)
        self.token_length = token_length

    def get_ciphertext(self, text):
        result = []
        current = ''

        for ch in text.upper():
            if ch not in ALPHABET:
                result.append(ch)
            else:
                current += ch
                if len(current) == self.token_length:
                    result.append(current)
                    current = ''

        return result

    def get_cipher_alphabet(self, ciphertext):
        cipher_tokens = set()
        for ch in ciphertext:
            if len(ch) == self.token_length and ch[0] in ALPHABET:
                cipher_tokens.add(ch)

        if len(cipher_tokens) > len(self.ngram_set.valid_letters):
            raise Exception("Too many (%d) tokens in cipher alphabet" % len(cipher_tokens))

        for i in range(len(self.ngram_set.valid_letters) - len(cipher_tokens)):
            cipher_tokens.add("dummy-%02d" % i)

        return cipher_tokens


if __name__ == '__main__':
    import sys

    if len(sys.argv) == 2:
        with open(sys.argv[1]) as f:
            text = f.read()
        for period in range(1, 20):
            print "%3d\t%04f" % (period, get_index_of_coincidence(text, period))
    elif len(sys.argv) == 4:
        token_length = int(sys.argv[1])
        lang = sys.argv[2]
        solver = PolySubstitutionSolver(token_length, NGramSet.make_pretrained(4, lang))
        with open(sys.argv[3]) as f:
            text = f.read()
        key, plaintext = solver.solve(text)
        print key
        print codecs.encode(plaintext, 'utf-8')
    else:
        print >>sys.stderr, "Usage:"
        print >>sys.stderr, "    %s filename" % sys.argv[0]
        print >>sys.stderr, "    %s token_length lang filename" % sys.argv[0]

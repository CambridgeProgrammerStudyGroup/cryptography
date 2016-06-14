#!/usr/bin/python

import random
import string
from quadgram import Scorer


ALPHABET = list(string.uppercase)

ENGLISH_FREQUENCY = ['E', 'T', 'A', 'O', 'N', 'I', 'H', 'S', 'R', 'D', 'L', 'U', 'M',
                     'W', 'C', 'F', 'Y', 'G', 'B', 'P', 'V', 'K', 'X', 'J', 'Q', 'Z']

DEBUG = False


def decrypt(key, text):
    table = dict(zip(key, ALPHABET))
    return ''.join(table.get(ch, ch) for ch in text.upper())


def make_random_key():
    key = list(ALPHABET)
    random.shuffle(key)
    return key


def change_key(old_key):
    key = list(old_key)
    i, j = tuple(random.sample(range(len(key)), 2))
    key[i], key[j] = key[j], key[i]
    return key


def make_reasonable_key(text):
    rev_table = dict(zip(ENGLISH_FREQUENCY, order_by_frequency(text)))
    return map(rev_table.get, ALPHABET)


def order_by_frequency(chars):
    freqs = {}
    for ch in ALPHABET:
        freqs[ch] = 0

    for ch in chars:
        ch = ch.upper()
        if ch in freqs:
            freqs[ch] += 1

    l = [(count, ch) for (ch, count) in freqs.items()]
    l.sort()
    l.reverse()
    return [ch for (_, ch) in l]


# Start with a reasonable guess as to the key (assume order of most frequent
# letters in the plain text is the same as in the training corpus) and try out
# small random changes to see if they improve the result until we can't seem
# to improve it any more. See
# http://practicalcryptography.com/cryptanalysis/stochastic-searching/cryptanalysis-simple-substitution-cipher/
def solve(text, scorer=None):
    if scorer is None:
        scorer = Scorer.make_pretrained()

    def get_improvement(key):
        score = scorer.score(decrypt(key, text))
        if DEBUG: print score
        for _ in range(1000):
            new_key = change_key(key)
            new_score = scorer.score(decrypt(new_key, text))
            if new_score > score:
                return new_key
        return None

    last_key =  make_reasonable_key(text)
    key = last_key
    while key is not None:
        last_key, key = key, get_improvement(key)
    return last_key


if __name__ == "__main__":
    import sys
    if len(sys.argv) == 2:
        with open(sys.argv[1]) as f:
            text = f.read()
        key = solve(text)
        print key
        print decrypt(key, text)
    else:
        print >>sys.stderr, "Usage %s filename" % sys.argv[0]

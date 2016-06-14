#!/usr/bin/python

import string
from quadgram import Scorer


ALPHABET = list(string.uppercase)


def decrypt(key, text):
    table = dict(zip(ALPHABET[key:]+ALPHABET[:key], ALPHABET))
    return ''.join(table.get(ch, ch) for ch in text.upper())


def solve(text, scorer=None):
    if scorer is None:
        scorer = Scorer.make_pretrained()

    best_key = None
    best_score = None

    for key in range(len(ALPHABET)):
        score = scorer.score(decrypt(key, text))
        if best_key is None or score > best_score:
            best_key = key
            best_score = score

    return best_key


if __name__ == '__main__':
    import sys
    if len(sys.argv) == 2:
        with open(sys.argv[1]) as f:
            text = f.read()
        key = solve(text)
        print key
        print decrypt(key, text)
    else:
        print >>sys.stderr, "Usage %s filename" % sys.argv[0]

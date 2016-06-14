#!/usr/bin/python

import string

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


if __name__ == '__main__':
    import sys

    if len(sys.argv) == 2:
        with open(sys.argv[1]) as f:
            text = f.read()
        for period in range(1, 20):
            print "%3d\t%04f" % (period, get_index_of_coincidence(text, period))
    else:
        print >>sys.stderr, "Usage %s filename" % sys.argv[0]

#!/usr/bin/python

import random
import string
from ngram import NGramSet


class SubstitutionSolver(object):
    def __init__(self, ngram_set):
        self.ngram_set = ngram_set
        self.debug = False

    # Start with a reasonable guess as to the key (assume order of most
    # frequent letters in the plain text is the same as in the training
    # corpus) and try out small random changes to see if they improve the
    # result until we can't seem to improve it any more. See
    # http://practicalcryptography.com/cryptanalysis/stochastic-searching/cryptanalysis-simple-substitution-cipher/
    def solve(self, text):
        ngram_set = self.ngram_set
        ciphertext = self.get_ciphertext(text)

        def get_improvement(key):
            score = ngram_set.score(self.decrypt(key, ciphertext))
            if self.debug: print score
            for _ in range(1000):
                new_key = self.change_key(key)
                new_score = ngram_set.score(self.decrypt(new_key, ciphertext))
                if new_score > score:
                    return new_key
            return None

        last_key = self.make_reasonable_key(ciphertext)
        key = last_key
        while key is not None:
            last_key, key = key, get_improvement(key)
        return last_key, self.decrypt(last_key, ciphertext)

    def make_reasonable_key(self, ciphertext):
        freqs = {}
        for ch in self.get_cipher_alphabet(ciphertext):
            freqs[ch] = 0

        for ch in ciphertext:
            if ch in freqs:
                freqs[ch] += 1

        l = [(count, ch) for (ch, count) in freqs.items()]
        l.sort()
        l.reverse()
        ordered_by_frequency = [ch for (_, ch) in l]
        corpus_frequency = self.ngram_set.get_letters_by_frequency()

        rev_table = dict(zip(corpus_frequency, ordered_by_frequency))
        return map(rev_table.get, sorted(self.ngram_set.valid_letters))

    def decrypt(self, key, ciphertext):
        alphabet = sorted(self.ngram_set.valid_letters)
        table = dict(zip(key, alphabet))
        return u''.join(table.get(ch, ch) for ch in ciphertext)

    def change_key(self, old_key):
        key = list(old_key)
        i, j = tuple(random.sample(range(len(key)), 2))
        key[i], key[j] = key[j], key[i]
        return key

    def get_ciphertext(self, text):
        return text.upper()

    def get_cipher_alphabet(self, ciphertext):
        return list(self.ngram_set.valid_letters)


if __name__ == "__main__":
    import sys
    if len(sys.argv) == 2:
        solver = SubstitutionSolver(NGramSet.make_pretrained(4, 'en'))
        with open(sys.argv[1]) as f:
            text = f.read()
        key, plaintext = solver.solve(text)
        print key
        print plaintext
    else:
        print >>sys.stderr, "Usage %s filename" % sys.argv[0]

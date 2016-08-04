from collections import defaultdict
from math import log
import string
import codecs

UTF8 = 'utf-8'

class NGramSet(object):
    def __init__(self, n, valid_letters):
        self.total = 0
        self.freqs = defaultdict(int)
        self.n = n
        self.valid_letters = valid_letters

    @classmethod
    def make_pretrained(cls, n=4, lang='en', filename=None):

        if filename is None:
            from os.path import dirname, join
            if lang == 'en':
                leafname = "%d-gram_freqs.txt" % n
            else:
                leafname = "%d-gram_freqs-%s.txt" % (n, lang)
            filename = join(dirname(__file__), leafname)

        scorer = cls(n, set())
        with codecs.open(filename, 'r', UTF8) as f:
            for line in f:
                if not line.startswith('#'):
                    parts = line.split()
                    seq = parts[0]
                    count = int(parts[1])
                    assert len(seq) == n
                    scorer.freqs[seq] = count
                    scorer.total += count
                    scorer.valid_letters.update(seq)
        return scorer

    def populate(self, chars):
        for seq in get_ngrams(chars, self.n, self.valid_letters):
            self.total += 1
            self.freqs[seq] += 1

    def populate_from_file(self, filename):
        self.populate(read_filechars(filename))

    def freq(self, seq):
        if seq in self.freqs:
            return self.freqs[seq]
        else:
            return 0

    def score(self, text):
        p = 0.0
        divisor = float(self.total)
        for seq in get_ngrams(text, self.n):
            if seq in self.freqs:
                count = self.freqs[seq]
            else:
                count = 0.1

            p += log(count / divisor)
        return p

    def get_letters_by_frequency(self):
        letter_freqs = defaultdict(int)
        for seq, freq in self.freqs.iteritems():
            for ch in seq:
                letter_freqs[ch] += freq
        letters = list(self.valid_letters)
        letters.sort(key=lambda ch: -letter_freqs[ch])
        return letters


def read_filechars(filename):
    with codecs.open(filename, 'r', 'utf-8-sig') as f:
        while True:
            ch = f.read(1)
            if not ch: break
            yield ch


def get_ngrams(chars, n, valid_letters=None):
    seq = u""
    for ch in chars:
        if ch.isdigit():
            ch = '.'
        elif ch.isalpha():
            ch = ch.upper()
            if valid_letters and ch not in valid_letters:
                ch = '.'
        else:
            continue

        seq = seq + ch

        if len(seq) > n:
            seq = seq[-n:]

        if len(seq) == n and '.' not in seq:
            yield seq


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print >>sys.stderr, "Usage %s [--alphabet file] n [file...]" % sys.argv[0]
        sys.exit(1)

    args = sys.argv[1:]

    if args[0] != '--alphabet':
        valid_letters = set(string.uppercase)
    else:
        valid_letters = set()
        with codecs.open(args[1], 'r', 'utf-8-sig') as f:
            for ch in f.read():
                if ch.isalpha():
                    valid_letters.add(ch.upper())
        args = args[2:]

    ngram_set = NGramSet(int(args[0]), valid_letters)

    for filename in args[1:]:
        ngram_set.populate_from_file(filename)

    ngrams = list(ngram_set.freqs.keys())
    ngrams.sort()
    for ngram in ngrams:
        sys.stdout.write("%s\t%d\n" % (codecs.encode(ngram, UTF8), ngram_set.freqs[ngram]))

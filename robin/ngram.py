from collections import defaultdict
from math import log

class NGramSet(object):
    def __init__(self, n):
        self.total = 0
        self.freqs = defaultdict(int)
        self.n = n

    @classmethod
    def make_pretrained(cls, n=4, filename=None):

        if filename is None:
            from os.path import dirname, join
            filename = join(dirname(__file__), "%d-gram_freqs.txt" % n)

        scorer = cls(n)
        with open(filename) as f:
            for line in f:
                if not line.startswith('#'):
                    parts = line.split()
                    seq = parts[0]
                    count = int(parts[1])
                    assert len(seq) == n
                    scorer.freqs[seq] = count
                    scorer.total += count
        return scorer

    def populate(self, chars):
        for seq in get_ngrams(chars, self.n):
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


def read_filechars(filename):
    with open(filename) as f:
        while True:
            ch = f.read(1)
            if not ch: break
            yield ch


def get_ngrams(chars, n):
    seq = ""
    for ch in chars:
        if ch.isdigit():
            ch = '.'
        elif ch.isalpha():
            ch = ch.upper()
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
        print >>sys.stderr, "Usage %s n [file...]" % sys.argv[0]
        sys.exit(1)

    ngram_set = NGramSet(int(sys.argv[1]))

    for filename in sys.argv[2:]:
        scorer.populate_from_file(filename)

    ngrams = list(scorer.freqs.keys())
    ngrams.sort()
    for ngram in ngrams:
        sys.stdout.write("%s\t%d\n" % (ngram, scorer.freqs[ngram]))

from collections import defaultdict
from math import log

class Scorer(object):
    def __init__(self):
        self.total = 0
        self.freqs = defaultdict(int)

    @classmethod
    def make_pretrained(cls, filename=None):

        if filename is None:
            from os.path import dirname, join
            filename = join(dirname(__file__), "quadgram_freqs.txt")

        scorer = cls()
        with open(filename) as f:
            for line in f:
                if not line.startswith('#'):
                    parts = line.split()
                    seq = parts[0]
                    count = int(parts[1])
                    scorer.freqs[seq] = count
                    scorer.total += count
        return scorer

    def populate(self, chars):
        for seq in get_quadgrams(chars):
            self.total += 1
            self.freqs[seq] += 1

    def populate_from_file(self, filename):
        self.populate(read_filechars(filename))

    def score(self, text):
        p = 0.0
        divisor = float(self.total)
        for seq in get_quadgrams(text):
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


def get_quadgrams(chars):
    seq = ""
    for ch in chars:
        if ch.isdigit():
            ch = '.'
        elif ch.isalpha():
            ch = ch.upper()
        else:
            continue

        seq = seq + ch

        if len(seq) > 4:
            seq = seq[-4:]

        if len(seq) == 4 and '.' not in seq:
            yield seq


if __name__ == "__main__":
    import sys

    scorer = Scorer()

    for filename in sys.argv[1:]:
        scorer.populate_from_file(filename)

    quadgrams = list(scorer.freqs.keys())
    quadgrams.sort()
    for quadgram in quadgrams:
        sys.stdout.write("%s\t%d\n" % (quadgram, scorer.freqs[quadgram]))

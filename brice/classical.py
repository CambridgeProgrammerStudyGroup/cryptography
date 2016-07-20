#!/usr/bin/env python

import Tools.utils as utils
import string
from collections import defaultdict

def stripNotIn(charset, orig):
    return [for c in orig if c in charset]

def alphanumOnly(s):
    return stripNotIn(set(string.letters+string.digits), s)

def alphaOnly(s):
    return stripNotIn(set(string.letters), s)

def frequencyCount(txt, ngram=1):
    frequencies=defaultdict(int)
    for segment in splitByN(alphaOnly(txt).upper(), ngram):
        frequencies[segment] += 1
    return frequencies

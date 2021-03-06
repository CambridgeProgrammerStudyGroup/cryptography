#!/usr/bin/env python

import os
import base64
import random
from collections import defaultdict
import pprint

import plotly.plotly as py
import plotly.graph_objs as go

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend


def mapKeys(d, newKey):
    return dict([(newKey(k), v) for k,v in d.items()])

def statsFrom(text):
    stats = dict([(c, 0.0) for c in range(256)])
    for c in text:
        stats[c] += 1.0
    total = sum(stats.values())
    stats = dict(map(lambda x: (x[0], x[1]/total), stats.items()))
    return stats

def getStats(filename):
    with open(filename) as f:
        return statsFrom(bytearray(f.read()))

ENGLISH_STATS = getStats("../data/COLLECTED_ENGLISH_CORPUS.txt")

def similarity(A,B):
    differences = [(A[c]-B[c]) for c in xrange(0,256)]
    return - sum([dif*dif for dif in differences])

def score(stats, text):
    textStats = statsFrom(text)
    return similarity(stats, textStats)

def decipherXOR(ciphertext, ch):
    res = bytearray(len(ciphertext))
    for i in range(len(ciphertext)):
        res[i] = ciphertext[i]^ch
    return res

def solveXOR(ciphertext):
    candidates = [(decipherXOR(ciphertext, c), c) for c in range(256)]
    scores = [(score(ENGLISH_STATS, cand), ch) for cand, ch in candidates]
    best = max(scores, key=lambda p: p[0])
    # pprint.pprint([
    #     (c, str(pt[:10])) for pt, c in candidates
    # ])
    return best[1]

def popcount(b):
    count = 0
    while b > 0:
        if (b & 0b1):
            count+=1
        b = b >>1
    return count

def hamming(A, B):
    """
    Calculates the hamming distance between two bytearrays
    >>> hamming(bytearray("this is a test"), bytearray("wokka wokka!!!"))
    37
    """
    return sum([popcount(a^b) for a,b in zip(A, B)])

def vignereScore(ciphertext, keysize):
    chunks = chunkify(ciphertext, keysize) # blocks of 16 bytes
    pairs = zip(chunks, chunks[1:])
    distance = sum([hamming(a,b)/float(keysize) for a,b in pairs])/float(len(pairs))
    return distance

def vignereLength(ciphertext, minv=2, maxv=50, filename=None):
    lowest_distance = 1000000
    best_length = 0
    lengths = []
    scores = []
    for ks in range(minv, maxv):
        distance = vignereScore(ks)
        lengths.append(ks)
        scores.append(distance)
        # print("size={} dist={}".format(ks, distance))
        if distance < lowest_distance:
            best_length = ks
            lowest_distance = distance
    if filename:
        fig = dict(
            data = [go.Scatter(
                x = lengths,
                y = scores
            )],
            layout = dict(
                title = "Averaged Hamming distance between ciphertext blocks ",
                xaxis = dict(title = 'Line'),
                yaxis = dict(title = 'Hamming distance (avg)'),
             )
        )
        py.iplot(fig, filename=filename)
    return best_length

def chunkify(text, n):
    return [text[i:i+n] for i in range(0, len(text), n)]

def solveVignere(ciphertext):
    N = vignereLength(ciphertext)
    return solveVignereN(ciphertext, N)

def solveVignereN(ciphertext, N):
    # print("vignerelength:", N)
    chunks = chunkify(ciphertext, N)[:-1]
    ciphertexts = zip(*chunks)
    # print([len(ct) for ct in ciphertexts])
    keybytes = [solveXOR(ct) for ct in ciphertexts]
    # pprint.pprint([
    #     (key, str(decipherXOR(ct, key))[:20])
    #     for key,ct in zip(keybytes, ciphertexts)
    # ])
    return bytearray(keybytes)

def XOR(A,B, size=16):
    return bytearray([a^b for a,b in zip(A, B)])[:size]

def vignere(ciphertext, key):
    nkeys = (len(ciphertext)/len(key))+1
    longkey = key*nkeys
    plaintext = bytearray([a^b for a,b in zip(ciphertext, longkey)])
    return str(plaintext)

def AES_ECB_encrypt(key, plaintext, iv=None):
    backend = default_backend()
    cipher = Cipher(algorithms.AES(bytes(key)), modes.ECB(), backend=backend)
    encryptor = cipher.encryptor()
    ct = encryptor.update(bytes(plaintext)) + encryptor.finalize()
    return ct

def AES_ECB_decrypt(key, ciphertext, iv=None):
    backend = default_backend()
    cipher = Cipher(algorithms.AES(bytes(key)), modes.ECB(), backend=backend)
    decryptor = cipher.decryptor()
    pt = decryptor.update(ciphertext) + decryptor.finalize()
    return pt

def AES_CBC_decrypt(key, ct, iv):
    blocks = chunkify(ct, 16)
    pass1 = [bytearray(AES_ECB_decrypt(key, b)) for b in blocks]
    return "".join([str(XOR(a,bytearray(b))) for a,b in zip(pass1, [iv]+blocks)])

def AES_CBC_encrypt(key, pt, iv):
    if len(pt)%16 != 0:
        raise RuntimeError("Wrong size for plaintext, not multiple of blocksize. Did you forget to pad?")
    blocks = chunkify(pt, 16)
    ct = [iv]
    for i,b in list(enumerate(blocks)):
        nb = XOR(bytearray(ct[i]),bytearray(b))
        ct.append(AES_ECB_encrypt(key, str(nb)))
    return "".join([str(x) for x in ct[1:]])

def pkcs7_pad(text, blocksize=16):
    if len(text)%blocksize == 0:
        return text+bytearray([16]*16)
    pad = blocksize - (len(text)%blocksize)
    return text+bytearray([pad]*pad)

def pkcs7_depad(text, blocksize):
    return text[:-int(text[-1])]

def randstr(size=16):
    return str(bytearray([random.randint(0,255) for i in range(size)]))

def ECB_score(text):
    return vignereScore(bytearray(text), 16)

def repeated_block_counts(text, blocksize):
    count = defaultdict(int)
    for block in chunkify(text, blocksize):
        count[block] += 1
    return sorted(count.values())

def repeated_blocks(text, blocksize):
    return max(repeated_block_counts(text, blocksize))

def accuracy(predictions, actual):
    correct = 0
    for p, actual in zip(predictions, actual):
        if p is actual:
            correct +=1
    return float(correct)/len(predictions)

def predict_mode(oracle):
    chosen_plaintext = "A"*100
    ciphertext = oracle(chosen_plaintext)
    rbs = repeated_blocks(ciphertext, 16)
    if rbs > 4:
        return AES_ECB_encrypt
    else:
        return AES_CBC_encrypt

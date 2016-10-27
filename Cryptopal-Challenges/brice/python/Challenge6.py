#!/usr/bin/env python

from utils import *


with open("../data/6.txt") as fp:
    b64 = fp.read()
ciphertext = bytearray(base64.b64decode(b64))

# DECIPHER SIMPLE XOR
# hexString = "1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736"
# xor_ciphertext = bytearray(hexString.decode('hex'))
# print(decipherXOR(xor_ciphertext, solveXOR(xor_ciphertext)))

# print(hamming(bytearray("this is a test"), bytearray("wokka wokka!!!")))
# print(chunkify("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789", 3))

key = solveVignere(ciphertext)
plaintext = vignere(ciphertext, key)
print plaintext

plaintext = bytearray("""
There was once a lamb with purple wool.
The others in the flock thought him a fool.
Shame for them, when easter came,
The purple wool went to the fair
The other lambs ended up as easter fare!
""")

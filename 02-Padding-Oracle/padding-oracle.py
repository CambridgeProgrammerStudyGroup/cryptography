#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: Emma Gordon
@author: Brice Fernandes
"""

import random
import sys
from Crypto.Cipher import AES


BLOCK_SIZE = 16  # bytes
INIT_VEC = 'This is an IV456'  # hardcoding this is a terrible idea

EXAMPLE_TEXT = """Friends, Romans, countrymen, lend me your ears;
I come to bury Caesar, not to praise him.
The evil that men do lives after them;
The good is oft interred with their bones;
So let it be with Caesar. The noble Brutus
Hath told you Caesar was ambitious:
If it were so, it was a grievous fault,
And grievously hath Caesar answer’d it.
Here, under leave of Brutus and the rest–
For Brutus is an honourable man;
So are they all, all honourable men–
Come I to speak in Caesar’s funeral.
He was my friend, faithful and just to me:
But Brutus says he was ambitious;
And Brutus is an honourable man.
He hath brought many captives home to Rome
Whose ransoms did the general coffers fill:
Did this in Caesar seem ambitious?
When that the poor have cried, Caesar hath wept:
Ambition should be made of sterner stuff:
Yet Brutus says he was ambitious;
And Brutus is an honourable man.
You all did see that on the Lupercal
I thrice presented him a kingly crown,
Which he did thrice refuse: was this ambition?
Yet Brutus says he was ambitious;
And, sure, he is an honourable man.
I speak not to disprove what Brutus spoke,
But here I am to speak what I do know.
You all did love him once, not without cause:
What cause withholds you then, to mourn for him?
O judgment! thou art fled to brutish beasts,
And men have lost their reason. Bear with me;
My heart is in the coffin there with Caesar,
And I must pause till it come back to me."""


class InvalidPadding(Exception):
    pass


def blockify(text, block_size=BLOCK_SIZE):
    return [text[i:i+block_size] for i in range(0, len(text), block_size)]


def key_gen():
    return "".join([chr(random.getrandbits(8)) for _ in xrange(BLOCK_SIZE)])


def validate_padding(padded_text):
    return all([n == padded_text[-1] for n in padded_text[-ord(padded_text[-1]):]])


def pkcs7_pad(text):
    length = BLOCK_SIZE - (len(text) % BLOCK_SIZE)
    text += chr(length) * length
    return text


def pkcs7_depad(text):
    if not validate_padding(text):
        raise InvalidPadding()
    return text[:-ord(text[-1])]


def encrypt(plaintext, key, init_vec):
    cipher = AES.new(key, AES.MODE_CBC, init_vec)
    padded_text = pkcs7_pad(plaintext)
    ciphertext = cipher.encrypt(padded_text)
    return ciphertext


def decrypt(ciphertext, key, init_vec):
    cipher = AES.new(key, AES.MODE_CBC, init_vec)
    padded_text = cipher.decrypt(ciphertext)
    plaintext = pkcs7_depad(padded_text)
    return plaintext

def numberify(characters):
    return map(lambda x: ord(x), characters)

def stringify(numbers):
    return "".join(map(lambda x: chr(x), numbers))

if __name__ == "__main__":
    my_key = key_gen()
    IV = numberify(INIT_VEC)
    ciphertext = numberify(encrypt(EXAMPLE_TEXT, my_key, INIT_VEC))
    blocks = blockify(ciphertext)

    cleartext = []
    for block_num, (c1, c2) in enumerate(zip([IV]+blocks, blocks)):
        print "cracking block {} out of {}".format(block_num+1, len(blocks))
        i2 = [0] * 16
        p2 = [0] * 16
        for i in xrange(15,-1,-1):
            for b in xrange(0,256):
                prefix = c1[:i]
                pad_byte = (BLOCK_SIZE-i)
                suffix = [pad_byte ^ val for val in i2[i+1:]]
                evil_c1 = prefix + [b] + suffix
                try:
                    decrypt(stringify(c2), my_key, stringify(evil_c1))
                except InvalidPadding:
                    pass
                else:
                    i2[i] = evil_c1[i] ^ pad_byte
                    p2[i] = c1[i] ^ i2[i]
                    break
        cleartext+=p2
        # print "i2:", i2
        # print "c2:", c2
        # print "p2:", p2
        # print "block:[{}]".format(stringify(p2))
        # print "expected:[{}]".format(EXAMPLE_TEXT[(16 * block_num):(16 * block_num)+16])
    print "========================="
    print stringify(cleartext)
    print "========================="

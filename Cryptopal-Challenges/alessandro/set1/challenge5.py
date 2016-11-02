#!/usr/bin/env python

import crypto

INPUT = "Burning 'em, if you ain't quick and nimble\nI go crazy when I hear a cymbal"

KEY = "ICE"


def repeat_to_length(string_to_expand, length):
   return (string_to_expand * ((length/len(string_to_expand))+1))[:length]


def xor_with_key(string, key):
    char_string = repeat_to_length(key, len(string))
    char_bits = crypto.ascii_to_bits(char_string)
    string_bits = crypto.ascii_to_bits(string)
    xored = crypto.xor(string_bits, char_bits)
    return crypto.bits_to_hex(xored)
    

encrypted = xor_with_key(INPUT, KEY)

print encrypted
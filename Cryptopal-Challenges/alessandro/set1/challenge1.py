#!/usr/bin/env python

import crypto

INPUT = "49276d206b696c6c696e6720796f757220627261696e206c696b65206120706f69736f6e6f7573206d757368726f6f6d"
OUTPUT = "SSdtIGtpbGxpbmcgeW91ciBicmFpbiBsaWtlIGEgcG9pc29ub3VzIG11c2hyb29t"

base64 = crypto.bits_to_base64(crypto.hex_to_bits(INPUT))
print base64

print OUTPUT
print base64 == OUTPUT
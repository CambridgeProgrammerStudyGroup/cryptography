#!/usr/bin/env python

import crypto

INPUT1 = "1c0111001f010100061a024b53535009181c"
INPUT2 = "686974207468652062756c6c277320657965"
OUTPUT = "746865206b696420646f6e277420706c6179"

xored = crypto.words_to_hex(crypto.xor(crypto.hex_to_words(INPUT1), crypto.hex_to_words(INPUT2)))
print xored
print OUTPUT
print OUTPUT == xored
#!/usr/bin/env python

import crypto

INPUT = "1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736"

decrypted_all = [crypto.xor_with_char(INPUT, chr(c)) for c in range(256)]

best = max(decrypted_all, key = lambda x: crypto.count_textchars(x))

print best
#!/usr/bin/env python

import crypto

INPUT_FILE = "4.txt"

with open(INPUT_FILE) as f:
    decrypted_all = [crypto.xor_with_char(line.strip(), chr(c)) 
                        for line in f 
                        for c in range(256)]
    best = max(decrypted_all, key = lambda x: crypto.count_textchars(x))
    print best
        
        

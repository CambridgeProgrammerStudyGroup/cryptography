#!/usr/bin/python

import string
import sys

ALPHABET = list(string.uppercase)

def make_table(offset):
    return dict(zip(ALPHABET,ALPHABET[offset:]+ALPHABET[:offset]))


# brute-force solution to caesar cipher
if __name__ == '__main__':
    
    print ALPHABET    
    text = ""
    if len(sys.argv) == 2:
        with open(sys.argv[1]) as f:
            text = f.read().upper()
        print text
    else:
        print "Usage :",sys.argv[0]," filename"
        sys.exit()
        
    #text.upper()    
    # trying all possible offsets
    for i in range(0,len(ALPHABET)):
        table = make_table(i)
        text_deciphered = ""  
        print "offset=",i
        for c in text:
            text_deciphered += table.get(c,c)
        print text_deciphered

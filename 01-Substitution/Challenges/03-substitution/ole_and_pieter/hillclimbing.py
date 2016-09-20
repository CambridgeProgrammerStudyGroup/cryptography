# -*- coding: utf-8 -*-
"""
Solution to substitution cipher by Pieter and Ole

Created on Wed Jul 20 19:14:20 2016

@author: ole
"""

import sys
import ngram_score as ns
import string

from random import randint

scorer = ns.ngram_score('english_trigrams.txt')

def compute_fitness(text):
    return scorer.score(text)
    
ALPHABET = list(string.ascii_uppercase)

def make_table(key):
    return dict(zip(ALPHABET,key))
    
def decipher(text,table):
    ret = ""    
    for c in text:
        ret += table.get(c,c)
    return ret
    
def mutate_key(key):
    kl = list(key)
    idx1 = randint(0,len(key)-1)
    idx2 = randint(0,len(key)-1)

    tmp = kl[idx1]
    kl[idx1] = kl[idx2]
    kl[idx2] = tmp
    return "".join(kl)

def main():
        
    #print compute_fitness('HELLOWORLD')
    #print compute_fitness('HELLOWORLDTHECAT')
    #print compute_fitness('YAHHFKKAHKANNAK')
    
    text = ""
    if len(sys.argv) == 2:
        with open(sys.argv[1]) as f:
            text = f.read().upper()
        text = "".join(c for c in text if c.isalpha() )
        print text
    else:
        print "Usage :",sys.argv[0]," filename"
        sys.exit()
        
    
    cur_key = ALPHABET
    cur_fitness = compute_fitness(text)
    for i in range(0,10000):
        next_key = mutate_key(cur_key)
        next_tbl = make_table(next_key)
        dec_text = decipher(text,next_tbl)
        next_fitn = compute_fitness(dec_text)
        if next_fitn>cur_fitness:
            cur_key = next_key
            cur_fitness = next_fitn
            print i," ",cur_fitness
            print dec_text

if __name__ == '__main__':
    main()

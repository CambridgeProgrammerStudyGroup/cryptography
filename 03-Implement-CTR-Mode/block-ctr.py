# -*- coding: utf-8 -*-
"""
Created on Wed Sep 14 19:10:04 2016

@author: Stuart 
@author: Brice
"""


#counterMask = (1<<64) -1
#nonceMask = counterMask << 64

from Crypto.Cipher import AES
import struct
import math
import base64

def encryptor(key,nonce,p):
    streamBytes = stream(key,nonce,len(p))
    c = [chr(ord(pi)^ord(si)) for pi, si in zip(p, streamBytes)]
    return "".join(c)

def stream(key,nonce,byteCount):
    #this generates the stream given nonce and key
    cipher=AES.new(key,AES.MODE_ECB)
    output = ""
    n = int(math.ceil(byteCount/16.0))
    for counter in range(0,n):
        output=output + cipher.encrypt(cle(nonce,counter))
    return output[0:byteCount]

def cle(nonce,counter):
    return struct.pack("<Q", nonce)+struct.pack("<Q", counter)

message = base64.b64decode('L77na/nrFsKvynd6HzOoG7GHTLXsTVu9qvY/2syLXzhPweyyMTJULu/6/kXX0KSvoOLSFQ==')
key = "YELLOW SUBMARINE"
nonce = 0

pstring = encryptor(key,nonce,message)
print(pstring)

cstring = encryptor(key,nonce,pstring)
print(cstring)


print encryptor(key,nonce,encryptor(key,nonce, "kthxbye"))

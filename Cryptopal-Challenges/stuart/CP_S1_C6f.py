# -*- coding: utf-8 -*-
"""
Created on Wed Oct 19 15:54:01 2016
@author: Stuart
"""
import random
import timeit
import base64
import string

print("_________________________________________________\n")
print("Cryptopals: Series 1, Challenge 6.")
print("_________________________________________________")

b64="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
if (len(b64)!=64):print("error in length of b64")

def binstring4ToHexc(bs4):
    if (len(bs4)!=4):return -1
    if (bs4=='0000'):return '0'
    if (bs4=='0001'):return '1'
    if (bs4=='0010'):return '2'
    if (bs4=='0011'):return '3'
    if (bs4=='0100'):return '4'
    if (bs4=='0101'):return '5'
    if (bs4=='0110'):return '6'
    if (bs4=='0111'):return '7'
    if (bs4=='1000'):return '8'
    if (bs4=='1001'):return '9'
    if (bs4=='1010'):return 'a'
    if (bs4=='1011'):return 'b'
    if (bs4=='1100'):return 'c'
    if (bs4=='1101'):return 'd'
    if (bs4=='1110'):return 'e'
    if (bs4=='1111'):return 'f'
    
def decToHW2s(dec):
    if (dec>255 or dec<0): return -1
    binstring = bin(dec)[2:].zfill(8)
    lsbin = binstring[4:]
    msbin = binstring[0:4]
    lshex = binstring4ToHexc(lsbin)
    mshex = binstring4ToHexc(msbin)
    return mshex + lshex #string concatenation
    
def Ach2HW2s(c):
    Acode=ord(c)
    return decToHW2s(Acode)

def HexcToBs4(h):
    m = eval('0x' + h)
    k = bin(m)[2:]
    g = k.zfill(4)
    #print("for h=" + str(h) + ", m=" + str(m) + "  k=" + k + "  g=" + g)
    return g

def HW2sToBinary8(hw):
    #print("hw=" + str(hw) + "  " + str(type(hw)))
    if (str(type(hw))=="<type 'str'>"):  
        ls = hw[1:]
        ms = hw[0:1]
        #print("ms=" + ms + "  ls=" + ls)
        msb = HexcToBs4(ms)
        lsb = HexcToBs4(ls)
        #print("msb=" + msb + "  lsb=" + lsb)
    else:
        #print("error: hw in HW2sToBinary8 should be string")        
        ls = bin(hw % 16)[2:].zfill(4)
        ms = str((hw - ls)/16)[2:0].zfill(4)
    return (msb + lsb).zfill(8)

def decToHexc(dec):
    if (dec>15 or dec<0): return '-1'
    if (dec==10): return 'a'
    if (dec==11): return 'b'
    if (dec==12): return 'c'
    if (dec==13): return 'd'
    if (dec==14): return 'e'
    if (dec==15): return 'f'
    return str(dec)

def textToHexstring(p):
    output=''    
    for i in range(0,len(p)):
        output += decToHW2s(ord(p[i:i+1]))
    return output

def textstringToBinarystring(p):
    output=''    
    for i in range(0,len(p)):
        c=bin(ord(p[i:i+1]))[2:].zfill(8)
        #print("i=" + str(i) + "  char=" + p[i:i+1] + "  n=" + str(ord(p[i:i+1])) + "  bin chunk=" + c)
        output += c
    return output    

def binarystringToTextstring(bs):
    lbs = len(bs)
    output = ''
    for i in range(0,int(lbs/8)):
        acb = bs[8*i:8*(i+1)]
        c=chr(eval('0b'+acb))
        #print("i=" + str(i) + "  acb=" + acb + "  c=" + c)
        output += c
    return output
    
def binarystringToBase64string(d1):
    fit = len(d1) % 24    
    #print("fit=" + str(fit))
    if (fit!=0):
        for i in range(0,fit):
            d1 += '0'
    #umber of 6-bit chunks is len(d)/6
    n=len(d1)/6
    output=''
    for i in range(0,n):
        chunk = d1[6*i:6*(i+1)]
        b64c = b64[eval('0b' + chunk)]
        output += b64c
        #print("i=" + str(i) + "  chunk=" + chunk + "  val=" + str(eval('0b' + chunk)) + "  b64c=" + b64c)
    return output

def base64stringToBinaryString(b64s):
    #print("Q has index " + str(b64.index('Q')) + " in b64.")
    lb64s=len(b64s)
    if (lb64s % 4 !=0):print("error in b64s length.")
    output = ''
    for i in range(0,lb64s):
        b64c = b64s[i]
        binchunk = bin(b64.index(b64c))[2:].zfill(6)
        output += binchunk
        print("i=" + str(i) + "  b64c=" + b64c + "  binchunk=" + binchunk)
    return output

def binToHexs(bins):
    lbins = int(len(bins)/4)
    output = ''
    for i in range(0,lbins):
        bin4 = bins[4*i:4*(i+1)]
        Hc = binstring4ToHexc(bin4)
        output += Hc
    return output
    
def binsXOR(bs1,bs2):
    lbs1 = len(bs1)
    lbs2 = len(bs2)
    if (lbs1!=lbs2):print("ERROR: bs1 and bs2 have different lengths")
    output = ''
    for i in range(0,lbs1):
        if (bs1[i]==bs2[i]):
            output += '0'
        else:
            output += '1'
    return output

def dXOR(hs1,hs2):
    lhs1 = len(hs1)
    lhs2 = len(hs2)
    #print("\nhs1=" + hs1 + "\nhs2=" + hs2)
    if (lhs1!=lhs2):print("ERROR: hs1 and hs2 have different lengths")
    output = ''
    for i in range(0,int(lhs1/2)):
        #print("hs1_at i: " + hs1[2*i:2*(i+1)])
        #print("hs2_at i: " + hs2[2*i:2*(i+1)])
        dec1 = ord(chr(eval('0x' + hs1[2*i:2*(i+1)])))
        dec2 = ord(chr(eval('0x' + hs2[2*i:2*(i+1)])))
        dec3 = dec1 ^ dec2
        output += decToHW2s(dec3)
    return output
    
def h2t_scXOR(hex1,code1):
    if (code1>255 or code1<0):print("ERROR: code1 out of bounds")
    lhex1=len(hex1)
    output = ''
    score1 = 0
    score2 = 0
    for i in range(0,int(lhex1/2)):
        hw = hex1[2*i:2*(i+1)]
        dec = eval('0x' + hw)
        xvalue = dec ^ code1
        #eliminate non-printable character strings via the fitness counters
        if (xvalue in range(0,32)):
            score1 = -100
            score2 = -100
        if (xvalue in range(32,127)):
            score1 += 1
            if (chr(xvalue) in ['e','t','a','o','i','n']):
                score2 += 1
        c3 = chr(xvalue)
        output += c3
    return [output,score1,score2]
    
def XORsl(hex,key):
    lh1 = len(hex)
    lk1 = len(key)
    if (lh1 > lk1):
        print("ERROR: XORsl requires hex strings og equal length")
        return -1
    output = ''    
    for i in range(0,int(lh1/2)):
        dech = eval('0x' + hex[2*i:2*(i+1)])
        deck = eval('0x' + key[2*i:2*(i+1)])
        dec3 = dech ^ deck
        hex3 = decToHW2s(dec3)
        output += hex3
    return output
    
def hamming(s1,s2):
    bs1 = textstringToBinarystring(s1)
    bs2 = textstringToBinarystring(s2)
    if (len(bs1)!=len(bs2)):
        raise Exception('hamming strings not equal length')
    count1 = 0
    for i in range(0,len(bs1)):
        if (bs1[i]!=bs2[i]):
            count1 += 1
    return count1
    
#££££££££££££££££££££££££££££££££££££££££££££££££££££££££££££££££££££££££££
start_time = timeit.default_timer()
elapsed = timeit.default_timer() - start_time
#print("First use execution time: " + str(elapsed) + " seconds\n")
#££££££££££££££££££££££££££££££££££££££££££££££££££££££££££££££££££££££££££

#££££££££££££££££££££££££££££££££££££££££££££££££££££££££££££££££££££££££££
start_time = timeit.default_timer()
print("\nStart\n")

s1 = "this is a test"
s2 = "wokka wokka!!!"

print("TEST HAMMING FUNCTION: expect HD=37. Calculated=" + str(hamming(s1,s2)))

with open('6.txt') as f:
    content = f.read()
    
    b1 = base64.b64decode(content)
    #print("b1=" + b1)

def vignerelength(s,minv=2,maxv=41):
    print("running vignerelength")
    bestLength = 0
    smallestScore = 8
    maxslice = 10    
    for KEYSIZE in range(minv,maxv):
        nhdavg = 0
        for i in range(0,maxslice):
            slice0 = s[i*KEYSIZE:(i+1)*KEYSIZE]
            slice1 = s[(i+1)*KEYSIZE:(i+2)*KEYSIZE]
            hd = hamming(slice0,slice1)
            nhd = hd/float(KEYSIZE)
            nhdavg += nhd/float(maxslice)
        print("maxslice=" +str(maxslice) +"\tKEYSIZE="+str(KEYSIZE)+"\tnhdavg="+str(nhdavg))
        if (nhdavg<smallestScore):
            smallestScore = nhdavg
            bestLength = KEYSIZE
    return bestLength
    
groupdict={}
groupdict[0]=['e','E']
groupdict[1]=['t','T','a','A']
groupdict[2]=['o','O','i','I']
groupdict[3]=['n','N','s','S']
groupdict[4]=['h','H','r','R']
groupdict[5]=['d','D','l','L','c','C']
groupdict[6]=['u','U','m','M','w','W','f','F']
groupdict[7]=['g','G','y','Y','p','P','b','B','v','V','k','K','j','J','x','X','q','Q','z','Z']
groupdict[8]=['.',',','!','\"','\'','@','#','~','+','-','£','$','%','^','&','*','(',')','_','{','}','[',']','?','<','>','/','\\','0','1','2','3','4','5','6','7','8','9']
groupdict[9]=[' ']

fdict = {}
fdict[0] = 0.12702
fdict[1] = 0.17223
fdict[2] = 0.14473
fdict[3] = 0.13076
fdict[4] = 0.12081
fdict[5] = 0.11060
fdict[6] = 0.09753
fdict[7] = 0.09632
fdict[8] = 0
fdict[9] = 0

countg = {}

def fitnessPureABC(str1):
    ls = len(str1)
    npc=0  #non-printable characters  31<ord(c)<128
    nnlc=0  #expect 1 new line character, ord(c)=10
    for m in range(0,10):
        countg[m]=0
    for i in range(0,ls):
        if ((ord(str1[i])<32) or (ord(str1[i])>128)):npc += 1
        if ((ord(str1[i])==10)):nnlc += 1
        for j in range(0,10):
            if (str1[i] in groupdict[j]):
                countg[j] += 1
    abc = ls - countg[8] - npc
    propabc = (abc*1.0)/(ls*1.0-nnlc) 
    return propabc

def chunks(s,l):
    print("Running chunks(s,l)")
    chunksL = []
    while len(s)>0:
        chunksL.append(s[0:l])
        s = s[l:]
    return chunksL

#print("ChunksL:" + str(chunks('abcdefghijklmn',3)))

def scXOR(s,ch):
    ol = []
    for c in s:
        ol.append(chr(ord(c)^ord(ch)))
    return ''.join(ol)
    
def englishScore(s):
    acceptable = set(string.letters + " ")
    return float(len([c for c in s if c in acceptable]))/len(s)
    
def solveScXOR(ciphertext):
    #print("Running solveScXOR")
    candidates = range(0,256)
    solutions = [(scXOR(ciphertext, chr(ch)), chr(ch)) for ch in candidates]
    def score(solutionCharPair):
        return englishScore(solutionCharPair[0])
    bestpair = max(solutions, key=score)
    return bestpair[1]

def solveVignere(s):
    print("\nRunning solveVignere")
    AKeySize = vignerelength(s)
    print("\nvignere length = " + str(AKeySize))
    chch = chunks(b1,AKeySize)
    chch = chch[0:-1] #done to ensure zip truncates the minimum - last cypher will need adding back to final solution
    #print("first:" + str(len(chch[0])) + "last:" + str(len(chch[-1])))
    cyphers = zip(*chch)
    return "".join([solveScXOR(cypher) for cypher in cyphers]) 

print("Solving to find each character in string of Vignere length")
print(solveVignere(b1))

def decryptVignere(cyphertext,key):
    print("Running decryptVignere\n")
    longkey = key*(len(cyphertext)/(len(key))+1)
    return "".join([chr(ord(a)^ord(b)) for a,b in zip(cyphertext, longkey)])
    
print decryptVignere(b1, solveVignere(b1))

elapsed = timeit.default_timer() - start_time
print("\nSolution execution time: " + str(elapsed) + " seconds\n")
#££££££££££££££££££££££££££££££££££££££££££££££££££££££££££££££££££££££££££


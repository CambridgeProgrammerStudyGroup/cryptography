#!/usr/bin/env python
import sys
import string
import random
import utils 

def mkCaesar(key):
	def shift(c, preserveCase=True):
		if c in string.letters:
			if preserveCase:
				base = ord('A') if c in string.uppercase else ord('a')
			else:
				base = ord('A')
			return chr(base+((ord(c) - base)+key)%26)
		else:
			return c
	return shift

class Substitution(object):
	def __init__(self, table):
		self.e_table = table
		self.e_transform = utils.mkTransform(table)
		self.d_table = utils.invert(table)
		self.d_transform = utils.mkTransform(self.d_table)

	@staticmethod
	def _crypt(t, table, transform, preserveUnknown=False):
		if preserveUnknown:
			return "".join(map(lambda t: transform(t) if t in table else t, t))
		else:
			return "".join(map(lambda t: transform(t) if t in table else "", t))

	def encrypt(self, plaintext, preserveUnknown=False):
		return Substitution._crypt(plaintext, self.e_table, self.e_transform, preserveUnknown=preserveUnknown)
		
	def decrypt(self, ciphertext, preserveUnknown=False):
		return Substitution._crypt(ciphertext, self.d_table, self.d_transform, preserveUnknown=preserveUnknown)

def Caesar(n):
	caesar = mkCaesar(n)
	rotDict = dict(map(lambda p: (p, caesar(p)), string.letters))
	return Substitution(rotDict)

def RandomAffine(n):

if __name__ == "__main__":
	import argparse

	parser = argparse.ArgumentParser(description='Use a substitution cipher')
	parser.add_argument('--rot13 FILENAME', dest="rot13", help='encode the file with rot13, print out the result on the command line')
	parser.add_argument('--caesar N FILENAME', dest="caesar", nargs=2, help='encode the file with a caesar shift of N')
	parser.add_argument('--keep-unknown', action='store_true', default=False, help='preserve all characters when encrypting (punctuation and spaces)')
	parser.add_argument('--sub-shuffle FILENAME', dest='sub_shuffle', help="encrypt with random shuffle cipher. (will print out the key used after the ciphertext)")

	args = parser.parse_args()

	if args.rot13:
		cipher = Caesar(13)
		filename = args.rot13
	if args.caesar:
		cipher = Caesar(int(args.caesar[0]))
		filename = args.caesar[1]

	with open(filename) as inFile:
		if args.keep_unknown:
			print cipher.encrypt(inFile.read(), preserveUnknown=args.keep_unknown)
		else:
			print utils.blockFormat(cipher.encrypt(inFile.read()))
	




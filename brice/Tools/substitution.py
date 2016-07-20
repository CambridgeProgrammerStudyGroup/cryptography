#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import string
import random
import utils 
import itertools
import json


class Substitution(object):
	def __init__(self, table, preserveAll=False):
		self.preserveAll = preserveAll
		self.e_table = table
		self.e_transform = utils.mkTransform(table)
		self.d_table = utils.invert(table)
		self.d_transform = utils.mkTransform(self.d_table)

	def _crypt(self, t, table, transform):
		if self.preserveAll:
			return "".join(map(lambda t: transform(t) if t in table else t, t))
		else:
			return "".join(map(lambda t: transform(t) if t in table else "", t))

	def encrypt(self, plaintext):
		return self._crypt(plaintext, self.e_table, self.e_transform)
		
	def decrypt(self, ciphertext):
		return self._crypt(ciphertext, self.d_table, self.d_transform)

def Caesar(n, preserveAll=False):
	def shift(c):
		c = c.upper()
		if c in string.letters:
			base = ord('A')
			return chr(base+((ord(c) - base)+n)%26)
		else:
			return c
	rotDict = dict(map(lambda p: (p, shift(p)), string.letters))
	cipher = Substitution(rotDict, preserveAll=preserveAll)
	cipher.key = "".join(map(shift, string.letters))
	return cipher

def RandomSubstitution(preserveAll=False):
	lettersLower = string.lowercase
	lettersUpper = lettersLower.upper()
	randomised = sorted(lettersUpper, key=lambda x: random.random())
	d1 = dict(zip(lettersLower, randomised))
	d2 = dict(zip(lettersUpper, randomised))
	d1.update(d2)
	cipher = Substitution(d1, preserveAll=preserveAll)
	cipher.key = "".join(randomised)
	return cipher

class RandomPolysubstitution(object):
	def __init__(self, n):
		self.n = n
		self.acceptable = set(string.uppercase)
		self.e_table = dict(zip(self.acceptable, utils.nLetterGenerator(self.acceptable, self.n)))
		self.e_transform = utils.mkTransform(self.e_table)
		self.d_table = utils.invert(self.e_table)
		self.d_transform = utils.mkTransform(self.d_table)
		self.key = json.dumps(self.e_table)

	def encrypt(self, plaintext):
		xs = filter(lambda x: x in self.acceptable, plaintext.upper())
		return "".join(map(lambda c: self.e_transform(c), xs))

	def decrypt(self, ciphertext):
		bare = filter(lambda x: x in self.acceptable, ciphertext)
		xs = utils.splitByN(bare, self.n)
		return "".join(map(lambda c: self.d_transform(c), xs))

class WithATwist(object):
	def __init__(self):
		# self.lower=u"aąbcćdeęfghijklłmnńoóprsśtuwyzźż"
		self.upper=u"AĄBCĆDEĘFGHIJKLŁMNŃOÓPRSŚTUWYZŹŻ"
		self.acceptable = set(self.upper)
		bigrams = utils.nLetterGenerator(string.uppercase, 2)
		self.e_table = dict(zip(self.acceptable, bigrams))
		self.e_transform = utils.mkTransform(self.e_table)
		self.d_table = utils.invert(self.e_table)
		self.d_transform = utils.mkTransform(self.d_table)
		self.key = json.dumps(self.e_table)

	def encrypt(self, plaintext):
		pt = plaintext.decode('utf-8').upper()
		xs = filter(lambda x: x in self.acceptable, pt)
		ciphertext = "".join(map(lambda c: self.e_transform(c), xs))
		return ciphertext

	def decrypt(self, ciphertext):
		bare = filter(lambda x: x in string.uppercase, unicode(ciphertext))
		xs = utils.splitByN(bare, 2)
		return "".join(map(lambda c: self.d_transform(c), xs))

	def loadKey(self, table):
		self.e_table = table
		self.e_transform = utils.mkTransform(self.e_table)
		self.d_table = utils.invert(self.e_table)
		self.d_transform = utils.mkTransform(self.d_table)
		self.key = json.dumps(self.e_table)
		



if __name__ == "__main__":
	import argparse
	import inspect

	ciphers = [
		('rot13', 			lambda: Caesar(13)),
		('rot13-keep', 		lambda: Caesar(13, preserveAll=True)),
		('caesar', 			lambda shift: Caesar(int(shift))),
		('caesar-keep',		lambda shift: Caesar(int(shift), preserveAll=True)),
		('shuffle',			lambda: RandomSubstitution()),
		('shuffle-keep',	lambda: RandomSubstitution(preserveAll=True)),
		('random-poly', 	lambda num_chars: RandomPolysubstitution(int(num_chars))),
		('eastern-twist',	lambda: WithATwist())
	]

	def showCiphers(ciphers):
		for name, constructor in ciphers:
			print("{}: {}".format(name, str(inspect.getargspec(constructor).args)))


	parser = argparse.ArgumentParser(description='Use a substitution cipher')
	parser.add_argument('--ciphers', action='store_true', dest="show_ciphers", help="Show cipher suites and options")
	parser.add_argument('--cipher', dest="cipher", help="Choose cipher")
	parser.add_argument('--cipher-options', nargs="*", dest="options", help="Cipher options")
	parser.add_argument('--save-key FILENAME', dest="save_key", help="Save the key into a file in a json format")
	parser.add_argument('--plaintext FILENAME', dest="plainfile", help="Select a plaintext file to encrypt. Output will be on STDOUT")
	parser.add_argument('--noblock', dest="noblock", action="store_true", help="Stop block output formatting")
	parser.add_argument('--load-key', dest="keyfile", help="Load a key to decrypt")
	parser.add_argument('--ciphertext FILNAME', dest="ciphertext", help="The file to be decrypted" )
	args = parser.parse_args()

	if args.show_ciphers:
		showCiphers(ciphers)
		sys.exit()

	if not args.cipher:
		print "We can't proceed without a cipher."
		showCiphers(ciphers)
		sys.exit()

	# Build the Cipher
	constructor = dict(ciphers)[args.cipher]
	expected_options = len(inspect.getargspec(constructor).args)
	if expected_options > 0 and (not args.options or not len(args.options) == expected_options):
		print "Insufficent options for cipher."
		showCiphers(ciphers)
		sys.exit()
	cipher = constructor(*args.options) if args.options else constructor()

	if args.plainfile:
		with open(args.plainfile) as inFile:
			if args.noblock:
				print cipher.encrypt(inFile.read().decode('utf-8'))
			else:
				print utils.blockFormat(cipher.encrypt(inFile.read()))

	if args.keyfile and args.ciphertext:
		with open(args.keyfile) as kf:
			key = json.load(kf)
			cipher.loadKey(key)
		with open(args.ciphertext) as ct:
			ciphertext = ct.read().decode('utf-8')
			print cipher.decrypt(ciphertext)

	if args.save_key:
		with open(args.save_key, "w") as kf:
			kf.write(cipher.key)
	




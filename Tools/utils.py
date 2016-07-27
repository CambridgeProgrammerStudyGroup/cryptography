import string
import random
import itertools

def splitByN(seq, n):
	return [seq[i:i+n] for i in range(0, len(seq), n)]

def blockFormat(text, blockwidth=5, blocks=8):
	text=text.upper()
	letters = set(string.uppercase)
	return "\n".join(map(lambda x: " ".join(x), splitByN(splitByN(filter(lambda c: c in letters, text), blockwidth), blocks)))

def nLetterGenerator(characters, n):
	strings = map(lambda x: "".join(x), itertools.combinations(characters, n))
	return sorted(strings, key=lambda x: random.random())

def invert(table):
	inverse = {}
	for k,v in table.items():
		if isinstance(v, str) or isinstance(v, unicode):
			inverse[v]=k
		else:
			try: # handle polysubstitution ciphers properly
				for item in v:
					inverse[item] = k
			except TypeError, te:
				inverse[v]=k
	return inverse

def mkTransform(table):
	"""
	Supports polyalphabetic substitution ciphers to 
	defeat naive frequency analysis
	"""
	def substitute(p):
		subs = table[p]
		if isinstance(subs, str) or isinstance(subs, unicode):
			return subs
		else:
			try:
				return random.choice(subs)
			except TypeError, te:
				return subs

	return substitute
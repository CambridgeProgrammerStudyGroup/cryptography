#!/usr/bin/env python

from collections import defaultdict
import json
import os.path
import math
import random
import string

CORPUS_PATH = "../diner/03_substitution/corpus/corpus_en.txt"
CIPHER_PATH = "../01-Substitution/03-substitution/cipher.txt"
DATA_PATH = 'dat.json'

def splitByN(seq, n):
	return [seq[i:i+n] for i in range(0, len(seq), n)]

def blockFormat(text, blockwidth=5, blocks=8):
	text=text.upper()
	letters = set(string.uppercase)
	return "\n".join(map(lambda x: " ".join(x), splitByN(splitByN(filter(lambda c: c in letters, text), blockwidth), blocks)))

def getText(fname):
    text = ""
    with open(fname, 'r') as fp:
        text = fp.read()
    return text

def nGramFrequencies(n, text):
    freqs = defaultdict(int)
    nGrams = len(text)-n
    for i in range(nGrams):
        substring = text[i:i+n]
        freqs[substring] += 1
    for k in freqs.keys():
        freqs[k] = freqs[k] / float(nGrams+1)
    return dict(freqs)

def getReference():
    if os.path.isfile(DATA_PATH):
        with open(DATA_PATH, 'r') as fp:
            reference = json.load(fp)
    else:
        text =  getText(CORPUS_PATH)
        reference = {
            "oneGrams": nGramFrequencies(1,text),
            "twoGrams": nGramFrequencies(2,text),
            "threeGrams": nGramFrequencies(3,text)
        }
        with open(DATA_PATH, 'w') as fp:
            json.dump(reference, fp)
    return reference

def compareHistograms(reference,test):
    # Kullback Leibler Divergence (discrete)
    frequencies = [(reference[k], test[k]) for k in reference.keys() if k in test]
    return sum([r* math.log(r/t) for r,t in frequencies])

def matchesReference(text, reference):
	"""Will return how well a text matches the reference language,
	where 'reference' encodes the language characteristics.

	a return value of 0.0 is a perfect match, with greater
	values signifying worse matches"""
	# oneGrams = nGramFrequencies(1,text)
	twoGrams = nGramFrequencies(2,text)
	# threeGrams = nGramFrequencies(3,text)
	return compareHistograms(reference["twoGrams"], twoGrams)

def bestGuess(text, reference):
    sorted_text_onegrams = sorted(nGramFrequencies(1,text).items(), key=lambda x: x[1])
    sorted_ref_onegrams = sorted(reference["oneGrams"].items(), key=lambda x: x[1])
    maxlen = min([len(sorted_ref_onegrams), len(sorted_text_onegrams)])
    sorted_text_onegrams = sorted_text_onegrams[-maxlen:]
    sorted_ref_onegrams = sorted_ref_onegrams[-maxlen:]
    mapping = dict([(t[0],r[0]) for t,r in zip(sorted_text_onegrams, sorted_ref_onegrams)])
    return mapping

def process(text):
    return "".join([c for c in text if c in string.ascii_uppercase])

def mapping2decrypt(mapping):
    def decrypt(text):
        ar = [mapping[c] if c in mapping else "_" for c in text]
        return "".join(ar)
    return decrypt


class Individual(object):
	ciphertext = None
	language_ref = None

	@classmethod
	def fromString(cls, keyStr):
		genome = dict(zip(string.uppercase, keyStr))
		return Individual(genome)

	def __init__(self, genome):
		self.genome = genome
		self._fitness = None

	def fitness(self):
		if self._fitness:
			return self._fitness
		decryptionFunction = mapping2decrypt(self.genome)
		self._fitness = matchesReference(decryptionFunction(Individual.ciphertext), Individual.language_ref)
		return self._fitness

	def __str__(self):
		return "Individual({}, {})".format(getKeyString(self.genome), self.fitness())



def GA(population, mutate, crossover, stopPredicate, fitness, maxiter=10000):
	pop = population
	iters = 0
	while iters < maxiter and not stopPredicate(pop):
		iters += 1
		breedingPairs, survivors = select(pop, fitness)
		children = [ mutate(crossover(a,b)) for a,b in breedingPairs ]
		pop = children + survivors
		best = max(pop, key=lambda x: x.fitness)
		print("[{}]: Best is {}".format(iters, best))
	return best

def mutate(individual):
	k1 = random.choice(individual.genome.keys())
	k2 = random.choice(individual.genome.keys())
	v1 = individual.genome[k1]
	individual.genome[k1] = individual.genome[k2]
	individual.genome[k2] = v1
	return individual

def getKeyString(mapping):
	kvPairs = sorted(mapping.items(), key=lambda x:x[0])
	return "".join([v for k,v in kvPairs])

def crossover2(i1, i2):
	ks1 = getKeyString(i1.genome)
	ks2 = getKeyString(i2.genome)

	charsByIndex = [(c, (ks1.index(c) + ks2.index(c))/2.0 ) for c in string.uppercase]
	orderedCharsByIndex = sorted(charsByIndex, key=lambda x: x[1])
	orderedChars = map(lambda x: x[0], orderedCharsByIndex)
	genome = dict(zip(string.uppercase, orderedChars))

	return Individual(genome)

def select(population):
	pass

def generateIndividual():
	return Individual.fromString(sorted(string.uppercase, key=lambda x: random.random()))


if __name__ == "__main__":
	en_reference = getReference()
	corpus_text = getText(CORPUS_PATH)

	cipher_text = process(getText(CIPHER_PATH))


	mapping = bestGuess(cipher_text, en_reference)
	decrypt = mapping2decrypt(mapping)
	decrypted_text = decrypt(cipher_text)

	# print(matchesReference(corpus_text, en_reference))
	print(matchesReference(cipher_text, en_reference))
	print(matchesReference(decrypted_text, en_reference))
	print("=============")

	Individual.ciphertext = cipher_text
	Individual.language_ref = en_reference

	i1 = generateIndividual()
	i2 = generateIndividual()
	i3 = crossover2(i1,i2)
	print(i1)
	print(i2)
	print(i3)

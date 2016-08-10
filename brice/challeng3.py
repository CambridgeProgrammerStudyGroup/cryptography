#!/usr/bin/env python

from collections import defaultdict
import json
import os.path
import math
import sys
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
    return sum([pow(abs(t-r),2) for r,t in frequencies])

def matchesReference(text, reference):
	"""Will return how well a text matches the reference language,
	where 'reference' encodes the language characteristics.

	a return value of 0.0 is a perfect match, with greater
	values signifying worse matches"""
	oneGrams = nGramFrequencies(1,text)
	twoGrams = nGramFrequencies(2,text)
	# threeGrams = nGramFrequencies(3,text)
	return compareHistograms(reference["twoGrams"], twoGrams)

def bestGuess(text, reference):
	text_onegrams = nGramFrequencies(1,text)
	for c in string.uppercase:
		if c not in text_onegrams:
			text_onegrams[c] = 0.0

	sorted_text_onegrams = sorted(text_onegrams.items(), key=lambda x: x[1])
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

def orderedStringFromOneGramFrequencies(char_freq_dict):
	sorted_chars_freqs = sorted(char_freq_dict.items(), key=lambda x: x[1])
	decreasing = sorted_chars_freqs[::-1]
	just_chars = [c for c,v in decreasing]
	return "".join( just_chars )

def decipherWith(individual, ciphertext):
	decryption_function = mapping2decrypt(individual.genome)
	plaintex_candidate = decryption_function(ciphertext)
	return plaintex_candidate

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
		attempted_decryption = decryptionFunction(Individual.ciphertext)
		self._fitness = 1.0/matchesReference(attempted_decryption, Individual.language_ref)
		if self._fitness < 0.0:
			self._fitness = 0.0
		assert self._fitness >= 0.0
		return self._fitness

	def crossover(self, other):
		ks1 = getKeyString(self.genome)
		ks2 = getKeyString(other.genome)
		# print self
		# print other
		# assert len(ks1) == 26
		# assert len(ks2) == 26
		alpahabetByFrequency = orderedStringFromOneGramFrequencies(self.language_ref["oneGrams"])
		charsByIndex = [(c, (ks1.index(c) + ks2.index(c))/2.0 ) for c in alpahabetByFrequency]
		orderedCharsByIndex = sorted(charsByIndex, key=lambda x: x[1])
		orderedChars = map(lambda x: x[0], orderedCharsByIndex)
		genome = dict(zip(string.uppercase, orderedChars))
		return Individual(genome)

	def __repr__(self):
		return str(self)

	def __str__(self):
		return "Individual({}, {})".format(getKeyString(self.genome), self.fitness())



def GA(population, mutate, select, stopPredicate, iterationCallback=None, maxiter=10000):
	pop = population
	iters = 0
	while iters < maxiter and not stopPredicate(pop):
		iters += 1
		breedingPairs, survivors = select(pop)
		children = [ mutate(a.crossover(b)) for a,b in breedingPairs ]
		pop = children + survivors
		if iterationCallback:
			iterationCallback(pop, iters)
	best = max(pop, key=lambda x: x.fitness())
	return best

def mutate(individual):
	mutations = 5
	def swap(individual):
		k1 = random.choice(individual.genome.keys())
		k2 = random.choice(individual.genome.keys())
		v1 = individual.genome[k1]
		individual.genome[k1] = individual.genome[k2]
		individual.genome[k2] = v1
		return individual
	for i in range(mutations):
		individual = swap(individual)
	return individual

def getKeyString(mapping):
	kvPairs = sorted(mapping.items(), key=lambda x:x[0])
	return "".join([v for k,v in kvPairs])


def select(population, preservation_rate=0.5):
	# fitness proportional selection
	num_survivors = int(preservation_rate*len(population))

	def select_N(N, population):
		# print "start select pop"
		total_fitness = sum([individual.fitness() for individual in population])
		selected = set([])
		population = set(population)
		while len(selected) < N:
			# print "selecting new individual"
			selector = random.random()*total_fitness
			assert selector >= 0.0
			assert total_fitness >= 0.0
			acc = 0.0
			for i in population:
				# print "Accu: {}, Selector: {} Total Fitness: {} I's Fitness: {}".format(acc, selector, total_fitness, i.fitness())
				if (acc < selector <= (acc + i.fitness())):
					total_fitness -= i.fitness()
					selected.add(i)
					population.remove(i)
					break
				acc += i.fitness()
			# print "done selecting individual"
		# print "endselect pop"
		return list(selected)

	survivors = sorted(population, key=lambda i: i.fitness())[-num_survivors:]

	# survivors = select_N(num_survivors, population)
	num_breeding_pairs = len(population) - num_survivors
	breedingPairs = [(random.choice(survivors), random.choice(population)) for i in range(num_breeding_pairs)]
	return (breedingPairs, survivors)

def generateIndividual():
	return Individual.fromString(sorted(string.uppercase, key=lambda x: random.random()))

if __name__ == "__main__":
	en_reference = getReference()
	corpus_text = getText(CORPUS_PATH)

	cipher_text = process(getText(CIPHER_PATH))

	def show_iteration(pop, iter):
		best = max(pop, key=lambda x: x.fitness())
		decrypt_attempt = decipherWith(best, cipher_text)[:45]
		print("[{}] best of {} is {} >> {}".format(iter, len(population), best, decrypt_attempt))

	Individual.ciphertext = cipher_text
	Individual.language_ref = en_reference

	best_mapping = bestGuess(cipher_text,en_reference)
	bestguess = Individual(best_mapping)
	print "Best guess is ", bestguess
	population = [generateIndividual() for i in range(99)]+[bestguess]
	best = GA(population, mutate, select, lambda x: False, iterationCallback=show_iteration, maxiter=10000)
	print(best)

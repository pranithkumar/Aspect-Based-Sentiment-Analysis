#!/usr/bin/env python

"""
File for aspect extraction functions
"""

import nltk
import sys
import re

from collections import Counter
from nltk.corpus import stopwords

from external.my_potts_tokenizer import MyPottsTokenizer

def get_sentences(review):
	"""
	INPUT: full text of a review
	OUTPUT: a list of sentences

	Given the text of a review, return a list of sentences. 
	"""

	sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')
	
	if isinstance(review, str):
		return sent_detector.tokenize(review)
	else: 
		raise TypeError('Sentence tokenizer got type %s, expected string' % type(review))


def tokenize(sentence):
	"""
	INPUT: string (full sentence)
	OUTPUT: list of strings

	Given a sentence in string form, return 
	a tokenized list of lowercased words. 
	"""

	pt = MyPottsTokenizer(preserve_case=False)
	return pt.tokenize(sentence)


def pos_tag(toked_sentence):
	"""
	INPUT: list of strings
	OUTPUT: list of tuples

	Given a tokenized sentence, return 
	a list of tuples of form (token, POS)
	where POS is the part of speech of token
	"""
	return nltk.pos_tag(toked_sentence)


def aspects_from_tagged_sents(tagged_sentences):
	"""
	INPUT: list of lists of strings
	OUTPUT: list of aspects

	Given a list of tokenized and pos_tagged sentences from reviews
	about a given restaurant, return the most common aspects
	"""

	STOPWORDS = set(stopwords.words('english'))

	# find the most common nouns in the sentences
	noun_counter = Counter()
	entity_counter = Counter()
	i = 0
	for sent in tagged_sentences:
		if re.match('[a-zA-Z0-9_\'/# -!=:?;@]',sent[0]):
			if sent[1]=='NNP' or sent[1]=='NN' and sent[0] not in STOPWORDS:
				noun_counter[sent[0]] += 1
				print "aspect: " + sent[0] + " " + str(i)
				i += 1
			if sent[1] in ['JJ','RB','RBR','RBS','VBN','VBD'] and sent[0] not in STOPWORDS:
				entity_counter[sent[0]] += 1
				print "entity: " + sent[0] + " " + str(i)
				i += 1

	# list of tuples of form (noun, count)
	return [noun for noun, _ in noun_counter.most_common(10)]

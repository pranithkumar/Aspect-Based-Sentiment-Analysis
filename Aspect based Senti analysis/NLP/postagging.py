import json
import nltk
from nltk.corpus import state_union
from nltk.tokenize import PunktSentenceTokenizer

"""
CC 	Coordinating conjunction
CD 	Cardinal number
DT 	Determiner
EX 	Existential there
FW 	Foreign word
IN 	Preposition or subordinating conjunction
JJ 	Adjective
JJR 	Adjective, comparative
JJS 	Adjective, superlative
LS 	List item marker
MD 	Modal
NN 	Noun, singular or mass
NNS 	Noun, plural
NNP 	Proper noun, singular
NNPS 	Proper noun, plural
PDT 	Predeterminer
POS 	Possessive ending
PRP 	Personal pronoun
PRP$ 	Possessive pronoun
RB 	Adverb
RBR 	Adverb, comparative
RBS 	Adverb, superlative
RP 	Particle
SYM 	Symbol
TO 	to
UH 	Interjection
VB 	Verb, base form
VBD 	Verb, past tense
VBG 	Verb, gerund or present participle
VBN 	Verb, past participle
VBP 	Verb, non-3rd person singular present
VBZ 	Verb, 3rd person singular present
WDT 	Wh-determiner
WP 	Wh-pronoun
WP$ 	Possessive wh-pronoun
WRB 	Wh-adverb 
"""


reviews_list_iphone = json.load(open("../data_scraping/reviewscraper/data/amazon/Apple-iPhone-Space-Grey-32GB.json","r"))
reviews_iphone = []
for i in range(0,len(reviews_list_iphone)):
	for review in reviews_list_iphone[i][u'review']:
		reviews_iphone.append(review)
strreviews_iphone = ''
for review in reviews_iphone:
	strreviews_iphone+=review


reviews_list_honor6x = json.load(open("../data_scraping/reviewscraper/data/amazon/Honor-6X-Grey-32GB.json","r"))
reviews_honor6x = []
for i in range(0,len(reviews_list_iphone)):
	for review in reviews_list_iphone[i][u'review']:
		reviews_honor6x.append(review)
strreviews_honor6x = ''
for review in reviews_honor6x:
	strreviews_honor6x+=review

#train_text = state_union.raw(strreviews_honor6x)
#sample_text = state_union.raw(strreviews_iphone)

custom_sent_tokenizer = PunktSentenceTokenizer(strreviews_honor6x)
tokenized = custom_sent_tokenizer.tokenize(strreviews_iphone)

def process_content():
	try:
		for i in tokenized:
			words=nltk.word_tokenize(i)
			tagged=nltk.pos_tag(words)
			print tagged

	except Exception as e:
		print str(e)

process_content()
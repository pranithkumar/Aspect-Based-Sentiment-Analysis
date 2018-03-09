import nltk
from rake_nltk import Rake
from nltk.tokenize import word_tokenize
import datapreprocessing as dp

r = Rake()
df = dp.dataframecomplete('Apple-iPhone-Space-Grey-32GB.json','apple-iphone-6-space-grey-32-gb.json')
#print df['review']
for review in df['review']:
	words = []
	review = review.lower()
	r.extract_keywords_from_text(review)
	raked = r.get_ranked_phrases()
	print "\n\n"+review
	print raked
	word_tokens = word_tokenize(review)
	pos = nltk.pos_tag(word_tokens)
	for phrase in raked:
		wordlist = phrase.split(' ')
		words = words+wordlist
	for word in words:
		for tup in pos:
			if tup[0]==word:
				print tup[0]+"\t"+tup[1]
#mytext = "This is a sample text."
#r.extract_keywords_from_text(mytext)
#print r.get_ranked_phrases()
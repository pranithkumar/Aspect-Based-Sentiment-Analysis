import datapreprocessing as dp
from extract_aspects import *
import re

reviews = dp.dataframecomplete('Apple-iPhone-Space-Grey-32GB.json','apple-iphone-6-space-grey-32-gb.json')

for review in reviews['review']:
	res = ' '
	for ch in review:
		if not re.match('[a-zA-Z0-9_\' ]',ch):
			res = res + ' ' + ch + ' '
		else:
			res = res + ch
	review = res[1:]
	print "\n\n\nreview:"
	print review
	tokenized_data = tokenize(review.encode('utf-8'))
	pos_tagged_data = pos_tag(tokenized_data)
	final_aspects = []
	print "aspects :"
	aspects_data = aspects_from_tagged_sents(pos_tagged_data)
	for asp in aspects_data:
		if re.match('[a-zA-Z0-9_\' -!=:?;@]',asp):
			final_aspects.append(asp)
	print final_aspects
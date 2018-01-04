import json
from autocorrect import spell

reviews_list = json.load(open("../../data_scraping/reviewscraper/data/amazon/Apple-iPhone-Space-Grey-32GB.json","r"))
reviews = []
for i in range(0,len(reviews_list)):
	for review in reviews_list[i][u'review']:
		reviews.append(review)
for text in reviews:
	tokens = text.split(' ')
	result = ''
	for s in tokens:
	    result += spell(s)+" "
	print result
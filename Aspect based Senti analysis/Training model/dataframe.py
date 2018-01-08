import json,pandas
reviews_list = json.load(open("Cell_Phones_and_Accessories_5.json","r"))
for i in range(0,len(reviews_list)):
	reviews_list[i].pop('reviewerID')
	reviews_list[i].pop('asin')
	reviews_list[i].pop('helpful')
	reviews_list[i].pop('unixReviewTime')
	reviews_list[i].pop('reviewTime')

df = pandas.DataFrame(reviews_list)
del df['reviewerName']
print df
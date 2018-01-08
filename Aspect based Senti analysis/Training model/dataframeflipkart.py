import json,pandas
reviews_list = json.load(open("apple-iphone-6-space-grey-32-gb.json","r"))

for i in range(0,len(reviews_list)):
	reviews_list[i].pop('date')
	reviews_list[i].pop('reviewer')
	reviews_list[i].pop('verification')

df = pandas.DataFrame(reviews_list)
print df
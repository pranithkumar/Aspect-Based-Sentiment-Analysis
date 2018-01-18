import json,pandas
reviews_list = json.load(open("Apple-iPhone-Space-Grey-32GB.json","r"))
df = pandas.DataFrame()

for i in range(0,len(reviews_list)):
	reviews_list[i].pop('date')
	reviews_list[i].pop('reviewer')
	reviews_list[i].pop('verification')

for i in range(0,len(reviews_list)):
	df = df.append(pandas.DataFrame(reviews_list[i]),ignore_index=True)

#print df
f = open("rev_amazon.txt","w")
f.write(df.reviews)

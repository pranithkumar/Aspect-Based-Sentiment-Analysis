import pandas
amazontext = pandas.read_json("~/Documents/Amazon_reviews_only.json")

#print amazontext['reviewText']
f = open("testtext.txt","w")

i = 0
for text in amazontext['reviewText']:
	if i== 20:
		break
	if i>10:
		f.write(text+"\n")
	i = i + 1
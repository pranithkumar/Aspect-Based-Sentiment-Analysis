import json,pandas

def dataframeflipkart(inputfile):
	reviews_list = json.load(open(inputfile,"r"))

	for i in range(0,len(reviews_list)):
		reviews_list[i].pop('date')
		reviews_list[i].pop('reviewer')
		reviews_list[i].pop('verification')

	df = pandas.DataFrame(reviews_list)
	return df

def dataframeamazon(inputfile):
	reviews_list = json.load(open(inputfile,"r"))
	df = pandas.DataFrame()

	for i in range(0,len(reviews_list)):
		reviews_list[i].pop('date')
		reviews_list[i].pop('reviewer')
		reviews_list[i].pop('verification')

	for i in range(0,len(reviews_list)):
		df = df.append(pandas.DataFrame(reviews_list[i]),ignore_index=True)

	return df

def dataframecomplete(inputamazon,inputflipkart):
	dfa = dataframeflipkart(inputflipkart)
	dff = dataframeamazon(inputamazon)
	df = dfa.append(dff,ignore_index=True)
	return df

print dataframecomplete('Apple-iPhone-Space-Grey-32GB.json','apple-iphone-6-space-grey-32-gb.json')
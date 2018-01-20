import json,pandas,nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer, WordNetLemmatizer

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

def preprocess(data):
	df = pandas.DataFrame()
	result = []
	stop_words = set(stopwords.words('english'))
	stemmer = PorterStemmer()
	lemmatizer = WordNetLemmatizer()
	count = 0
	for review in data['review']:
		result.append({'stprmv':[],'stem':[],'lemma':[],'pos':[]})
		word_tokens = word_tokenize(review)
		filtered_sentence = [w for w in word_tokens if not w in stop_words]
	   	stprmv = ''
	   	for w in filtered_sentence:
	   		stprmv+=' '+w
	   	result[count]['stprmv'].append(stprmv[1:])

	   	stem = []
		for sentence in filtered_sentence:
			stem.append(stemmer.stem(sentence))
		result[count]['stem'].append(stem)		

	   	lemma = []
		for sentence in filtered_sentence:
			lemma.append(lemmatizer.lemmatize(sentence, pos='v'))
		result[count]['lemma'].append(lemma)

		pos = nltk.pos_tag(word_tokens)
		result[count]['pos'].append(pos)
		
		count += 1
	return pandas.DataFrame(result)

df = dataframecomplete('Apple-iPhone-Space-Grey-32GB.json','apple-iphone-6-space-grey-32-gb.json')
#print df['review']
print preprocess(df).to_json("preprocessing.txt",orient='records')
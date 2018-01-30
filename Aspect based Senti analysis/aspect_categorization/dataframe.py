import json
import pandas
import numpy
import nltk
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
	for review in data['reviewText']:
		print count
		if count == 100000:
			break
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

def count_postagged_nouns(df_pp):
	nouns_dictionary = {}
	for index, row in df_pp.iterrows():
		temp_list = row['pos']
		for i in temp_list[0]:
			#print i[0].encode("utf-8")
			#print i[1]
			if i[1] == 'NN':
				if i[0].encode("utf-8") in nouns_dictionary:
					nouns_dictionary[i[0].encode("utf-8")] = nouns_dictionary[i[0].encode("utf-8")] + 1
				else:
					nouns_dictionary[i[0].encode("utf-8")] = 1
			elif i[1] == 'NNP':
				if i[0].encode("utf-8") in nouns_dictionary:
					nouns_dictionary[i[0].encode("utf-8")] = nouns_dictionary[i[0].encode("utf-8")] + 1
				else:
					nouns_dictionary[i[0].encode("utf-8")] = 1
			elif i[1] == 'NNPS':
				if i[0].encode("utf-8") in nouns_dictionary:
					nouns_dictionary[i[0].encode("utf-8")] = nouns_dictionary[i[0].encode("utf-8")] + 1
				else:
					nouns_dictionary[i[0].encode("utf-8")] = 1
			elif i[1] == 'NNS':
				if i[0].encode("utf-8") in nouns_dictionary:
					nouns_dictionary[i[0].encode("utf-8")] = nouns_dictionary[i[0].encode("utf-8")] + 1
				else:
					nouns_dictionary[i[0].encode("utf-8")] = 1
			else:
				continue
	return nouns_dictionary

def read_amazondata():
	df = pandas.read_json("Amazon_reviews_only.json")
	#df = pandas.read_json("test.json")
	return df



'''
reviews_list = json.load(open("Cell_Phones_and_Accessories_5.json","r"))
for i in range(0,len(reviews_list)):
	reviews_list[i].pop('reviewerID')
	reviews_list[i].pop('asin')
	reviews_list[i].pop('helpful')
	reviews_list[i].pop('unixReviewTime')
	reviews_list[i].pop('reviewTime')
'''
#df = pandas.DataFrame(reviews_list)

#df = read_amazondata()
#print df
#df_pp = preprocess(df) #.to_json("preprocessing_test.txt",orient='records')
#print df_pp.columns.values
#df_pp.to_csv("onelach_preprocessed.csv", sep=',', encoding='utf-8')
#dict_nn = count_postagged_nouns(df_pp)
#numpy.save('my_file.npy', dict_nn)
#print dict_nn

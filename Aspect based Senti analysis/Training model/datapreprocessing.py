#This file takes the data from the json files and converts it to dataframes and preprocesses it(stopwords removal,stemming and postagging) using nltk
import json,pandas,nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer, WordNetLemmatizer

#function to convert data from flipkart json file to dataframe
def dataframeflipkart(inputfile):
	reviews_list = json.load(open(inputfile,"r"))

	for i in range(0,len(reviews_list)):
		reviews_list[i].pop('date')
		reviews_list[i].pop('reviewer')
		reviews_list[i].pop('verification')

	df = pandas.DataFrame(reviews_list)
	return df

#function to convert data from amazon json file to dataframe
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

#function to combine dataframes of flipkart and amazon
def dataframecomplete(inputamazon,inputflipkart):
	dfa = dataframeflipkart(inputflipkart)
	dff = dataframeamazon(inputamazon)
	df = dfa.append(dff,ignore_index=True)
	return df

#function to preprocess the dataframe
def preprocess(data):
	df = pandas.DataFrame()
	result = []
	stop_words = set(stopwords.words('english'))
	stemmer = PorterStemmer()
	lemmatizer = WordNetLemmatizer()
	count = 0
	#for each review
	for review in data['reviewText']:
		print str(count)+'\t'+review
		result.append({'stprmv':[],'stem':[],'lemma':[],'pos':[]})
		#converting review into tokens of words
		word_tokens = word_tokenize(review)
		#stopword removal
		filtered_sentence = [w for w in word_tokens if not w in stop_words]
	   	stprmv = ''
	   	for w in filtered_sentence:
	   		stprmv+=' '+w
	   	#storing in resultant dataframe
	   	result[count]['stprmv'].append(stprmv[1:])

	   	stem = []
	   	#stemming
		for sentence in filtered_sentence:
			stem.append(stemmer.stem(sentence))
		#storing in resultant dataframe
		result[count]['stem'].append(stem)		

	   	lemma = []
	   	#lemmatization
		for sentence in filtered_sentence:
			lemma.append(lemmatizer.lemmatize(sentence, pos='v'))
		#storing in resultant dataframe
		result[count]['lemma'].append(lemma)

		#POS tagging
		pos = nltk.pos_tag(word_tokens)
		#storing in resultant dataframe
		result[count]['pos'].append(pos)
		
		count += 1
	return pandas.DataFrame(result)

#df = dataframecomplete('Apple-iPhone-Space-Grey-32GB.json','apple-iphone-6-space-grey-32-gb.json')
#print df['review']
#df_pp = preprocess(df).to_json("preprocessing.txt",orient='records')

reviews_list = json.load(open("Cell_Phones_and_Accessories_5.json","r"))
for i in range(0,len(reviews_list)):
	reviews_list[i].pop('reviewerID')
	reviews_list[i].pop('asin')
	reviews_list[i].pop('helpful')
	reviews_list[i].pop('unixReviewTime')
	reviews_list[i].pop('reviewTime')

df = pandas.DataFrame(reviews_list)
del df['reviewerName']
print df['reviewText']
df_pp = preprocess(df)
#print df_pp['pos']

nouns_dictionary = {}

def count_postagged_nouns(df_pp):
	for index, row in df_pp.iterrows():
		temp_list = row['pos']
		temp_list = temp_list[0]
		for i in temp_list:
			#print str(i[0][0])
			#print i[0][1]
			if i[1] == 'NN':
				if str(i[0].encode('utf-8')) in nouns_dictionary:
					nouns_dictionary[str(i[0].encode('utf-8'))] = nouns_dictionary[str(i[0].encode('utf-8'))] + 1
				else:
					nouns_dictionary[str(i[0].encode('utf-8'))] = 1
			elif i[1] == 'NNP':
				if str(i[0].encode('utf-8')) in nouns_dictionary:
					nouns_dictionary[str(i[0].encode('utf-8'))] = nouns_dictionary[str(i[0].encode('utf-8'))] + 1
				else:
					nouns_dictionary[str(i[0].encode('utf-8'))] = 1
			elif i[1] == 'NNPS':
				if str(i[0].encode('utf-8')) in nouns_dictionary:
					nouns_dictionary[str(i[0].encode('utf-8'))] = nouns_dictionary[str(i[0].encode('utf-8'))] + 1
				else:
					nouns_dictionary[str(i[0].encode('utf-8'))] = 1
			elif i[1] == 'NNS':
				if str(i[0].encode('utf-8')) in nouns_dictionary:
					nouns_dictionary[str(i[0].encode('utf-8'))] = nouns_dictionary[str(i[0].encode('utf-8'))] + 1
				else:
					nouns_dictionary[str(i[0].encode('utf-8'))] = 1
			else:
				continue

count_postagged_nouns(df_pp)
print nouns_dictionary

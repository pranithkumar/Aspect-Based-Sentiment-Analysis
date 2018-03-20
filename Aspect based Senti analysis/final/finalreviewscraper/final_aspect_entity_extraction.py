import datapreprocessing as dp
from extract_aspects_mine import *
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import nltk,pandas,re,pprint,sys
from textblob import TextBlob

reload(sys)
sys.setdefaultencoding('utf8')
STOPWORDS = set(stopwords.words('english'))
f=open('new_stopwords','r')
NEWSTOPWORDS = f.read().split('\n')
STOPWORDS = STOPWORDS|set(NEWSTOPWORDS)

def find_sub_list(sl,l):
	result = []
	sll=len(sl)
	for ind in (i for i,e in enumerate(l) if e==sl[0]):
		if l[ind:ind+sll]==sl:
			result.append((ind,ind+sll-1))
	return result

def aspects_from_tagged_sents(tagged_sentences):

	temp = []
	for i in range(0,len(tagged_sentences)):
		temp.append(i)

	count = 0
	res = []
	for sent in tagged_sentences:
		#print sent[0]
		if re.match('[a-zA-Z0-9]',sent[0]):
			res.append(tuple([sent[0],sent[1]]))
			#print "True"
		else:
			temp[count] = -1
			#print "False"
		count += 1

	# find the most common nouns in the sentences
	asp_ent_pair = {}
	noun_sets = [['NN','NN'],['NNP','NNP'],['NNS','NNS'],['NN','NNP'],['NN','NNS'],['NNP','NN'],['NNP','NNS'],['NNS','NN'],['NNS','NNP']]
	c = 0

	tags_list = []
	word_list = []
	for sent in tagged_sentences:
		word_list.append(sent[0])
		tags_list.append(sent[1])

	for noun in noun_sets:
		if find_sub_list(noun,tags_list) != []:
			#print noun
			parts = find_sub_list(noun,tags_list)
			#print parts[0]
			asp = ' '

			for index in range(int(parts[0][0]),int(parts[0][1])+1):
				if tagged_sentences[index][0] not in STOPWORDS:
					if re.match('[a-zA-Z0-9]',tagged_sentences[index][0]):
						temp[index] = -1
						asp += ' ' + tagged_sentences[index][0]

			#print "aspect:" + asp[2:]
			asp_ent_pair[asp[2:]] = {}
			c = 1
	#print temp
	count = 0
	for sent in tagged_sentences:
		if re.match('[a-zA-Z0-9]',sent[0]):
			if sent[1]=='NNP' or sent[1]=='NN' or sent[1]=='NNS':
				if(sent[0] not in STOPWORDS) and (temp[count] != -1):
					#print "aspect:"+sent[0]
					asp_ent_pair[sent[0]] = {}
					c = 1
		count += 1

	for sent in tagged_sentences:
		if re.match('[a-zA-Z0-9_]',sent[0]):
			if c == 0:
				break
			if sent[1] in ['JJ','RB','RBR','RBS','VBN','VBD','VBP']:
					if sent[0] not in STOPWORDS:
						#print "entity: " + sent[0]
						for asp in asp_ent_pair:
							asp_ent_pair[asp][sent[0]] = 1

	if '' in asp_ent_pair:
		asp_ent_pair[''] = {}
	# list of tuples of form (noun, count)
	return asp_ent_pair


def get_aspects(Amazon,Flipkart,input_text):

	if input_text not in STOPWORDS:
		STOPWORDS.add(input_text)

	skip_words = input_text.split(' ')
	for word in skip_words:
		if word not in STOPWORDS:
			STOPWORDS.add(word)

	#Using preprocessed text for categorization
	reviews = dp.dataframecomplete(Amazon,Flipkart)

	#initnalizing the aspects dictionary
	aspects_dict = {}

	#if reviews are taken after preprocessing use below line for looping
	for review in reviews['review']:
		#converting all reviews to lowercase
		review = review.lower()
		res = ' '
		for ch in review:
			if not re.match('[a-zA-Z0-9_\' ]',ch):
				res = res + ' ' + ch + ' '
			else:
				res = res + ch
		review = res[1:]
		#print "\n\n\nreview: "+review

		word_tokens = word_tokenize(review)
		#pos tagging
		pos_tuples = nltk.pos_tag(word_tokens)

		split_sets = []
		split_list = ' '
		final_sets = []
		split_words = [',','.',';','!','?','+']

		for word,pos in pos_tuples:
			if pos == 'CC':
				split_words.append(word)
		
		#print "word tokens:"
		#print word_tokens
		#print "pos tuples:"
		#print pos_tuples

		for word in word_tokens:
			if word in split_words:
				split_sets.append(split_list[2:])
				split_list = ' '
			if word not in split_words:
				split_list += ' ' + word
		split_sets.append(split_list[2:])

		for i in range(0,len(split_sets)):
			if len(split_sets[i])!=0:
				final_sets.append(split_sets[i])

		split_words = [',','.',';']

		#print "sets:"
		#print final_sets

		for sentence in final_sets:
			tokenized_data = tokenize(sentence.encode('utf-8','ignore'))

			#print "tokenized_data:"
			#print tokenized_data
			
			pos_tagged_data = pos_tag(tokenized_data)
			
			#print "pos_tagged_data:"
			#print pos_tagged_data
			
			final_aspects = {}
			
			aspects_data = aspects_from_tagged_sents(pos_tagged_data)

			#print "aspects and entities :"
			#print aspects_data
			
			for asp in aspects_data:
				if asp in aspects_dict:
					for ent in aspects_data[asp]:
						if ent in aspects_dict[asp]:
							aspects_dict[asp][ent] += 1
						else:
							aspects_dict[asp][ent] = 1
				else:
					aspects_dict[asp] = aspects_data[asp]
		i +=1	
	#pprint.pprint(aspects_dict)
	i = 0
	#print '\n\n\n\n\n\n\n\n\n\n'

	for key, value in sorted(aspects_dict.iteritems(), key=lambda (k,v): (v,k),reverse = True):
		if i < 15:
		    pprint.pprint(key)
		    #for ke in aspects_dict[key].keys():
		    	#wrd = key + ' ' + ke
		    	#txt = TextBlob(wrd)
		    	#print "text :" + wrd + "\t\t\tsentiment: " + str(txt.sentiment.polarity)
		    i=i+1
	return aspects_dict
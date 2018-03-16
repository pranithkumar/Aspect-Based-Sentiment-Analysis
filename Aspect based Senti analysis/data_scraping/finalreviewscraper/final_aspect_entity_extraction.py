import datapreprocessing as dp
from extract_aspects_mine import *
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import nltk,pandas,re,pprint,sys
from textblob import TextBlob

reload(sys)  
sys.setdefaultencoding('utf8')
STOPWORDS = set(stopwords.words('english'))

def aspects_from_tagged_sents(tagged_sentences):

	# find the most common nouns in the sentences
	asp_ent_pair = {}
	c = 0

	for sent in tagged_sentences:
		if sent[1]=='NNP' or sent[1]=='NN' or sent[1]=='NNS':
			if sent[0] not in STOPWORDS:
				print "aspect:"+sent[0]
				asp_ent_pair[sent[0]] = {}
				c = 1

	for sent in tagged_sentences:
		if c == 0:
			break
		if sent[1] in ['JJ','RB','RBR','RBS','VBN','VBD','VBP']:
				if sent[0] not in STOPWORDS:
					print "entity: " + sent[0]
					for asp in asp_ent_pair:
						asp_ent_pair[asp][sent[0]] = 1

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
		print "\n\n\nreview: "+review

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

		print "sets:"
		print final_sets

		for sentence in final_sets:
			tokenized_data = tokenize(sentence.encode('utf-8','ignore'))

			#print "tokenized_data:"
			#print tokenized_data
			
			pos_tagged_data = pos_tag(tokenized_data)
			
			#print "pos_tagged_data:"
			#print pos_tagged_data
			
			final_aspects = {}
			
			aspects_data = aspects_from_tagged_sents(pos_tagged_data)

			print "aspects and entities :"
			print aspects_data
			
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
	pprint.pprint(aspects_dict)
	i = 0
	print '\n\n\n\n\n\n\n\n\n\n'

	for key, value in sorted(aspects_dict.iteritems(), key=lambda (k,v): (v,k),reverse = True):
		if i < 15:
		    pprint.pprint(key)
		    #for ke in aspects_dict[key].keys():
		    	#wrd = key + ' ' + ke
		    	#txt = TextBlob(wrd)
		    	#print "text :" + wrd + "\t\t\tsentiment: " + str(txt.sentiment.polarity)
		    i=i+1

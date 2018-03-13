import nltk,pandas,pprint,re
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import datapreprocessing as dp
from textblob import TextBlob

#To give a file explicitly
#amazontext = pandas.read_json("~/Documents/Amazon_reviews_only.json")
#amazontext = pandas.read_json("apple-iphone-6-space-grey-32-gb.json")

#Using preprocessed text for categorization
reviews = dp.dataframecomplete('Apple-iPhone-Space-Grey-32GB.json','apple-iphone-6-space-grey-32-gb.json')

#function that returns the indexes of the sublist that matches a pattern
def find_sub_list(sl,l):
	result = []
	sll=len(sl)
	for ind in (i for i,e in enumerate(l) if e==sl[0]):
		if l[ind:ind+sll]==sl:
			result.append((ind,ind+sll-1))
	return result

#patterns set 1 containing noun
patterns1 = [['NN','NN','VBN','JJ'],['NN','NNS','VBN','JJ'],['NNS','NN','VBN','JJ'],['NNS','NNS','VBN','JJ'],['NN','NN','VBD','JJ'],['NN','NNS','VBD','JJ'],['NNS','NN','VBD','JJ'],['NNS','NNS','VBD','JJ'],['JJ','NN','NN'],['JJ','NN','NNS'],['JJ','NNS','NN'],['JJ','NNS','NNS'],['RB','JJ','NN'],['RBR','JJ','NN'],['RBS','JJ','NN'],['RB','JJ','NNS'],['RBR','JJ','NNS'],['RBS','JJ','NNS'],['RB','RB','NN'],['RBR','RB','NN'],['RBS','RB','NN'],['RB','RB','NNS'],['RBR','RB','NNS'],['RBS','RB','NNS'],['RB','RBR','NN'],['RBR','RBR','NN'],['RBS','RBR','NN'],['RB','RBR','NNS'],['RBR','RBR','NNS'],['RBS','RBR','NNS'],['RB','RBS','NN'],['RBR','RBS','NN'],['RBS','RBS','NN'],['RB','RBS','NNS'],['RBR','RBS','NNS'],['RBS','RBS','NNS'],['NN','VBZ','JJ'],['NNP','NN'],['JJ','NN'],['JJ','NNS'],['VBN','NN'],['VBN','NNS'],['VBD','NN'],['VBD','NNS']]

#patterns set 2 without noun
patterns2 = [['RB','JJ'],['RBR','JJ'],['RBS','JJ'],['RB','VBN'],['RBR','VBN'],['RBS','VBN'],['RB','VBD'],['RBR','VBD'],['RBS','VBD'],['VBN','RB'],['VBN','RBR'],['VBN','RBS'],['VBD','RB'],['VBD','RBR'],['VBD','RBS']]

#initnalizing the aspects dictionary
aspects_dict = {'camera':{},'camera quality':{},'battery':{},'price':{}}

#extracting stopwords
stop_words = set(stopwords.words('english'))

#if reviews are taken explicitly use below line for looping
#for review in amazontext['review']:

#if reviews are taken after preprocessing use below line for looping
for review in reviews['review']:
	#converting all reviews to lowercase
	review = review.lower()
	#adding a space before and after characters that do not belong to regilar expression
	res = ' '
	for ch in review:
		if not re.match('[a-zA-Z0-9_\' ]',ch):
			res = res + ' ' + ch + ' '
		else:
			res = res + ch
	review = res[1:]
	#declaring the nouns list
	nounlist = ['NN','NNS']
	print "\n"+review
	lines = []
	#splitting each review into lines and extracting aspects
	lines = review.split('.')
	#for each line
	for line in lines:
		word_tokens = word_tokenize(line)
		#pos tagging
		pos_tuples = nltk.pos_tag(word_tokens)
		#print pos_tuples
		pos =[]
		#storing pos tags in a sepetare list
		for tag in pos_tuples:
			pos.append(tag[1])
		#evaluating for pattern 1
		for pattern in patterns1:
			if find_sub_list(pattern,pos) != None:
				parts = find_sub_list(pattern,pos)
				for indices in parts:
					#indices = find_sub_list(pattern,pos)
					print pattern
					#print indices
					aspect = ' '
					entity = ' '
					for i in range(int(indices[0]),int(indices[1])+1):
						#concatenating aspects if there are multiple aspects
						if pos_tuples[i][1] in nounlist:
							aspect = aspect + ' ' + pos_tuples[i][0]
						else:
							#concatenating entities if there are multiple entities
							if pos_tuples[i][0] not in stop_words:
								entity = entity + ' ' + pos_tuples[i][0]
						print pos_tuples[i]
					#inserting aspect-entity pairs into the aspects dictionary
					if aspect[2:].encode('utf-8') in aspects_dict:
						if entity[2:] in aspects_dict[aspect[2:].encode('utf-8')]:
							aspects_dict[aspect[2:].encode('utf-8')][entity[2:]] += 1
						else:
							aspects_dict[aspect[2:].encode('utf-8')][entity[2:]] = 1
					else:
						aspects_dict[aspect[2:].encode('utf-8')] = {}
						aspects_dict[aspect[2:].encode('utf-8')][entity[2:]] = 1
		
		#evaluating for pattern 2
		for pattern in patterns2:
			if find_sub_list(pattern,pos) != None:
				parts = find_sub_list(pattern,pos)
				check_noun = {}
				for indices in parts:
					i = 0
					#chacking for the nearest noun from the pattern 2
					for tag in pos_tuples:
						if tag[1] in nounlist:
							if i < parts[0][0]:
								check_noun[i] = parts[0][0] - i
							elif i > parts[0][1]:
								check_noun[i] = i - parts[0][1]
						i = i+1
					#extracting the noun index
					if check_noun:
						noun_index = min(check_noun.items(), key = lambda x: x[1])
						print "considered"
					#indices = find_sub_list(pattern,pos)
					print pattern
					if check_noun:
						print pos_tuples[noun_index[0]]
					#print indices
					aspect = ' '
					entity = ' '
					#concatenating aspects if there are multiple aspects
					if check_noun:
						aspect = aspect + ' ' + pos_tuples[noun_index[0]][0]
					for i in range(int(indices[0]),int(indices[1])+1):
						#concatenating entities if there are multiple entities
						if pos_tuples[i][0] not in stop_words:
							entity = entity + ' ' + pos_tuples[i][0]
						print pos_tuples[i]
					#inserting aspect-entity pairs into the aspects dictionary
					if aspect[2:].encode('utf-8') in aspects_dict:
						if entity[2:] in aspects_dict[aspect[2:].encode('utf-8')]:
							aspects_dict[aspect[2:].encode('utf-8')][entity[2:]] += 1
						else:
							aspects_dict[aspect[2:].encode('utf-8')][entity[2:]] = 1
					else:
						aspects_dict[aspect[2:].encode('utf-8')] = {}
						aspects_dict[aspect[2:].encode('utf-8')][entity[2:]] = 1

#removing empty aspects from aspects dictionary
if '' in aspects_dict.keys():
	aspects_dict.pop('',None)

#pprint.pprint(aspects_dict)
#sorting based on size of value of aspects dictionary and printing the top 10
print "\n\n\nAspect\t\t\tEntity\t\t\tCount\t\t\tSentiment"
for k in sorted(aspects_dict, key=lambda k: len(aspects_dict[k]), reverse=True):
	sot_list = sorted(aspects_dict[k], key=lambda ke: aspects_dict[k][ke], reverse = True)
	for i in sot_list:
		if aspects_dict[k][i] > 1:
			wrd = i+' '+k
			#getting sentiment
			txt = TextBlob(wrd)
			print k + '\t\t\t' + i + '\t\t\t' + str(aspects_dict[k][i]) + '\t\t\t' + str(txt.sentiment.polarity)
#print aspects_dict.keys()
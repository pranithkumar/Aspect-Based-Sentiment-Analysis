import pandas
import nltk
from nltk.tokenize import word_tokenize

#amazontext = pandas.read_json("~/Documents/Amazon_reviews_only.json")
amazontext = pandas.read_json("apple-iphone-6-space-grey-32-gb.json")
def find_sub_list(sl,l):
	result = []
	sll=len(sl)
	for ind in (i for i,e in enumerate(l) if e==sl[0]):
		if l[ind:ind+sll]==sl:
			result.append((ind,ind+sll-1))
	return result

patterns = [['JJ','NN','NN'],['JJ','NN','NNS'],['JJ','NNS','NN'],['JJ','NNS','NNS'],['RB','JJ','NN'],['RBR','JJ','NN'],['RBS','JJ','NN'],['RB','JJ','NNS'],['RBR','JJ','NNS'],['RBS','JJ','NNS'],['RB','RB','NN'],['RBR','RB','NN'],['RBS','RB','NN'],['RB','RB','NNS'],['RBR','RB','NNS'],['RBS','RB','NNS'],['RB','RBR','NN'],['RBR','RBR','NN'],['RBS','RBR','NN'],['RB','RBR','NNS'],['RBR','RBR','NNS'],['RBS','RBR','NNS'],['RB','RBS','NN'],['RBR','RBS','NN'],['RBS','RBS','NN'],['RB','RBS','NNS'],['RBR','RBS','NNS'],['RBS','RBS','NNS'],['JJ','NN'],['JJ','NNS'],['RB','JJ'],['RBR','JJ'],['RBS','JJ'],['RB','VBN'],['RBR','VBN'],['RBS','VBN'],['RB','VBD'],['RBR','VBD'],['RBS','VBD'],['VBN','NN'],['VBN','NNS'],['VBD','NN'],['VBD','NNS'],['VBN','RB'],['VBN','RBR'],['VBN','RBS'],['VBD','RB'],['VBD','RBR'],['VBD','RBS']]
'''
for review in amazontext['review']:
	print "\n"+review
	word_tokens = word_tokenize(review)
	pos_tuples = nltk.pos_tag(word_tokens)
	#print pos_tuples
	pos =[]
	for tag in pos_tuples:
		pos.append(tag[1])
	for pattern in patterns:
		if find_sub_list(pattern,pos) != None:
			parts = find_sub_list(pattern,pos)
			for indices in parts:
				#indices = find_sub_list(pattern,pos)
				print pattern
				#print indices
				for i in range(int(indices[0]),int(indices[1])+1):
					print pos_tuples[i]
'''
for review in amazontext['review']:
	print "\n"+review
	lines = []
	lines = review.split('.')
	for line in lines:
		word_tokens = word_tokenize(line)
		pos_tuples = nltk.pos_tag(word_tokens)
		print pos_tuples
		pos =[]
		for tag in pos_tuples:
			pos.append(tag[1])
		for pattern in patterns:
			if find_sub_list(pattern,pos) != None:
				parts = find_sub_list(pattern,pos)
				for indices in parts:
					#indices = find_sub_list(pattern,pos)
					print pattern
					#print indices
					for i in range(int(indices[0]),int(indices[1])+1):
						print pos_tuples[i]
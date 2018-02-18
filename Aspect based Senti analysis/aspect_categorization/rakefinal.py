import nltk
from nltk.tokenize import word_tokenize

'''def sublist(lst1, lst2):
	pos = []
	tokens = []
	for tag in lst2:
		pos.append(tag[1])
		tokens.append(tag[0])
	ls1 = [element for element in lst1 if element in pos]
	ls2 = [element for element in pos if element in lst1]
	if ls1 == ls2:
		return ls2
	else:
		return 0'''

def find_sub_list(sl,l):
	result = []
	sll=len(sl)
	for ind in (i for i,e in enumerate(l) if e==sl[0]):
		if l[ind:ind+sll]==sl:
			result.append((ind,ind+sll-1))
	return result

f = open("testtext.txt","r")

patterns = [['JJ','NN','NN'],['JJ','NN','NNS'],['JJ','NNS','NN'],['JJ','NNS','NNS'],['RB','JJ','NN'],['RBR','JJ','NN'],['RBS','JJ','NN'],['RB','JJ','NNS'],['RBR','JJ','NNS'],['RBS','JJ','NNS'],['RB','RB','NN'],['RBR','RB','NN'],['RBS','RB','NN'],['RB','RB','NNS'],['RBR','RB','NNS'],['RBS','RB','NNS'],['RB','RBR','NN'],['RBR','RBR','NN'],['RBS','RBR','NN'],['RB','RBR','NNS'],['RBR','RBR','NNS'],['RBS','RBR','NNS'],['RB','RBS','NN'],['RBR','RBS','NN'],['RBS','RBS','NN'],['RB','RBS','NNS'],['RBR','RBS','NNS'],['RBS','RBS','NNS'],['JJ','NN'],['JJ','NNS'],['RB','JJ'],['RBR','JJ'],['RBS','JJ'],['RB','VBN'],['RBR','VBN'],['RBS','VBN'],['RB','VBD'],['RBR','VBD'],['RBS','VBD'],['VBN','NN'],['VBN','NNS'],['VBD','NN'],['VBD','NNS'],['VBN','RB'],['VBN','RBR'],['VBN','RBS'],['VBD','RB'],['VBD','RBR'],['VBD','RBS']]

for review in f.readlines():
	print "\n"+review
	lines = []
	lines = review.split('.')
	for line in lines:
		word_tokens = word_tokenize(line)
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
	'''for pattern in patterns:
		if sublist(pattern,pos_tuples) != 0:
			print sublist(pattern,pos_tuples)'''
	#print pos
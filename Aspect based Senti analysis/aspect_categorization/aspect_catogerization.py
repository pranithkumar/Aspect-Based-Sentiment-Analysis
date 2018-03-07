import nltk,pandas,pprint,re
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

#amazontext = pandas.read_json("~/Documents/Amazon_reviews_only.json")
amazontext = pandas.read_json("apple-iphone-6-space-grey-32-gb.json")
def find_sub_list(sl,l):
	result = []
	sll=len(sl)
	for ind in (i for i,e in enumerate(l) if e==sl[0]):
		if l[ind:ind+sll]==sl:
			result.append((ind,ind+sll-1))
	return result

patterns1 = [['NN','NN','VBN','JJ'],['NN','NNS','VBN','JJ'],['NNS','NN','VBN','JJ'],['NNS','NNS','VBN','JJ'],['NN','NN','VBD','JJ'],['NN','NNS','VBD','JJ'],['NNS','NN','VBD','JJ'],['NNS','NNS','VBD','JJ'],['JJ','NN','NN'],['JJ','NN','NNS'],['JJ','NNS','NN'],['JJ','NNS','NNS'],['RB','JJ','NN'],['RBR','JJ','NN'],['RBS','JJ','NN'],['RB','JJ','NNS'],['RBR','JJ','NNS'],['RBS','JJ','NNS'],['RB','RB','NN'],['RBR','RB','NN'],['RBS','RB','NN'],['RB','RB','NNS'],['RBR','RB','NNS'],['RBS','RB','NNS'],['RB','RBR','NN'],['RBR','RBR','NN'],['RBS','RBR','NN'],['RB','RBR','NNS'],['RBR','RBR','NNS'],['RBS','RBR','NNS'],['RB','RBS','NN'],['RBR','RBS','NN'],['RBS','RBS','NN'],['RB','RBS','NNS'],['RBR','RBS','NNS'],['RBS','RBS','NNS'],['NN','VBZ','JJ'],['NNP','NN'],['JJ','NN'],['JJ','NNS'],['VBN','NN'],['VBN','NNS'],['VBD','NN'],['VBD','NNS']]

patterns2 = [['RB','JJ'],['RBR','JJ'],['RBS','JJ'],['RB','VBN'],['RBR','VBN'],['RBS','VBN'],['RB','VBD'],['RBR','VBD'],['RBS','VBD'],['VBN','RB'],['VBN','RBR'],['VBN','RBS'],['VBD','RB'],['VBD','RBR'],['VBD','RBS']]

aspects_dict = {}
stop_words = set(stopwords.words('english'))

for review in amazontext['review']:
	review = review.lower()
	res = ' '
	for ch in review:
		if not re.match('[a-zA-Z0-9_ ]',ch):
			res = res + ' ' + ch + ' '
		else:
			res = res + ch
	review = res[1:]
	nounlist = ['NN','NNS']
	#aspects_dict = {}
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
						if pos_tuples[i][1] in nounlist:
							aspect = aspect + ' ' + pos_tuples[i][0]
						else:
							if pos_tuples[i][0] not in stop_words:
								entity = entity + ' ' + pos_tuples[i][0]
						print pos_tuples[i]
					if aspect[2:] in aspects_dict:
						if entity[2:] in aspects_dict[aspect[2:]]:
							aspects_dict[aspect[2:]][entity[2:]] += 1
						else:
							aspects_dict[aspect[2:]][entity[2:]] = 1
					else:
						aspects_dict[aspect[2:]] = {}
						aspects_dict[aspect[2:]][entity[2:]] = 1
		
		for pattern in patterns2:
			if find_sub_list(pattern,pos) != None:
				parts = find_sub_list(pattern,pos)
				check_noun = {}
				for indices in parts:
					i = 0
					for tag in pos_tuples:
						if tag[1] in nounlist:
							if i < parts[0][0]:
								check_noun[i] = parts[0][0] - i
							elif i > parts[0][1]:
								check_noun[i] = i - parts[0][1]
						i = i+1
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
					if check_noun:
						aspect = aspect + ' ' + pos_tuples[noun_index[0]][0]
					for i in range(int(indices[0]),int(indices[1])+1):
						if pos_tuples[i][0] not in stop_words:
							entity = entity + ' ' + pos_tuples[i][0]
						print pos_tuples[i]
					if aspect[2:] in aspects_dict:
						if entity[2:] in aspects_dict[aspect[2:]]:
							aspects_dict[aspect[2:]][entity[2:]] += 1
						else:
							aspects_dict[aspect[2:]][entity[2:]] = 1
					else:
						aspects_dict[aspect[2:]] = {}
						aspects_dict[aspect[2:]][entity[2:]] = 1

#pprint.pprint(aspects_dict)
for k in sorted(aspects_dict, key=lambda k: len(aspects_dict[k]), reverse=True):
	sot_list = sorted(aspects_dict[k], key=lambda ke: aspects_dict[k][ke], reverse = True)
	for i in sot_list:
		if aspects_dict[k][i] > 1:
			print 'aspect: '+ k + ', entity:' + i + ', count: ' + str(aspects_dict[k][i])

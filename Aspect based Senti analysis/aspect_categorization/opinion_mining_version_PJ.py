import datapreprocessing as dp
from extract_aspects import *
import re, pprint

def find_sub_list(sl,l):
	result = []
	sll=len(sl)
	for ind in (i for i,e in enumerate(l) if e==sl[0]):
		if l[ind:ind+sll]==sl:
			result.append((ind,ind+sll-1))
	return result


#EDit this function
def patterns(pos_tuples):
	patterns = [['JJ','NN','NN'],['JJ','NN','NNS'],['JJ','NNS','NN'],['JJ','NNS','NNS'],['RB','JJ','NN'],['RBR','JJ','NN'],['RBS','JJ','NN'],['RB','JJ','NNS'],['RBR','JJ','NNS'],['RBS','JJ','NNS'],['RB','RB','NN'],['RBR','RB','NN'],['RBS','RB','NN'],['RB','RB','NNS'],['RBR','RB','NNS'],['RBS','RB','NNS'],['RB','RBR','NN'],['RBR','RBR','NN'],['RBS','RBR','NN'],['RB','RBR','NNS'],['RBR','RBR','NNS'],['RBS','RBR','NNS'],['RB','RBS','NN'],['RBR','RBS','NN'],['RBS','RBS','NN'],['RB','RBS','NNS'],['RBR','RBS','NNS'],['RBS','RBS','NNS'],['JJ','NN'],['JJ','NNS'],['RB','JJ'],['RBR','JJ'],['RBS','JJ'],['RB','VBN'],['RBR','VBN'],['RBS','VBN'],['RB','VBD'],['RBR','VBD'],['RBS','VBD'],['VBN','NN'],['VBN','NNS'],['VBD','NN'],['VBD','NNS'],['VBN','RB'],['VBN','RBR'],['VBN','RBS'],['VBD','RB'],['VBD','RBR'],['VBD','RBS']]
	pos =[]
	pattern_snips = []
	for tag in pos_tuples:
		pos.append(tag[1])
		for pattern in patterns:
			if find_sub_list(pattern,pos) != None:
				parts = find_sub_list(pattern,pos)
				for indices in parts:
					#indices = find_sub_list(pattern,pos)
					print pattern
					#print indices
					
					#for i in range(int(indices[0]),int(indices[1])+1):
					#	print pos_tuples[i][0].encode('utf-8')
 					pattern_text = ' '.join(pos_tuples[i][0].encode('utf-8') for i in range(int(indices[0]),int(indices[1])+1))
 					#pattern_text = ' '.join(e.encode('utf-8') for e in pos_tuples[int(indices[0]): int(indices[1])+1][1])
 					pattern_snips.append(pattern_text)
 					print pattern_text
 	return pattern_snips

#main code

reviews = dp.dataframecomplete('Apple-iPhone-Space-Grey-32GB.json','apple-iphone-6-space-grey-32-gb.json')
aspects_dict = {}
aspects_top = []
ae_pairs = {}
for review in reviews['review']:
	res = ' '
	for ch in review:
		if not re.match('[a-zA-Z0-9_\' ]',ch):
			res = res + ' ' + ch + ' '
		else:
			res = res + ch
	review = res[1:]
	
	print "\n\n\nreview: " + review
	
	tokenized_data = tokenize(review.encode('utf-8'))
	pos_tagged_data = pos_tag(tokenized_data)
	print "pos tag: " 
	print pos_tagged_data

	pat = patterns(pos_tagged_data)

	final_aspects = []
	final_entities = []
	print "aspects :"
	aspects_data = aspects_from_tagged_sents(pos_tagged_data)
	entity_data = entities_from_tagged_sents(pos_tagged_data)
	for asp in aspects_data:
		if re.match('[a-zA-Z0-9_\' -!=:?;@]',asp):
			final_aspects.append(asp)
			if asp.encode('utf-8') in aspects_dict:
				aspects_dict[asp] += 1
			else:
				aspects_dict[asp] = 1
	print final_aspects
	print "entities :"
	for ent in entity_data:
		if re.match('[a-zA-Z0-9_\' -!=:?;@]',ent):
			final_entities.append(ent)
	print final_entities

i = 0
#pprint.pprint(aspects_dict)
for k in sorted(aspects_dict.items(), key=lambda x:x[1], reverse=True):
	print k[0].encode('utf-8') + ' ' + str(k[1])
	if i<15:
		aspects_top.append(k[0].encode('utf-8'))
		i = i+1

#print aspects_top

# mining entities from aspects
aspects_dict = {a:[] for a in aspects_top}

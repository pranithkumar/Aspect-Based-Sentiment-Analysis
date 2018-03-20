import nltk,re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

def find_sub_list(sl,l):
	result = []
	sll=len(sl)
	for ind in (i for i,e in enumerate(l) if e==sl[0]):
		if l[ind:ind+sll]==sl:
			result.append((ind,ind+sll-1))
	return result

sentences = 'the battery backup of the mobile is very good /u444/1222 /'

word_tokens = word_tokenize(sentences)
tagged_sentences = nltk.pos_tag(word_tokens)
STOPWORDS = set(stopwords.words('english'))
print tagged_sentences

asp_ent_pair = {}
noun_sets = [['NN','NN'],['NNP','NNP'],['NNS','NNS'],['NN','NNP'],['NN','NNS'],['NNP','NN'],['NNP','NNS'],['NNS','NN'],['NNS','NNP']]
c = 0
temp = []
for i in range(0,len(tagged_sentences)):
	temp.append(i)

print temp

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

print temp
print res

tags_list = []
word_list = []
for sent in tagged_sentences:
	word_list.append(sent[0])
	tags_list.append(sent[1])

for noun in noun_sets:
	if find_sub_list(noun,tags_list) != []:
		print noun
		parts = find_sub_list(noun,tags_list)
		print parts[0]
		asp = ' '

		for index in range(int(parts[0][0]),int(parts[0][1])+1):
			if tagged_sentences[index][0] not in STOPWORDS:
				if re.match('[a-zA-Z0-9]',tagged_sentences[index][0]):
					temp[index] = -1
					asp += ' ' + tagged_sentences[index][0]

		print "aspect:" + asp[2:]
		asp_ent_pair[asp[2:]] = {}
		c = 1

print temp
count = 0
for sent in tagged_sentences:
	if re.match('[a-zA-Z0-9_]',sent[0]):
		if sent[1]=='NNP' or sent[1]=='NN' or sent[1]=='NNS':
			if(sent[0] not in STOPWORDS) and (temp[count] != -1):
				print "aspect:"+sent[0]
				asp_ent_pair[sent[0]] = {}
				c = 1
	count += 1

for sent in tagged_sentences:
	if re.match('[a-zA-Z0-9_]',sent[0]):
		if c == 0:
			break
		if sent[1] in ['JJ','RB','RBR','RBS','VBN','VBD','VBP']:
				if sent[0] not in STOPWORDS:
					print "entity: " + sent[0]
					for asp in asp_ent_pair:
						asp_ent_pair[asp][sent[0]] = 1

print asp_ent_pair
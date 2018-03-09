from nltk.corpus import wordnet

#list1 = ['Compare', 'require']
#list2 = ['choose', 'copy', 'define', 'duplicate', 'find', 'how', 'identify', 'label', 'list', 'listen', 'locate', 'match', 'memorise', 'name', 'observe', 'omit', 'quote', 'read', 'recall', 'recite', 'recognise', 'record', 'relate', 'remember', 'repeat', 'reproduce', 'retell', 'select', 'show', 'spell', 'state', 'tell', 'trace', 'write']
list = []
list1 = ['quality']
list2 = ['quality_earphones','quality_camera']

i=0
for word1 in list1:
	print i;j=0
	for word2 in list2:
		print j
		wordFromList1 = wordnet.synsets(word1)
		print wordFromList1
		wordFromList2 = wordnet.synsets(word2)
		print wordFromList2
		if wordFromList1 and wordFromList2:
			s = wordFromList1[0].wup_similarity(wordFromList2[0])
			list.append(s)
		print list
		j += 1
	i += 1

print(list)
from nltk.corpus import stopwords

STOPWORDS = set(stopwords.words('english'))
f=open('new_stopwords','r')
NEWSTOPWORDS = f.read().split('\n')
temp = []
for word in NEWSTOPWORDS:
	temp.append(word.decode('ascii'))
NEWSTOPWORDS = temp
STOPWORDS = STOPWORDS|set(NEWSTOPWORDS)
print STOPWORDS
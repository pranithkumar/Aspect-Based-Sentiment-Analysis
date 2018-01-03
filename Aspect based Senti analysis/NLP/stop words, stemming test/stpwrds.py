from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
 
data = "I have been told by Flipkart that they cant be bothered, as Xiaomi is at fault. Its really a sad situation to be in."
stopWords = set(stopwords.words('english'))
#print len(stopWords)
#print stopWords

words = word_tokenize(data)
wordsFiltered = []
for w in words:
    if w not in stopWords:
        wordsFiltered.append(w)
 
print(wordsFiltered)

ps = PorterStemmer()
for w in wordsFiltered:
	print(ps.stem(w))
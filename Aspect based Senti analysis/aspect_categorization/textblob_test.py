from textblob import TextBlob
from textblob.classifiers import NaiveBayesClassifier

'''
train = [
	('I love this sandwich.', 'pos'),
	('this is an amazing place!', 'pos'),
	('I feel very good about these beers.', 'pos'),
	('this is my best work.', 'pos'),
	("what an awesome view", 'pos'),
	('I do not like this restaurant', 'neg'),
	('I am tired of this stuff.', 'neg'),
	("I can't deal with this", 'neg'),
	('he is my sworn enemy!', 'neg'),
	('my boss is horrible.', 'neg')
	]
'''

text = "i love the camera but baterry is bad"
blob = TextBlob(text)
print blob.tags
print blob.noun_phrases

for sent in blob.sentences:
	print sent.sentiment.polarity

#cl = NaiveBayesClassifier(train)
print cl.classify(text)

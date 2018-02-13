import RAKE
import pandas
from nltk.corpus import stopwords
from textblob import TextBlob
from textblob.classifiers import NaiveBayesClassifier

stop_words = stopwords.words('english')
#r= RAKE.Rake(stop_words)
r= RAKE.Rake(RAKE.SmartStopList())
#print stpwords
text = "Although honor 8 is a bit old now its checks all the boxes. You won't be getting a 18:9 display and latest android but the device is fast and responsive. Kirin 950 is still a great performer compared to the budget chips. I really like the glass back of this phone and fingerprint reader is fast and responsive. Camera is great, it has a usb type-c port, the screen is also gorgeous for a 1080p display with nice viewing angles and sunlight readability.   It might not make sense to buy a phone with big bezels and older android versions right now but if you look past them honor 8 is a superb phone."
print r.run(text)
print "\n\n\n\n"
blob = TextBlob(text)
print blob.tags

#mytext= "The camera quality of this iphone is good.The meal was delicious but not as good as butter."

amazontext = pandas.read_json("~/Documents/Amazon_reviews_only.json")



#print amazontext['reviewText']

i = 0
"""for text in amazontext['reviewText']:
	if i== 10:
		break
	print i
	print text
	print r.run(text)
	#print r.extract_keywords_from_text(str(text))
	#print r.get_ranked_phrases()
	i = i + 1"""

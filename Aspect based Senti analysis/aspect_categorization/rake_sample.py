import nltk
from rake_nltk import Rake
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import dataframe as dp
from textblob import TextBlob

r = Rake()
#df = dp.dataframecomplete('data/Apple-iPhone-Space-Grey-32GB.json','data/apple-iphone-6-space-grey-32-gb.json')
df = dp.read_amazondata()
count = 0
for review in df['reviewText']:
    if count == 50:
        break
    words = []
    review = review.lower()
    r.extract_keywords_from_text(review)
    print "\n\n" + review
    raked = r.get_ranked_phrases()
    for rak in raked:
        words.append(rak.encode("utf-8"))
    print words
    for stat in words:
        if(len(stat.split(' ')) > 1):
            txt = TextBlob(stat)
            print txt.tags
            for sent in txt.sentences:
                print sent.sentiment.polarity
    count = count + 1

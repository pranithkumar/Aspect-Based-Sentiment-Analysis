from rake_nltk import Rake
r= Rake()
mytext= "The camera quality of this iphone is good.The meal was delicious but not as good as butter."
print r.extract_keywords_from_text(mytext)
print r.get_ranked_phrases()

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer, WordNetLemmatizer

example_sent = "This is a sample sentence, showing off the stop words filtration."
stop_words = set(stopwords.words('english'))
word_tokens = word_tokenize(example_sent)
filtered_sentence = [w for w in word_tokens if not w in stop_words]
filtered_sentence = []
for w in word_tokens:
    if w not in stop_words:
        filtered_sentence.append(w)

print(word_tokens)
print(filtered_sentence)

stemmer = PorterStemmer()
lemmatizer = WordNetLemmatizer()

for sentence in filtered_sentence:
	print("Stem %s: %s" % (sentence,stemmer.stem(sentence)))

for sentence in filtered_sentence:
    print("lemma %s: %s" % (sentence,lemmatizer.lemmatize(sentence, pos='v')))

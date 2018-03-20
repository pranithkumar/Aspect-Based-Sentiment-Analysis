import nltk,re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from final_aspect_entity_extraction import *

sentences = 'the battery backup of the mobile is very good /u444/1222 /'

word_tokens = word_tokenize(sentences)
tagged_sentences = nltk.pos_tag(word_tokens)
print aspects_from_tagged_sents(tagged_sentences)
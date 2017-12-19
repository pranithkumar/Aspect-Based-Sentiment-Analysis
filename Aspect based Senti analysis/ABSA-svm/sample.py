import pandas as pd
from sklearn.externals import joblib
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction import DictVectorizer
from sklearn.linear_model import SGDClassifier
from sklearn.multiclass import OneVsRestClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn import svm
import xml.etree.ElementTree as ET
from lxml import etree
from scipy.sparse import hstack
import numpy as np
import warnings


path_train = r'data/ABSA16_Laptops_Train_English_SB2.xml'
path_test = r'data/EN_LAPT_SB2_TEST.xml'

#For stanford POS Tagger

from nltk.tag.stanford import CoreNLPPOSTagger as POS_Tag
from nltk import word_tokenize
_path_to_model = 'stanford-postagger/models/english-bidirectional-distsim.tagger' 
_path_to_jar = 'stanford-postagger/stanford-postagger.jar'
stanford_tag = POS_Tag(_path_to_model, _path_to_jar)

#xml parser
def get_list(path):
    tree=ET.parse(path)
    root = tree.getroot()
    text_list = []
    opinion_list = []
    for review in root.findall('Review'):
        text_string=""
        opinion_inner_list=[]
        for sent in review.findall('./sentences/sentence'):
            text_string= text_string+ " "+ sent.find('text').text
        text_list.append(text_string)
        for opinion in review.findall('./Opinions/Opinion'):
            opinion_dict = {
                opinion.get('category').replace('#','_'): opinion.get('polarity')
            }
            opinion_inner_list.append(opinion_dict)
        opinion_list.append(opinion_inner_list)
    return text_list,opinion_list

#Selecting only 20 most common aspect.
def get_most_common_aspect(opinion_list):
    import nltk
    opinion= []
    for inner_list in opinion_list:
        for _dict in inner_list:
            for key in _dict:
                opinion.append(key)
    most_common_aspect = [k for k,v in nltk.FreqDist(opinion).most_common(20)]
    return most_common_aspect



#generate data frame
def get_data_frame(text_list,opinion_list,most_common_aspect):
    data={'Review':text_list}
    df = pd.DataFrame(data)
    if opinion_list:
        for inner_list in opinion_list:
            for _dict in inner_list:
                for key in _dict:
                    if key in most_common_aspect:
                        df.loc[opinion_list.index(inner_list),key]=_dict[key]
    return df




#generate data frame for aspect extraction task
def get_aspect_data_frame(df,most_common_aspect):
    for common_aspect in most_common_aspect:
        df[common_aspect]=df[common_aspect].replace(['positive','negative','neutral','conflict'],[1,1,1,1])
    df = df.fillna(0)
    return df


def get_positive_data_frame(df,most_common_aspect):
    for common_aspect in most_common_aspect:
        df[common_aspect]=df[common_aspect].replace(['positive'],[1])
        df[common_aspect]=df[common_aspect].replace(['negative','neutral','conflict'],[0,0,0])
    df = df.fillna(0)
    return df


def get_negative_data_frame(df,most_common_aspect):
    for common_aspect in most_common_aspect:
        df[common_aspect]=df[common_aspect].replace(['negative'],[1])
        df[common_aspect]=df[common_aspect].replace(['positive','neutral','conflict'],[0,0,0])
    df = df.fillna(0)
    return df


def get_neutral_data_frame(df,most_common_aspect):
    for common_aspect in most_common_aspect:
        df[common_aspect]=df[common_aspect].replace(['neutral','conflict'],[1,1])
        df[common_aspect]=df[common_aspect].replace(['negative','positive'],[0,0])
    df = df.fillna(0)
    return df


#To tag using stanford pos tagger
def posTag(review):
    tagged_text_list=[]
    for text in review:
        tagged_text_list.append(stanford_tag.tag(word_tokenize(text)))
    return tagged_text_list
#posTag("this is random text")


#Filter the word with tag- noun,adjective,verb,adverb
def filterTag(tagged_review):
    final_text_list=[]
    for text_list in tagged_review:
        final_text=[]
        for word,tag in text_list:
            if tag in ['NN','NNS','NNP','NNPS','RB','RBR','RBS','JJ','JJR','JJS','VB','VBD','VBG','VBN','VBP','VBZ']:
                final_text.append(word)
        final_text_list.append(' '.join(final_text))
    return final_text_list


def get_dict_aspect(y,most_common_aspect):
    position=[]
    for innerlist in y:
        position.append([i for i, j in enumerate(innerlist) if j == 1])
    sorted_common=sorted(most_common_aspect)
    dict_aspect=[]
    for innerlist in position:
        inner_dict={}
        for word in sorted_common:
            if sorted_common.index(word) in innerlist:
                inner_dict[word]= 5
            else:
                inner_dict[word]=0
        dict_aspect.append(inner_dict)
    return dict_aspect


#Stage 1:
#Making list to train
train_text_list,train_opinion_list = get_list(path_train)
most_common_aspect = get_most_common_aspect(train_opinion_list)


#This takes time to tag. Already tagged and saved. So, loading file ...
#tagged_text_list_train=posTag(train_text_list)
#joblib.dump(tagged_text_list_train, 'tagged_text_list_train.pkl')
tagged_text_list_train=joblib.load('tagged_text_list_train.pkl')


#train list after filter
final_train_text_list=filterTag(tagged_text_list_train)


#get data frame
df_train = get_data_frame(final_train_text_list,train_opinion_list,most_common_aspect)
df_train_aspect = get_aspect_data_frame(df_train,most_common_aspect)
df_train_aspect = df_train_aspect.reindex(sorted(df_train_aspect.columns), axis=1)


#Similar for test list
test_text_list,test_opinion_list = get_list(path_test)


#tagged_text_list_test=posTag(test_text_list)
#joblib.dump(tagged_text_list_test, 'tagged_text_list_test.pkl')
tagged_text_list_test=joblib.load('tagged_text_list_test.pkl')


final_test_text_list=filterTag(tagged_text_list_test)


df_test = get_data_frame(final_test_text_list,test_opinion_list,most_common_aspect)
df_test_aspect = get_aspect_data_frame(df_test,most_common_aspect)
df_test_aspect = df_test_aspect.reindex(sorted(df_test_aspect.columns), axis=1)


#Sort the data frame according to aspect's name and separate data(X) and target(y)
#df_train_aspect = df_train_aspect.sample(frac=1).reset_index(drop=True) #For randoming
X_train= df_train_aspect.Review
y_train = df_train_aspect.drop('Review',1)

#df_test_aspect = df_test_aspect.sample(frac=1).reset_index(drop=True) #For randoming
X_test = df_test_aspect.Review
y_test = df_test_aspect.drop('Review',1)


#Change y_train to numpy array
import numpy as np
#y_train = np.asarray(y_train, dtype=np.int64)
#y_test = np.asarray(y_test, dtype=np.int64)
print('train\n')
print(y_train)
print('\ntest\n')
print(y_test)
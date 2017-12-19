
# coding: utf-8

# In[1]:


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
#home =
from nltk.tag.stanford import CoreNLPPOSTagger as POS_Tag
from nltk import word_tokenize
_path_to_model = 'stanford-postagger/models/english-bidirectional-distsim.tagger' 
_path_to_jar = 'stanford-postagger/stanford-postagger.jar'
stanford_tag = POS_Tag(_path_to_model, _path_to_jar)


# In[2]:


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


# In[3]:


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


# In[4]:


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


# In[5]:


#generate data frame for aspect extraction task
def get_aspect_data_frame(df,most_common_aspect):
    for common_aspect in most_common_aspect:
        df[common_aspect]=df[common_aspect].replace(['positive','negative','neutral','conflict'],[1,1,1,1])
    df = df.fillna(0)
    return df


# In[6]:


def get_positive_data_frame(df,most_common_aspect):
    for common_aspect in most_common_aspect:
        df[common_aspect]=df[common_aspect].replace(['positive'],[1])
        df[common_aspect]=df[common_aspect].replace(['negative','neutral','conflict'],[0,0,0])
    df = df.fillna(0)
    return df


# In[7]:


def get_negative_data_frame(df,most_common_aspect):
    for common_aspect in most_common_aspect:
        df[common_aspect]=df[common_aspect].replace(['negative'],[1])
        df[common_aspect]=df[common_aspect].replace(['positive','neutral','conflict'],[0,0,0])
    df = df.fillna(0)
    return df


# In[8]:


def get_neutral_data_frame(df,most_common_aspect):
    for common_aspect in most_common_aspect:
        df[common_aspect]=df[common_aspect].replace(['neutral','conflict'],[1,1])
        df[common_aspect]=df[common_aspect].replace(['negative','positive'],[0,0])
    df = df.fillna(0)
    return df


# In[9]:


#To tag using stanford pos tagger
def posTag(review):
    tagged_text_list=[]
    for text in review:
        tagged_text_list.append(stanford_tag.tag(word_tokenize(text)))
    return tagged_text_list
#posTag("this is random text")


# In[10]:


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


# In[11]:


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


# In[12]:


#Stage 1:
#Making list to train
train_text_list,train_opinion_list = get_list(path_train)
most_common_aspect = get_most_common_aspect(train_opinion_list)


# In[13]:


#This takes time to tag. Already tagged and saved. So, loading file ...
#tagged_text_list_train=posTag(train_text_list)
#joblib.dump(tagged_text_list_train, 'tagged_text_list_train.pkl')
tagged_text_list_train=joblib.load("tagged_text_list_train.pkl")


# In[14]:


#train list after filter
final_train_text_list=filterTag(tagged_text_list_train)


# In[15]:


#get data frame
df_train = get_data_frame(final_train_text_list,train_opinion_list,most_common_aspect)
df_train_aspect = get_aspect_data_frame(df_train,most_common_aspect)
df_train_aspect = df_train_aspect.reindex(sorted(df_train_aspect.columns), axis=1)


# In[16]:


#Similar for test list
test_text_list,test_opinion_list = get_list(path_test)


# In[17]:


#tagged_text_list_test=posTag(test_text_list)
#joblib.dump(tagged_text_list_test, 'tagged_text_list_test.pkl')
tagged_text_list_test=joblib.load("tagged_text_list_test.pkl")


# In[18]:


final_test_text_list=filterTag(tagged_text_list_test)


# In[19]:


df_test = get_data_frame(final_test_text_list,test_opinion_list,most_common_aspect)
df_test_aspect = get_aspect_data_frame(df_test,most_common_aspect)
df_test_aspect = df_test_aspect.reindex(sorted(df_test_aspect.columns), axis=1)


# In[20]:


#Sort the data frame according to aspect's name and separate data(X) and target(y)
#df_train_aspect = df_train_aspect.sample(frac=1).reset_index(drop=True) #For randoming
X_train= df_train_aspect.Review
y_train = df_train_aspect.drop('Review',1)

#df_test_aspect = df_test_aspect.sample(frac=1).reset_index(drop=True) #For randoming
X_test = df_test_aspect.Review
y_test = df_test_aspect.drop('Review',1)


# In[21]:


#Change y_train to numpy array
import numpy as np
y_train = np.asarray(y_train, dtype=np.int64)
y_test = np.asarray(y_test, dtype=np.int64)


# In[22]:


#Generate word vecotors using CountVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from nltk import word_tokenize          
from nltk.stem import WordNetLemmatizer 
vect = CountVectorizer(max_df=1.0,stop_words='english')  
X_train_dtm = vect.fit_transform(X_train)
X_test_dtm = vect.transform(X_test)


# In[23]:


#Create various models. These are multi-label models.
nb_classif = OneVsRestClassifier(MultinomialNB()).fit(X_train_dtm, y_train)
C = 1.0 #SVregularization parameter
svc = OneVsRestClassifier(svm.SVC(kernel='linear', C=C)).fit(X_train_dtm, y_train)
lin_svc = OneVsRestClassifier(svm.LinearSVC(C=C)).fit(X_train_dtm, y_train)
sgd = OneVsRestClassifier(SGDClassifier()).fit(X_train_dtm,y_train)


# In[24]:


#Predict the test data using classifiers
y_pred_class = nb_classif.predict(X_test_dtm)
y_pred_class_svc = svc.predict(X_test_dtm)
y_pred_class_lin_svc = lin_svc.predict(X_test_dtm)
y_pred_class_sgd = sgd.predict(X_test_dtm)


# In[25]:


#Following code to test metrics of all aspect extraction classifiers
from sklearn import metrics


# In[26]:


print(metrics.accuracy_score(y_test,y_pred_class))
print(metrics.accuracy_score(y_test,y_pred_class_svc))
print(metrics.accuracy_score(y_test,y_pred_class_lin_svc))
print(metrics.accuracy_score(y_test,y_pred_class_sgd))


# In[27]:


print(metrics.precision_score(y_test,y_pred_class,average='micro'))
print(metrics.precision_score(y_test,y_pred_class_svc,average='micro'))
print(metrics.precision_score(y_test,y_pred_class_lin_svc,average='micro'))
print(metrics.precision_score(y_test,y_pred_class_sgd,average='micro'))


# In[28]:


print(metrics.recall_score(y_test,y_pred_class,average='micro'))
print(metrics.recall_score(y_test,y_pred_class_svc,average='micro'))
print(metrics.recall_score(y_test,y_pred_class_lin_svc,average='micro'))
print(metrics.recall_score(y_test,y_pred_class_sgd,average='micro'))


# In[29]:


print(metrics.f1_score(y_test,y_pred_class,average='micro'))
print(metrics.f1_score(y_test,y_pred_class_svc,average='micro'))
print(metrics.f1_score(y_test,y_pred_class_lin_svc,average='micro'))
print(metrics.f1_score(y_test,y_pred_class_sgd,average='micro'))


# In[30]:


with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    print(metrics.classification_report(y_test, y_pred_class))
    print(metrics.classification_report(y_test, y_pred_class_svc))
    print(metrics.classification_report(y_test, y_pred_class_lin_svc))
    print(metrics.classification_report(y_test, y_pred_class_sgd))


# In[31]:


#Stage 2:
#Generating extra feature that indicates which aspect category is present in the review
train_dict_aspect=get_dict_aspect(y_train, most_common_aspect)
d_train=DictVectorizer() 
X_train_aspect_dtm = d_train.fit_transform(train_dict_aspect)

#y_test is used to generated extra feature in order to test the performance of 2nd classifer.
#Use y_pred_class_svc(Highest performer for aspect classification) as input for extra feature to test the overall performace.
test_dict_aspect=get_dict_aspect(y_test,most_common_aspect)
d_test=DictVectorizer() 
X_test_aspect_dtm = d_test.fit_transform(test_dict_aspect)


# In[32]:


#Function for classiflying positive,negative or neutral sentiment of all the aspects
def classify_sentiment(df_train,df_test,X_train_aspect_dtm,X_test_aspect_dtm):
    
    df_train = df_train.reindex_axis(sorted(df_train_positive.columns), axis=1)
    df_test = df_test.reindex_axis(sorted(df_test_positive.columns), axis=1)

    import numpy as np
    X_train = df_train.Review
    y_train = df_train.drop('Review',1)
    y_train = np.asarray(y_train, dtype=np.int64)

    X_test = df_test.Review
    y_test = df_test.drop('Review',1)
    y_test = np.asarray(y_test, dtype=np.int64)

    vect_sen = CountVectorizer(stop_words='english',ngram_range=(1,2))  
    X_train_dtm = vect_sen.fit_transform(X_train)
    X_test_dtm = vect_sen.transform(X_test)

    #ombining word vector with extra feature.
    from scipy.sparse import hstack
    X_train_dtm=hstack((X_train_dtm, X_train_aspect_dtm))
    X_test_dtm=hstack((X_test_dtm, X_test_aspect_dtm))

    C = 1.0 #SVregularization parameter
    nb_classif = OneVsRestClassifier(MultinomialNB()).fit(X_train_dtm, y_train)
    svc = OneVsRestClassifier(svm.SVC(kernel='linear', C=C)).fit(X_train_dtm, y_train)
    lin_svc = OneVsRestClassifier(svm.LinearSVC(C=C)).fit(X_train_dtm, y_train)
    sgd = OneVsRestClassifier(SGDClassifier()).fit(X_train_dtm,y_train)

    y_pred_class= nb_classif.predict(X_test_dtm)
    y_pred_class_svc = svc.predict(X_test_dtm)
    y_pred_class_lin_svc = lin_svc.predict(X_test_dtm)
    y_pred_class_sgd = sgd.predict(X_test_dtm)
    return (y_test,y_pred_class,y_pred_class_svc,y_pred_class_lin_svc,y_pred_class_sgd)


# In[33]:


def print_metrices(y_test,y_pred_class,y_pred_class_svc,y_pred_class_lin_svc,y_pred_class_sgd):
    print("Accuracy:")
    print(metrics.accuracy_score(y_test,y_pred_class))
    print(metrics.accuracy_score(y_test,y_pred_class_svc))
    print(metrics.accuracy_score(y_test,y_pred_class_lin_svc))
    print(metrics.accuracy_score(y_test,y_pred_class_sgd))

    print("\nAverage precision:")
    print(metrics.precision_score(y_test,y_pred_class,average='micro'))
    print(metrics.precision_score(y_test,y_pred_class_svc,average='micro'))
    print(metrics.precision_score(y_test,y_pred_class_lin_svc,average='micro'))
    print(metrics.precision_score(y_test,y_pred_class_sgd,average='micro'))

    print("\nAverage recall:")
    print(metrics.recall_score(y_test,y_pred_class,average='micro'))
    print(metrics.recall_score(y_test,y_pred_class_svc,average='micro'))
    print(metrics.recall_score(y_test,y_pred_class_lin_svc,average='micro'))
    print(metrics.recall_score(y_test,y_pred_class_sgd,average='micro'))
    
    print("\nAverage f1:")
    print(metrics.f1_score(y_test,y_pred_class,average='micro'))
    print(metrics.f1_score(y_test,y_pred_class_svc,average='micro'))
    print(metrics.f1_score(y_test,y_pred_class_lin_svc,average='micro'))
    print(metrics.f1_score(y_test,y_pred_class_sgd,average='micro'))

    print("\nClassification report:")
    print(metrics.classification_report(y_test, y_pred_class))
    print(metrics.classification_report(y_test, y_pred_class_svc))
    print(metrics.classification_report(y_test, y_pred_class_lin_svc))
    print(metrics.classification_report(y_test, y_pred_class_sgd))


# In[34]:


#For positive sentiment classifier
df_train = get_data_frame(final_train_text_list,train_opinion_list,most_common_aspect)
df_test = get_data_frame(final_test_text_list,test_opinion_list,most_common_aspect)

df_train_positive = get_positive_data_frame(df_train,most_common_aspect)
df_test_positive = get_positive_data_frame(df_test,most_common_aspect)
y_test_pos,y_pred_class_pos,y_pred_class_svc_pos,y_pred_class_lin_svc_pos,y_pred_class_sgd_pos=classify_sentiment(df_train_positive,df_test_positive,X_train_aspect_dtm,X_test_aspect_dtm)
with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    print_metrices(y_test_pos,y_pred_class_pos,y_pred_class_svc_pos,y_pred_class_lin_svc_pos,y_pred_class_sgd_pos)


# In[35]:


#For negative sentiment classifier
df_train = get_data_frame(final_train_text_list,train_opinion_list,most_common_aspect)
df_test = get_data_frame(final_test_text_list,test_opinion_list,most_common_aspect)

df_train_neg = get_negative_data_frame(df_train,most_common_aspect)
df_test_neg = get_negative_data_frame(df_test,most_common_aspect)

y_test_neg,y_pred_class_neg,y_pred_class_svc_neg,y_pred_class_lin_svc_neg,y_pred_class_sgd_neg=classify_sentiment(df_train_neg,df_test_neg,X_train_aspect_dtm,X_test_aspect_dtm)
with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    print_metrices(y_test_neg,y_pred_class_neg,y_pred_class_svc_neg,y_pred_class_lin_svc_neg,y_pred_class_sgd_neg)


# In[36]:


#For neutral or conflict sentiment classifier
df_train = get_data_frame(final_train_text_list,train_opinion_list,most_common_aspect)
df_test = get_data_frame(final_test_text_list,test_opinion_list,most_common_aspect)

df_train_neu = get_neutral_data_frame(df_train,most_common_aspect)
df_test_neu = get_neutral_data_frame(df_test,most_common_aspect)

y_test_neu,y_pred_class_neu,y_pred_class_svc_neu,y_pred_class_lin_svc_neu,y_pred_class_sgd_neu=classify_sentiment(df_train_neu,df_test_neu,X_train_aspect_dtm,X_test_aspect_dtm)
with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    print_metrices(y_test_neu,y_pred_class_neu,y_pred_class_svc_neu,y_pred_class_lin_svc_neu,y_pred_class_sgd_neu)


# In[37]:


#Aspect Based Sentiment analyis of user's input.
user_input=input("Enter a laptop review:\n\n")
#Preprocessing and vectorizing
tagged_user_input = posTag([user_input])
filter_tagged_user_input = filterTag(tagged_user_input)

user_input_series=pd.Series(filter_tagged_user_input)
user_input_series_dtm=vect.transform(user_input_series)

predict_aspect= svc.predict(user_input_series_dtm)
extra_feature=get_dict_aspect(predict_aspect, most_common_aspect)
extra_feature_dtm=DictVectorizer().fit_transform(extra_feature)
predict_aspect


# In[38]:


#predicting weather the dectected aspect is positive or not
test_opinion_list=[]
df_test = get_data_frame(filter_tagged_user_input,test_opinion_list,most_common_aspect)
df_train = get_data_frame(final_train_text_list,train_opinion_list,most_common_aspect)

df_train_positive = get_positive_data_frame(df_train,most_common_aspect)
y_test_pos,y_pred_class_pos,y_pred_class_svc_pos,y_pred_class_lin_svc_pos,y_pred_class_sgd_pos=classify_sentiment(df_train_positive,df_test,X_train_aspect_dtm,extra_feature_dtm)

y_pred_class_svc_pos


# In[39]:


#predicting weather the dectected aspect is negative or not
test_opinion_list=[]
df_test = get_data_frame(filter_tagged_user_input,test_opinion_list,most_common_aspect)
df_train = get_data_frame(final_train_text_list,train_opinion_list,most_common_aspect)

df_train_negative = get_negative_data_frame(df_train,most_common_aspect)
y_test_neg,y_pred_class_neg,y_pred_class_svc_neg,y_pred_class_lin_svc_neg,y_pred_class_sgd_neg=classify_sentiment(df_train_negative,df_test,X_train_aspect_dtm,extra_feature_dtm)

y_pred_class_svc_neg


# In[40]:


#predicting weather the dectected aspect is neutral or coflict or not
test_opinion_list=[]
df_test = get_data_frame(filter_tagged_user_input,test_opinion_list,most_common_aspect)
df_train = get_data_frame(final_train_text_list,train_opinion_list,most_common_aspect)

df_train_neutral = get_neutral_data_frame(df_train,most_common_aspect)
y_test_neu,y_pred_class_neu,y_pred_class_svc_neu,y_pred_class_lin_svc_neu,y_pred_class_sgd_neu=classify_sentiment(df_train_neutral,df_test,X_train_aspect_dtm,extra_feature_dtm)

y_pred_class_svc_neu


# In[41]:


#Finding the aspect that is positive
index_positive=[]
for i, (a, b) in enumerate(zip(predict_aspect.tolist()[0], y_pred_class_svc_pos.tolist()[0])):
    if a ==1 and b==1:
        index_positive.append(i)
index_positive         


# In[42]:


#Finding the aspect that is negative
index_negative=[]
for i, (a, b) in enumerate(zip(predict_aspect.tolist()[0], y_pred_class_svc_neg.tolist()[0])):
    if a ==1 and b==1:
        index_negative.append(i)
index_negative         


# In[43]:


#Finding the aspect that is neutral
index_neutral=[]
for i, (a, b) in enumerate(zip(predict_aspect.tolist()[0], y_pred_class_svc_neu.tolist()[0])):
    if a ==1 and b==1:
        index_neutral.append(i)
index_neutral         


# In[44]:


output=[]


# In[45]:


if index_positive:
    for index in index_positive:
        output.append(sorted(most_common_aspect)[index]+": positive")


# In[46]:


if index_negative:
    for index in index_negative:
        output.append(sorted(most_common_aspect)[index]+": negative")


# In[47]:


if index_neutral:
    for index in index_neutral:
        output.append(sorted(most_common_aspect)[index]+": neutral or conflict")


# In[48]:


#Prediction of Aspect Based Sentiment Analaysis for user's input
output


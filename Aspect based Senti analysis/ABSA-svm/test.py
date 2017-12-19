from sklearn.externals import joblib

tagged_text_list_train=joblib.load('tagged_text_list_train.pkl')
file = open('testfile.txt','w') 
file.write(tagged_text_list_train)
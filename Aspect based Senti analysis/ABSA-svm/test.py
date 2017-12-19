from sklearn.externals import joblib

tagged_text_list_train=joblib.load('tagged_text_list_train.pkl')
joblib.dump(tagged_text_list_train,'test_dump')

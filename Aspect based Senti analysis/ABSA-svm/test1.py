from sklearn.externals import joblib

tagged_text_list_train=joblib.load('test_dump')
joblib.dump(tagged_text_list_train,'tagged_text_list_train_final.pkl')
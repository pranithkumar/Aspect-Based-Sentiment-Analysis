from gensim import models
from sklearn.decomposition import PCA
from matplotlib import pyplot
import plotly.offline as py
import plotly.graph_objs as go
import datapreprocessing as dp
import json

df = dp.dataframecomplete('../Apple-iPhone-Space-Grey-32GB.json','../apple-iphone-6-space-grey-32-gb.json')

reviews = []

for review in df['review']:
	tokens = review.encode('utf-8').split()
	tokens = [x.lower() for x in tokens]
	reviews.append(tokens)

"""finalwords = []
for sentences in df['lemma']:
	for sentence in sentences:
		for word in sentence:	
			finalwords.append(word.encode('utf-8'))

model = models.Word2Vec([finalwords])
print model['Camera']"""

model = models.Word2Vec(reviews)
model.save('model.bin')
#print model['mobile']
#print model['guitar']
words = list(model.wv.vocab)
print model.most_similar('camera')

"""X = model[model.wv.vocab]
pca = PCA(n_components=2)
result = pca.fit_transform(X)
pyplot.scatter(result[:, 0], result[:, 1])
for i, word in enumerate(words):
	pyplot.annotate(word, xy=(result[i, 0], result[i, 1]))
pyplot.show()"""


"""points=[]
for i, word in enumerate(words):
	points.append(word)

trace1 = go.Scatter(x=result[:,0], y=result[:,1], marker={"color": "blue", "size": 12},mode="markers",  text=points, name='Word2Vec Sample')
data=go.Data([trace1])
layout=go.Layout(title="Word2Vec Plot", xaxis={'title':'dim 1'}, yaxis={'title':'dim 2'})
figure=go.Figure(data=data,layout=layout)
py.plot(figure, filename='pyguide_1.html')"""
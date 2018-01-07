import json
import numpy
import pandas

traffic = json.load(open('data/Cell_Phones_and_Accessories_5.json'))
df = pandas.DataFrame(traffic)
print df[0:8]

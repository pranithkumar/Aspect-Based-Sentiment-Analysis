import json
Reviews=json.load(open('amazonreviews.json'))
dic = {}
li = []
for review in Reviews:
	for i in range(1,len(review["title"])):
		li.append(review["title"][i])
print li

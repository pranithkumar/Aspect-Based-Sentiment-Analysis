from fuzzywuzzy import fuzz

f = open('amazon_titles_links.txt','r')
contents = f.read().split('\n')
f.close()
amazon_titles = []
for i in range(0,len(contents)/2):
	amazon_titles.append(contents[i*2])

print amazon_titles

f = open('flipkart_titles_links.txt','r')
contents = f.read().split('\n')
f.close()
flipkart_titles = []
for i in range(0,len(contents)/2):
	flipkart_titles.append(contents[i*2])

print flipkart_titles

for atitle in amazon_titles:
	for ftitle in flipkart_titles:
		if int(fuzz.ratio(atitle,ftitle))>85:
			print atitle
			print ftitle
			print fuzz.ratio(atitle,ftitle)
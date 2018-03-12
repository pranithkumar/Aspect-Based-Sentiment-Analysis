import os
f = open('productlinkamazon.txt','r')
titles = f.read()
f.close()
title=titles.split('/')[1]
print title
os.system("scrapy crawl searchspideramazon")
os.system("scrapy crawl getproductspideramazon")
os.system("scrapy crawl completeamazonscraper -o data/"+title+".json")
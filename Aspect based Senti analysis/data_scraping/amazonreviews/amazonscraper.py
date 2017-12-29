import os
os.system("scrapy crawl searchspider")
os.system("scrapy crawl getproductspider")
os.system("scrapy crawl completeamazonscraper -o amazonreviews.json")
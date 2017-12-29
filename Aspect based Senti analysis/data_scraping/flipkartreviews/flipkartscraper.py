import os
os.system("scrapy crawl searchspider")
os.system("scrapy crawl completeflipkartscraper -o flipkartreviews.json")
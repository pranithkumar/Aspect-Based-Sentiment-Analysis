import os
os.system("scrapy crawl fksearchspider")
os.system("scrapy crawl completeflipkartscraper -o flipkartreviews.json")

os.system("scrapy crawl searchspider")
os.system("scrapy crawl getproductspider")
os.system("scrapy crawl completeamazonscraper -o amazonreviews.json")

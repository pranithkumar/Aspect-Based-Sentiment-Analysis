import os
import sys

runf = 'scrapy crawl searchspider'
os.system(runf)
runf = 'scrapy crawl getproductspider'
os.system(runf)
runf = 'scrapy crawl completeamazonscraper -o amazonreviews_test.json'
os.system(runf)
sys.exit(0)

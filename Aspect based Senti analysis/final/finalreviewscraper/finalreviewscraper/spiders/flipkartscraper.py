# -*- coding: utf-8 -*-
import scrapy
import requests


class FlipkartscraperSpider(scrapy.Spider):
    name = 'flipkartscraper'
    allowed_domains = ['flipkart.com']
    start_urls = ["https://www.flipkart.com/search?q="]

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url+self.ip+"&otracker=start&as-show=on&as=off", dont_filter=True)

    def parse(self, response):
		#extracting titles of all products for type one search results
		titles = response.xpath('//a[contains(@rel,"noopener noreferrer")]/div/div/div/div/img/@alt').extract()
		#extracting titles of all products for type two search results
		if len(titles) == 0:
			titles = response.xpath('//a[contains(@rel,"noopener noreferrer")]/text()').extract()
		#extracting product links of all products   
		links = response.xpath('//a[contains(@rel,"noopener noreferrer")]/@href').extract()
		#print links[0]
		#storing the titles and product links of search results in output.txt
		f=open("flipkart_titles_links.txt","w")
		for i in range(0,len(titles)-3):
			f.write(str(titles[i].encode('utf-8','ignore'))+"\n"+str(links[i].encode('utf-8','ignore'))+"\n")
		pid = links[0].split("?")[1].split("&")[0].split("=")[1]
		n=100
		#required attributes for review extraction
		data = {"productId": pid, # end of url pid=MOBEG4XWJG7F9A6Z
		    "count": n,
		    "ratings": "ALL",
		    "reviewerType:ALL"
		    "sortOrder": "MOST_HELPFUL"}

		headers = ({"x-user-agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.92 Safari/537.36 FKUA/website/41/website/Desktop"})
		#api call to extract reviews
		data = requests.get("https://www.flipkart.com/api/3/product/reviews", params=data, headers=headers).json()
		#calculating the number of reviews extracted
		if len(data['RESPONSE']['data'])<n:
			n=len(data['RESPONSE']['data'])
		#extracting the required attributes from the json data acquired
		for i in range(0,n):
			reviewer=data['RESPONSE']['data'][i][u'value'][u'author']
			title=data['RESPONSE']['data'][i][u'value'][u'title']
			rating=data['RESPONSE']['data'][i][u'value'][u'rating']
			verification=data['RESPONSE']['data'][i][u'value'][u'reviewPropertyMap']
			date=data['RESPONSE']['data'][i][u'value'][u'created']
			review=data['RESPONSE']['data'][i][u'value'][u'text']
			#print "review number="+str(i)+"\n"+reviewer+"\n"+title+"\n"+str(rating)+"\n"+str(verification)+"\n"+date+"\n"+review+"\n"
			#defining json file attributes
			yield{
				"reviewer":reviewer,
				"title":title,
				"rating":rating,
				"date":date,
				"verification":verification,
				"review":review
			}
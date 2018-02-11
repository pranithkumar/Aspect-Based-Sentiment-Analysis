# -*- coding: utf-8 -*-
import scrapy
import requests

class CompleteflipkartscraperSpider(scrapy.Spider):
    name = 'completeflipkartscraper'
    allowed_domains = ['flipkart.com']
    start_urls = ['http://flipkart.com/']

    def parse(self, response):
		f=open("flipkartreviews.json","w")
		f.close()
		f=open("productlinkflipkart.txt","r")
		link=f.read()
		links=link.split("\n")
		temp=links[1].split("?")
		res=temp[1].split("&")
		pid=res[0].split("=")[1]
		n=50
		data = {"productId": pid, # end of url pid=MOBEG4XWJG7F9A6Z
		        "count": n,
		        "ratings": "ALL",
		        "reviewerType:ALL"
		        "sortOrder": "MOST_HELPFUL"}

		headers = ({"x-user-agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.92 Safari/537.36 FKUA/website/41/website/Desktop"})
		data = requests.get("https://www.flipkart.com/api/3/product/reviews", params=data, headers=headers).json()
		if len(data['RESPONSE']['data'])<n:
			n=len(data['RESPONSE']['data'])
		for i in range(0,n):
			reviewer=data['RESPONSE']['data'][i][u'value'][u'author']
			title=data['RESPONSE']['data'][i][u'value'][u'title']
			rating=data['RESPONSE']['data'][i][u'value'][u'rating']
			verification=data['RESPONSE']['data'][i][u'value'][u'reviewPropertyMap']
			date=data['RESPONSE']['data'][i][u'value'][u'created']
			review=data['RESPONSE']['data'][i][u'value'][u'text']
			print "review number="+str(i)+"\n"+reviewer+"\n"+title+"\n"+str(rating)+"\n"+str(verification)+"\n"+date+"\n"+review+"\n"
			yield{
				"reviewer":reviewer,
				"title":title,
				"rating":rating,
				"date":date,
				"verification":verification,
				"review":review
			}
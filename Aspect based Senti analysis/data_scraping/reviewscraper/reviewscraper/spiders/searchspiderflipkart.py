# -*- coding: utf-8 -*-
import scrapy


class SearchspiderflipkartSpider(scrapy.Spider):
    name = 'searchspiderflipkart'
    allowed_domains = ['flipkart.com']
    f=open("input.txt","r")
    search_keyword=f.read()
    start_urls = ["https://www.flipkart.com/search?q="+search_keyword+"&otracker=start&as-show=on&as=off"]

    def parse(self, response):
        title = response.xpath('//a[contains(@rel,"noopener noreferrer")]/@href').extract()
    	f=open("productlinkflipkart.txt","w")
    	for link in title:
    		f.write(str(link)+"\n")

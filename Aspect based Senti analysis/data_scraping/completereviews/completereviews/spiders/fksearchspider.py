# -*- coding: utf-8 -*-
import scrapy


class SearchspiderSpider(scrapy.Spider):
    name = 'fksearchspider'
    allowed_domains = ['flipkart.com']
    f=open("input.txt","r")
    search_keyword=f.read()
    start_urls = ["https://www.flipkart.com/search?q="+search_keyword+"&otracker=start&as-show=on&as=off"]

    def parse(self, response):
    	title = response.xpath('//a[contains(@rel,"noopener noreferrer")]/@href').extract()
    	f=open("productlink.txt","w")
    	for link in title:
    		f.write(str(link)+"\n")

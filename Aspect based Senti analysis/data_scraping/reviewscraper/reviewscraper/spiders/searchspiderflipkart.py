# -*- coding: utf-8 -*-
import scrapy


class SearchspiderflipkartSpider(scrapy.Spider):
    name = 'searchspiderflipkart'
    allowed_domains = ['flipkart.com']
    f=open("input.txt","r")
    search_keyword=f.read()
    start_urls = ["https://www.flipkart.com/search?q="+search_keyword+"&otracker=start&as-show=on&as=off"]

    def parse(self, response):
        titlename = response.xpath('//a[contains(@rel,"noopener noreferrer")]/div/div/div/div/img/@alt').extract()
        if len(titlename) == 0:
            titlename = response.xpath('//a[contains(@rel,"noopener noreferrer")]/text()').extract()    
        titlelink = response.xpath('//a[contains(@rel,"noopener noreferrer")]/@href').extract()
    	f=open("productlinkflipkart.txt","w")
    	for title in range(0,24):
    		f.write(str(titlename[title])+"\n"+str(titlelink[title])+"\n")

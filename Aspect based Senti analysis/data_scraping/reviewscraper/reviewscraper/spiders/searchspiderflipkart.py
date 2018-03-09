#This file takes the search keyword from input.txt as input and stores the titles and respective links of the search results in output.txt
# -*- coding: utf-8 -*-
import scrapy


class SearchspiderflipkartSpider(scrapy.Spider):
    name = 'searchspiderflipkart'
    allowed_domains = ['flipkart.com']
    #input.txt contains the keyword searched
    f=open("input.txt","r")
    search_keyword=f.read()
    start_urls = ["https://www.flipkart.com/search?q="+search_keyword+"&otracker=start&as-show=on&as=off"]

    def parse(self, response):
        #extracting titles of all products for type one search results
        titlename = response.xpath('//a[contains(@rel,"noopener noreferrer")]/div/div/div/div/img/@alt').extract()
        #extracting titles of all products for type two search results
        if len(titlename) == 0:
            titlename = response.xpath('//a[contains(@rel,"noopener noreferrer")]/text()').extract()
        #extracting product links of all products   
        titlelink = response.xpath('//a[contains(@rel,"noopener noreferrer")]/@href').extract()
        #storing the titles and product links of search results in output.txt
    	f=open("productlinkflipkart.txt","w")
    	for title in range(0,len(titlename)):
    		f.write(str(titlename[title])+"\n"+str(titlelink[title])+"\n")

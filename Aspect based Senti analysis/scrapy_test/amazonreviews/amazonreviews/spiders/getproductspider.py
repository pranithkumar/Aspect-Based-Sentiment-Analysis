# -*- coding: utf-8 -*-
import scrapy


class GetproductspiderSpider(scrapy.Spider):
    name = 'getproductspider'
    allowed_domains = ['amazon.in']
    f=open("output.txt","r")
    data=f.read()
    links=data.split("\n")
    start_urls = [links[0]]

    def parse(self, response):
    	link = response.xpath('//a[contains(@class,"a-link-emphasis a-text-bold")]/@href').extract()
        f=open("productlink.txt","w")
        f.write(str(link[0]))
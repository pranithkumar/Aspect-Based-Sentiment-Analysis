# -*- coding: utf-8 -*-
import scrapy


class GetproductspideramazonSpider(scrapy.Spider):
    name = 'getproductspideramazon'
    allowed_domains = ['amazon.in']
    f=open("output.txt","r")
    data=f.read()
    links=data.split("\n")
    start_urls = [links[0]]

    def parse(self, response):
        link = response.xpath('//a[contains(@class,"a-link-emphasis a-text-bold")]/@href').extract()
        temp = response.xpath('//a[contains(@class,"a-link-emphasis a-text-bold")]/text()').extract()
        num = temp[0].split(" ")
        total = int(num[2].replace(",",""))
        f=open("productlinkamazon.txt","w")
        f.write(str(link[0]))
        f.write("\n"+str(total))

# -*- coding: utf-8 -*-
import scrapy


class GetproductspideramazonSpider(scrapy.Spider):
    name = 'getproductspideramazon'
    allowed_domains = ['amazon.in']
    f=open("output.txt","r")
    data=f.read()
    f.close()
    links=data.split("\n")
    start_urls = [links[1]]

    def parse(self, response):
        link = response.xpath('//a[contains(@class,"a-link-emphasis a-text-bold")]/@href').extract()
        temp = response.xpath('//a[contains(@class,"a-link-emphasis a-text-bold")]/text()').extract()
        num = temp[0].split(" ")
        total = int(num[2].replace(",",""))
        f=open("output.txt","r")
        data=f.read()
        f.close()
        title = data.split('\n')[0]
        f=open("productlinkamazon.txt","w")
        f.write(str(title)+"\n")
        f.write(str(link[0]))
        f.write("\n"+str(total))

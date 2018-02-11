# -*- coding: utf-8 -*-
import scrapy


class SearchspideramazonSpider(scrapy.Spider):
    name = 'searchspideramazon'
    allowed_domains = ['amazon.in']
    f=open("input.txt","r")
    product=f.read()
    search_keyword=product.replace(" ","+")
    start_urls = ["https://www.amazon.in/s/ref=nb_sb_noss_2?url=search-alias%3Daps&field-keywords="+search_keyword]

    def parse(self, response):
        titles = response.xpath('//a[contains(@class,"a-link-normal s-access-detail-page  s-color-twister-title-link a-text-normal")]/h2/text()').extract()
        links = response.xpath('//a[contains(@class,"a-link-normal s-access-detail-page  s-color-twister-title-link a-text-normal")]/@href').extract()
        f=open("output.txt","w")
        for i in range(0,len(links)):
            f.write(str(titles[i].encode('utf-8'))+"\n"+str(links[i].encode('utf-8'))+"\n")

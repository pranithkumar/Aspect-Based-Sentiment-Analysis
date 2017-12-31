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
        title = response.xpath('//a[contains(@class,"a-link-normal s-access-detail-page  s-color-twister-title-link a-text-normal")]/@href').extract()
        f=open("output.txt","w")
        for link in title:
            f.write(str(link)+"\n")

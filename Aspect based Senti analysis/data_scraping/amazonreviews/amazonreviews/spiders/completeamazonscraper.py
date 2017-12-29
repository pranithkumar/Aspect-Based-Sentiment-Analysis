# -*- coding: utf-8 -*-
import scrapy


class CompleteamazonscraperSpider(scrapy.Spider):
    name = 'completeamazonscraper'
    allowed_domains = ['amazon.in']
    f=open("amazonreviews.json","w")
    f.close()
    f=open("productlink.txt","r")
    contents=f.read()
    link=contents.split("\n")
    if(int(link[1])/10<20):
        n=int(link[1])/10
    else:
        n=20
    start_urls = ['http://amazon.in/'+link[0]+'&pageNumber={}'.format(i) for i in range(1,n)]

    def parse(self, response):
        review = response.xpath('//span[contains(@class,"a-size-base review-text")]/text()').extract()
        reviewer = response.xpath('//a[contains(@class,"a-size-base a-link-normal author")]/text()').extract()
        title = response.xpath('//a[contains(@class,"a-size-base a-link-normal review-title a-color-base a-text-bold")]/text()').extract()
        date = response.xpath('//span[contains(@class,"a-size-base a-color-secondary review-date")]/text()').extract()
        verification = response.xpath('//span[contains(@class,"a-size-mini a-color-state a-text-bold")]/text()').extract()
        rating = response.xpath('//span[contains(@class,"a-icon-alt")]/text()').extract()
        yield{
        	"reviewer":reviewer,
        	"title":title,
        	"rating":rating,
        	"date":date,
            	"verification":verification,
        	"review":review
        }
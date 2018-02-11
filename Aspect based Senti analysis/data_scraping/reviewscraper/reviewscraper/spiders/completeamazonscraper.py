#This file takes the link to see all reviews from productlinkamazon.txt as input and scrapes through n pages and stores the data in a json file.
# -*- coding: utf-8 -*-
import scrapy
import html2text

class CompleteamazonscraperSpider(scrapy.Spider):
    name = 'completeamazonscraper'
    allowed_domains = ['amazon.in']
    #clearing existing data from the json file
    #f=open("amazonreviews.json","w")
    #f.close()
    #productlinkamazon.txt contains the title,link to see all reviews and number of reviews
    f=open("productlinkamazon.txt","r")
    contents=f.read()
    link=contents.split("\n")
    #n is the number of pages to scrape
    n=10
    #link[1] contains the link to see all reviews
    start_urls = ['http://amazon.in/'+link[1]+'&pageNumber={}'.format(i) for i in range(1,n)]

    def parse(self, response):
        #extracting review in html format
        htmlreview = response.xpath('//span[contains(@class,"a-size-base review-text")]').extract()
        #extracting date
        date = response.xpath('//span[contains(@data-hook,"review-date")]/text()').extract()
        #extracting reviewer name
        reviewer = response.xpath('//a[contains(@class,"a-size-base a-link-normal author")]/text()').extract()
        #extracting review title
        title = response.xpath('//a[contains(@class,"a-size-base a-link-normal review-title a-color-base a-text-bold")]/text()').extract()
        #extracting authentication of the user
        verification = response.xpath('//span[contains(@class,"a-size-mini a-color-state a-text-bold")]/text()').extract()
        #extracting user rating
        rating = response.xpath('//div[contains(@class,"a-row")]/a[contains(@class,"a-link-normal")]/@title').extract()
        #converting html data to raw string
        converter = html2text.HTML2Text()
        converter.ignore_links = True
        review=[]
        for i in range(0,len(htmlreview)):
            review.append(converter.handle(htmlreview[i]))
        #defining json file attributes
        yield{
        	"reviewer":reviewer,
        	"title":title,
        	"rating":rating,
        	"date":date,
            "verification":verification,
        	"review":review
        }

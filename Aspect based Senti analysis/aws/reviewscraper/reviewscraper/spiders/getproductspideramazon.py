#This file takes the first title and link from output.txt as input and stores the title and the link to see all reviews in productlinkamazon.txt
# -*- coding: utf-8 -*-
import scrapy


class GetproductspideramazonSpider(scrapy.Spider):
    name = 'getproductspideramazon'
    allowed_domains = ['amazon.in']
    #output.txt contains the titles and links of the search results
    f=open("output.txt","r")
    data=f.read()
    f.close()
    links=data.split("\n")
    #selecting the first product from search results
    start_urls = [links[1]]

    def parse(self, response):
        #extracting link to see all reviews
        link = response.xpath('//a[contains(@class,"a-link-emphasis a-text-bold")]/@href').extract()
        #extracting number of reviews
        temp = response.xpath('//a[contains(@class,"a-link-emphasis a-text-bold")]/text()').extract()
        #converting number of reviews from string to number
        num = temp[0].split(" ")
        total = int(num[2].replace(",",""))
        #taking title of first product from output.txt
        f=open("output.txt","r")
        data=f.read()
        f.close()
        title = data.split('\n')[0]
        #storing the product title,link to see all reviews and number of reviews in productlinkamazon.txt
        f=open("productlinkamazon.txt","w")
        f.write(str(title)+"\n")
        f.write(str(link[0]))
        f.write("\n"+str(total))

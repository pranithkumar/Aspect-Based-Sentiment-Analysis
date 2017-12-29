# -*- coding: utf-8 -*-
import scrapy


class ReviewspiderSpider(scrapy.Spider):
    name = 'reviewspider'
    allowed_domains = ['amazon.in']
    start_urls = ['https://www.amazon.in/Redmi-4-Black-16-GB/product-reviews/B01MT0QKAG/ref=cm_cr_arp_d_paging_btm_2?ie=UTF8&reviewerType=all_reviews&pageNumber={}'.format(i) for i in range(1,10)]

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
        	"review":review
        }
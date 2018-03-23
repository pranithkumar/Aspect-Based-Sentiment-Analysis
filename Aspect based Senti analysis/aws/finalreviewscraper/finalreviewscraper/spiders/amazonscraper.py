# -*- coding: utf-8 -*-
import scrapy
import html2text


class AmazonscraperSpider(scrapy.Spider):
    name = 'amazonscraper'
    allowed_domains = ['amazon.in']
    start_urls = ["https://www.amazon.in/s/ref=nb_sb_noss_2?url=search-alias%3Daps&field-keywords="]

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url+self.ip, dont_filter=True,headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'})

    def parse(self, response):
        #extracting titles of all products
        titles = response.xpath('//a[contains(@class,"a-link-normal s-access-detail-page  s-color-twister-title-link a-text-normal")]/h2/text()').extract()
        #extracting product links of all products
        links = response.xpath('//a[contains(@class,"a-link-normal s-access-detail-page  s-color-twister-title-link a-text-normal")]/@href').extract()
        f=open("amazon_titles_links.txt","w")
        for i in range(0,len(links)):
            f.write(str(titles[i].encode('utf-8'))+"\n"+str(links[i].encode('utf-8'))+"\n")

        for i in links:
            if '/dp/' in i:
                link = i
                break
        print "\n\n\n\n\n\n\n\n\n\n"
        print link

        link = link.replace('/dp/','/product-reviews/') + '/ref=cm_cr_dp_d_show_all_btm?ie=UTF8&reviewerType=all_reviews'
        
        for i in range(1,11):
            request = scrapy.Request(link+'&pageNumber='+str(i),callback=self.scrape_reviews,headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'})
            print request
            yield request

    def scrape_reviews(self,response):
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
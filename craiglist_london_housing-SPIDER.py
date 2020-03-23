# -*- coding: utf-8 -*-
import scrapy


class CraiglistLondonHousingSpider(scrapy.Spider):
    
    name = 'craiglist_london_housing'
    allowed_domains = ['london.craigslist.org']
    start_urls = ['https://london.craigslist.org/d/flats-housing-for-rent/search/apa']

    def parse(self, response):
        houses= response.xpath("//li[@class='result-row']")
        for house in houses:
            name=house.xpath(".//a[@class='result-title hdrlnk']/text()").get()
            link=house.xpath(".//a[@class='result-title hdrlnk']/@href").get()
            date=house.xpath(".//time[@class='result-date']/text()").get()

        

            yield scrapy.Request(link,
                                callback=self.parse_listing,
                                meta={'house_name':name,
                                      'house_link':link,
                                      'house_date':date})

        next_page= response.xpath("//a[@class='button next']").get()

        if next_page:
            yield response.follow (url=next_page, callback=self.parse)

    def parse_listing(self,response):
        name=response.meta['house_name']
        link=response.meta['house_link']
        date=response.meta['house_date']


        post_id= response.xpath("//p[@class='postinginfo'] [1]/text()").get().strip('post id: ')

        description = "".join(line for line in response.xpath('//*[@id="postingbody"]/text()').extract()).strip()
                                                       

        images= response.xpath("//div[@id='thumbs']/a/img/@src").getall()
        images=[image.replace('50x50c','600x450')for image in images]

        yield {
            'house_name':name,
            'house_link':link,
            'house_date':date,
            'id':post_id,
            'description': description,
            'images':images

        }

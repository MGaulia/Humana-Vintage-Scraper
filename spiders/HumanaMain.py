# -*- coding: utf-8 -*-
import scrapy
import re

class HumanamainSpider(scrapy.Spider):
    name = 'HumanaMain'
    allowed_domains = []

    start_urls = ['https://e-vintage.humana.lt/collections/moterims',
                  'https://e-vintage.humana.lt/collections/vyrams',
                  'https://e-vintage.humana.lt/collections/aksesuariai'
                  ]

    def parse(self, response):
        max_page_count = response.xpath('//li[@class="pagination__text"]/text()[1]').extract()[0]
        max_page_count = int(max_page_count.split("iš")[1].split("psl")[0].strip())
        for page in range(1,max_page_count+1):
            next_page_link = response.url + "?page=" + str(page)
            yield scrapy.Request(next_page_link, callback=self.scrape_products)


    def scrape_products(self, response):
        links = response.xpath('//a[@class="grid-view-item__link grid-view-item__image-container full-width-link"]/@href').extract()
        names = response.xpath('//div[@class="h4 grid-view-item__title product-card__title"]/text()[1]').extract()
        prices = response.xpath('//span[@class="price-item price-item--sale"]/text()[1]').extract()
        for link, name, price in zip(links, names, prices):
            yield {
                "name" : name,
                "price" : float( re.findall("\d+\,\d+", price)[0].replace(',','.') ),
                "link" : "https://e-vintage.humana.lt/"+link
            }


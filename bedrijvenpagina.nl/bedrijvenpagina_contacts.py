# -*- coding: utf-8 -*-
# (c) dlancer, 2017

from scrapy import Spider, Request

BASE_URL = 'https://www.bedrijvenpagina.nl'


class BedrijvenpaginaContactsSpider(Spider):
    name = "bedrijvenpagina_contacts"
    allowed_domains = ["bedrijvenpagina.nl"]

    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36'
    }

    def start_requests(self):
        yield Request(url=BASE_URL, callback=self.process_categories)

    def process_categories(self, response):

        # if proxy is enabled check proper response from site
        if self.settings.get('PROXY_USE'):
            if not response.xpath('//a[@class="navbar-brand"]'):
                yield Request(url=response.url, dont_filter=True, callback=self.process_categories)

        categories = response.css('ul.dropdown-menu-right').css('.categorieen')
        categories_urls = categories.css('a::attr(href)').extract()
        for url in categories_urls:
            yield Request(url=BASE_URL + url, callback=self.parse)

    def parse(self, response):

        # if proxy is enabled check proper response from site
        if self.settings.get('PROXY_USE'):
            if not response.xpath('//a[@class="navbar-brand"]'):
                yield Request(url=response.url, dont_filter=True, callback=self.parse)

        for card in response.css('div.card'):
            name = card.css('h3.fn').css('.org span::text').extract_first()
            adr = card.css('span.adr')
            street_address = adr.css('span.street-address::text').extract_first()
            postal_code = adr.css('span.postal-code::text').extract_first()
            locality = adr.css('span.locality::text').extract_first()
            country = adr.css('span.country-name::text').extract_first()
            #info = card.css('div.note p::text').extract_first()

            yield {
                'name': name,
                'street_address': street_address,
                'postal_code': postal_code,
                'locality': locality,
                'country': country,
                #'info': info
            }

        # select the next page for parsing
        next_page = response.css('div.pagers').css('ul.pager').css('li.next a::attr(href)').extract_first()

        if next_page is not None:
            next_url = BASE_URL + next_page
            yield Request(url=next_url, callback=self.parse)

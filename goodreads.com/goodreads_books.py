# -*- coding: utf-8 -*-
# (c) dlancer, 2017

import re
from scrapy import Spider, Request, FormRequest

BASE_URL = 'https://www.goodreads.com'
CATEGORIES = ['present-tense']
USERNAME = ''
PASSWORD = ''


class GoodreadsBooksSpider(Spider):
    name = 'goodreads_books'
    allowed_domains = ['www.goodreads.com']
    start_urls = [BASE_URL + '/user/sign_in']

    def parse(self, response):
        token = response.css('input[name="authenticity_token"]::attr(value)').extract_first()
        yield FormRequest.from_response(
            response,
            formxpath='//form[@name="sign_in"]',
            formdata={
                'user[email]': USERNAME,
                'user[password]': PASSWORD,
                'authenticity_token': token,
            },
            callback=self.after_login)

    def after_login(self, response):
        # check login succeed before going on
        if 'Sorry, we didn’t recognize' in response.body:
            self.logger.error('Login failed')
            return

        # parse all categories
        for category in CATEGORIES:
            yield Request(
                url=BASE_URL + '/shelf/show/' + category,
                callback=self.action
            )

    def action(self, response):

        # item parsing
        for book in response.css('div.elementList'):
            full_title = book.css('a.bookTitle::text').extract_first()
            try:
                title, add_info = full_title.split(' (')
            except ValueError:
                title = full_title
                add_info = ''

            full_info = book.css('span.greyText').css('.smallText::text').extract()
            info = None
            for text in full_info:
                if 'avg rating' in text:
                    info = text
                    break
            if info is None:
                self.logger.error('html layout changed on goodreads.com, can\'t parse anything.')
                return

            avg_rating_info, ratings_info, published_info = info.encode('utf-8').split('\xe2\x80\x94')
            result = re.search('(\d+\.\d+)', avg_rating_info)
            avg_rating = result.group(0) if result is not None else ''
            result = re.search('\d+(?:,\d+)?', ratings_info)
            ratings = result.group(0).replace(',', '') if result is not None else ''
            result = re.search('(\d+)', published_info)
            year = result.group(0) if result is not None else ''
            yield {
                'title': title.rstrip(),
                'author': book.css('a.authorName span::text').extract_first(),
                'info': add_info.replace('(', '').replace(')', ''),
                'avg_rating': avg_rating,
                'ratings': ratings,
                'year': year,
            }

        # select the next page for parsing
        next_page = response.css('a.next_page::attr(href)').extract_first()
        if next_page is not None:
            next_url = BASE_URL + next_page
            yield Request(url=next_url, callback=self.action)

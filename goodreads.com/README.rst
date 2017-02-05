goodreads.com scrapy spider
===========================

Basic scrapy spider for books information from goodreads.com

Usage
=====

You can use this spider for any categories, just add categories you need to ``CATEGORIES``.

Before start spider you should add your goodreads.com account credentials, without this step you will get 
only first 50 most popular books from category.

Do not forget setup ``ROBOTSTXT_OBEY = False`` in your scrapy project settings.

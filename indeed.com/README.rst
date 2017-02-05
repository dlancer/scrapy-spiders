Installation
============

For proper script usage you need python 2.7 environment with installed packages::


    pip install -r requirements.txt

Usage
=====

Default job type is 'fulltime', but you can override it from command line.

Spider use xlsx file for scraping all locations by default.

Examples::

    cd dscrapper
    scrapy crawl indeed_jobs -a query=Java -o jobs.csv
    scrapy crawl indeed_jobs -a query=Java radius=100 -o jobs.csv
    scrapy crawl indeed_jobs -a query=Java job_type=contract radius=100 -o jobs.json


if xlsx file does not exist, the you can define locations from command line::


    scrapy crawl indeed_jobs -a query=Java city=New+York state=NY job_type=contract radius=100 -o jobs.json



Settings
========

You can adjust various scrapping settings in settings.py

Settings related for scrapping speed and chance what your IP is will be banned::

    CONCURRENT_REQUESTS = 32
    DOWNLOAD_DELAY = 3
    CONCURRENT_REQUESTS_PER_DOMAIN = 16
    CONCURRENT_REQUESTS_PER_IP = 16


I recommend you use lower settings.

You can also adjust AutoThrottle extension settings and enable and setup proxy usage in settings.py


Caveats
=======

This spider just a POC, so csvexporte class is not included.

indeed.com can detect crawling very fast, so you must limit your crawling speed and use proxy.
Installation
============

For proper script usage you need python 2.7 environment with installed packages::

    pip install -r requirements.txt


Usage
=====

Run this commands for scrape data::

    cd dscrapper
    scrapy crawl bedrijvenpagina_contacts -o contacts.json


All scrapped data will be saved to contacts.json as JSON formatted file.

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

This spider just a POC, so sometimes you can get empty address if contact information submitted to wrong field on
bedrijvenpagina.nl, but you can try extract this information from info field.

bedrijvenpagina.nl can detect crawling very fast, so you must limit your crawling speed and use proxy.
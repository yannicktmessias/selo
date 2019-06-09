# -*- coding: utf-8 -*-
from scrapy import Spider, Selector, FormRequest
import os

class AsesSpider(Spider):
    name = 'ases'
    start_url = 'http://asesweb.governoeletronico.gov.br/ases/'
    start_urls = [start_url]

    def parse(self, response):
        pass

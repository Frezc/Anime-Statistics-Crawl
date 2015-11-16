# -*- coding: utf-8 -*-
import scrapy

from anime_statistics.items import ANNAnimeBaseInfo


class AnnUrlSpider(scrapy.Spider):
    name = "ann_base"
    allowed_domains = ["animenewsnetwork.com"]
    start_urls = [
        'http://www.animenewsnetwork.com/encyclopedia/anime-list.php?showdate=1&limit_to=9999&showT=1&showM=1&showO=1&showN=1&showS=1&licensed=&sort=date',
    ]

    def parse(self, response):
        sel = response.xpath('//tbody[2]/tr/td[1]/font')
        info_list = []
        for item in sel.xpath('b/a | a'):
            base_info = ANNAnimeBaseInfo()
            base_info['url'] = item.xpath('@href').extract()[0]
            # exp = item.xpath('font/text()').re(r'([^\(\)]+)(\s\(([^\(\)]+)\))*$')
            # base_info['name_english'] = exp[0]
            # base_info['type'] = exp[3]
            info_list.append(base_info)
        return info_list

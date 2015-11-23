# -*- coding: utf-8 -*-
from anime_statistics.db_filter.MySqlConn import MysqlConn
import scrapy


class BgmInfospiderSpider(scrapy.Spider):
    name = "BGMInfo"
    allowed_domains = ["bangumi.tv"]
    conn = MysqlConn()
    cur = conn.start_conn()

    def __init__(self, *args, **kwargs):
        super(BgmInfospiderSpider, self).__init__(*args, **kwargs)
        self.start_urls = []
        i = 1
        while i <= 404:
            self.start_urls.append('http://bangumi.tv/anime/browser?page=' + str(i))
            i += 1

    def parse(self, response):
        sels = response.xpath('//ul[@id="browserItemList"]/li/div[@class="inner"]')
        for sel in sels:
            sid = sel.xpath('h3/a/@href').re(r'/subject/(\d+)')[0]
            url = 'http://bangumi.tv' + sel.xpath('h3/a/@href').extract()[0]
            name = sel.xpath('h3/small/text()').extract()
            name_chinese = sel.xpath('h3/a/text()').extract()[0]
            if len(name) < 1:
                name = name_chinese
            else:
                name = name[0]

            info = sel.xpath('p[@class="info tip"]/text()').extract()
            if len(info) > 0:
                info = info[0]
                info = info.strip()
            else:
                info = ''

            values = [
                sid,
                name,
                name_chinese,
                url,
                info
            ]
            self.cur.execute(
                'insert into bgm_anime_info (id, name, name_chinese, url, info) values(%s,%s,%s,%s,%s)',
                values)

    def closed(self, reason):
        self.conn.close()

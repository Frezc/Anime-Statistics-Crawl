# -*- coding: utf-8 -*-
import scrapy
from anime_statistics.db_filter.MySqlConn import MysqlConn


class SatiInfospiderSpider(scrapy.Spider):
    name = "SATIInfo"
    allowed_domains = ["animesachi.com"]
    conn = MysqlConn()
    cur = conn.start_conn()

    def __init__(self, *args, **kwargs):
        super(SatiInfospiderSpider, self).__init__(*args, **kwargs)
        self.start_urls = []
        i = 1958
        while i <= 2015:
            self.start_urls.append('http://www.animesachi.com/visitor/year_' + str(i) + '_1.html?sort=startDay_up')
            i += 1

    def parse(self, response):
        sum = response.xpath('//div[@class="page_info_summury"]/text()').re(r'\d+')[0]
        sum = int(sum)
        # 10 items per page
        pages = int((sum + 10 - 1) / 10)
        i = 1
        url = response.url
        while i <= pages:
            item_url = url[:44] + str(i) + url[url.find('.html'):]
            i += 1
            yield scrapy.Request(item_url, self.parse_item)

    def parse_item(self, response):
        sels = response.xpath(u'//a[@title="基本情報を見る"]')

        for sel in sels:
            url = sel.xpath('@href').extract()[0]
            aid = url[8:url.find('.html')]
            url = 'http://www.animesachi.com/visitor/' + url
            name = sel.xpath('text()').extract()[0]
            air_date = sel.xpath(u'../../td[@title="放送開始日"]/text()').extract()[0]

            values = [
                aid,
                name,
                url,
                air_date
            ]
            self.cur.execute(
                'insert into sati_anime_info (id, name, url, air_date) values(%s,%s,%s,%s)',
                values)

    def closed(self, reason):
        self.conn.close()

# -*- coding: utf-8 -*-
import scrapy
from anime_statistics.db_filter.MySqlConn import MysqlConn


class ANNConsSpider(scrapy.Spider):
    name = "AnnCons"
    allowed_domains = ["animenewsnetwork.com"]
    conn = MysqlConn()
    cur = conn.start_conn()

    def __init__(self, **kwargs):
        super(ANNConsSpider, self).__init__(**kwargs)
        self.start_urls = []
        self.cur.execute('SELECT url FROM ann_anime_info')
        results = self.cur.fetchall()
        # print results
        for result in results:
            self.start_urls.append(result[0])

    def parse(self, response):
        # fix the vintage issue
        vintage = response.xpath('//div[@id="infotype-7"]').xpath('span|div[@class="tab"][1]').xpath('text()').extract()
        if len(vintage) > 0:
            vintage = vintage[0]

        rate_n = response.xpath('//div[@id="infotype-8"]/span/text()').extract()
        cons = 0
        if len(rate_n) > 0:
            s = rate_n[0]
            if int(s[:s.find(u'rating') - 1]) >= 150:
                cons = 1

        self.cur.execute(
            'update ann_anime_info set vintage = %s, consider = %s WHERE url = %s',
            [vintage, cons, response.url])

    def closed(self, reason):
        self.conn.close()

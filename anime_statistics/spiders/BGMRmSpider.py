# -*- coding: utf-8 -*-
from anime_statistics.db_filter.MySqlConn import MysqlConn
import scrapy


class BGMRmSpider(scrapy.Spider):
    name = "BGMRm"
    allowed_domains = ["bangumi.tv"]
    conn = MysqlConn()
    cur = conn.start_conn()

    def __init__(self, *args, **kwargs):
        super(BGMRmSpider, self).__init__(**kwargs)
        self.start_urls = []
        self.cur.execute('select bgm_url from anime_relate_info where bgm_url is not null;')
        results = self.cur.fetchall()
        for result in results:
            self.start_urls.append(result[0])

    def parse(self, response):
        n = response.xpath('//span[@property="v:votes"]/text()').extract()[0]
        n = int(n)
        if n < 200:
            self.cur.execute('delete from anime_relate_info WHERE bgm_url = %s', response.url)

    def closed(self, reason):
        self.conn.close()

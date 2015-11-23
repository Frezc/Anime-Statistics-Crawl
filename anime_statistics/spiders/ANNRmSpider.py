# -*- coding: utf-8 -*-
import scrapy
from anime_statistics.db_filter.MySqlConn import MysqlConn


class ANNRmSpider(scrapy.Spider):
    name = "AnnRm"
    allowed_domains = ["animenewsnetwork.com"]
    conn = MysqlConn()
    cur = conn.start_conn()

    def __init__(self, **kwargs):
        super(ANNRmSpider, self).__init__(**kwargs)
        self.start_urls = []
        self.cur.execute('SELECT url FROM ann_anime_info')
        results = self.cur.fetchall()
        print results
        # for result in results:
        #     self.start_urls.append()

    def parse(self, response):
        pass

    def closed(self, reason):
        self.conn.close()

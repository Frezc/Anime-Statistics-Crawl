# -*- coding: utf-8 -*-
import scrapy

from anime_statistics.db_filter.MySqlConn import MysqlConn


class AnnUrlSpider(scrapy.Spider):
    name = "test"
    allowed_domains = ["animenewsnetwork.com"]
    start_urls = ['http://www.animenewsnetwork.com/encyclopedia/anime.php?id=17']
    conn = MysqlConn()
    cur = conn.start_conn()

    def parse(self, response):
        self.cur.execute('select id FROM ann_info where url = %s', ['http://www.animenewsnetwork.com/encyclopedia/anime.php?id=17'])
        print self.cur.fetchall()

    def closed(self, reason):
        self.conn.close()
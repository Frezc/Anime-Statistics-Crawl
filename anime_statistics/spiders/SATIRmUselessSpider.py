# -*- coding: utf-8 -*-
from MySqlConn import MysqlConn
import scrapy


class SatiRmUselessSpider(scrapy.Spider):
    name = "SATIRmUseless"
    allowed_domains = ["animesachi.com"]
    conn = MysqlConn
    cur = conn.start_conn()

    def __init__(self, *args, **kwargs):
        super(SatiRmUselessSpider, self).__init__(*args, **kwargs)
        self.start_urls = []
        self.cur.execute('select sati_url from anime_relate_info')
        results = self.cur.fetchall()
        for result in results:
            self.start_urls.append(result[0])

    def parse(self, response):
        n = response.xpath('//span[@property="v:votes"]/text()').extract()[0]
        n = int(n)
        if n < 20:
            self.cur.execute('delete from anime_relate_info WHERE sati_url = %s', response.url)

    def closed(self, reason):
        self.conn.close()

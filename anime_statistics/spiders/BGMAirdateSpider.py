# -*- coding: utf-8 -*-
import json

import MySQLdb
import scrapy


class BGMAirdateSpider(scrapy.Spider):
    name = "BGMAirdate"
    allowed_domains = ["api.bgm.tv"]
    conn = MySQLdb.connect(host='localhost',
                           user='root',
                           passwd='123456',
                           db='anime_statistics',
                           charset="utf8",
                           port=3306)
    cur = conn.cursor()

    def __init__(self, *args, **kwargs):
        super(BGMAirdateSpider, self).__init__(**kwargs)
        self.start_urls = []
        self.cur.execute('select id from bgm_anime_info')
        results = self.cur.fetchall()
        for result in results:
            self.start_urls.append('http://api.bgm.tv/subject/' + str(result[0]))

    def parse(self, response):
        data = json.loads(response.body)
        value = [data['air_date'], data['id']]
        self.cur.execute('update bgm_anime_info SET air_date = %s where id = %s', value)

    def closed(self, reason):
        self.conn.commit()
        self.cur.close()
        self.conn.close()

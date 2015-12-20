# -*- coding: utf-8 -*-
import scrapy
import json
from anime_statistics.db_filter.MySqlConn import MysqlConn


class ImageSpider(scrapy.Spider):
    name = "ImageSpider"
    allowed_domains = [
        "bgm.tv"
    ]

    conn = MysqlConn()
    cur = conn.start_conn()

    def __init__(self, *args, **kwargs):
        super(ImageSpider, self).__init__(**kwargs)
        self.cur.execute('SELECT bgm_url FROM relate_info')
        urls = self.cur.fetchall()
        # print urls
        for url in urls:
            self.start_urls.append(url[0].split(',')[0].replace('bangumi', 'api.bgm'))

    def parse(self, response):
        data = json.loads(response.body)
        image = data['images']['common']
        url = response.url.replace('api.bgm', 'bangumi')
        rid = self.fetch_id_by_url(url)
        if rid != -1:
            self.cur.execute('update relate_info SET image = %s WHERE id = %s',
                             [image, rid])

    def closed(self, reason):
        self.conn.close()

    def fetch_id_by_url(self, url, column='bgm_url'):
        n = self.cur.execute('select id FROM relate_info WHERE ' + column + ' = %s', url)

        if n == 1:
            return self.cur.fetchone()[0]
        else:
            rurl = '%' + url + '%'
            n = self.cur.execute('select id,' + column + ' FROM relate_info WHERE ' + column + ' like %s', rurl)

            if n > 0:
                rs = self.cur.fetchall()
                for r in rs:
                    for u in r[1].split(','):
                        if u == url:
                            return r[0]

        return -1

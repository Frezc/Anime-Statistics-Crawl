# -*- coding: utf-8 -*-
import scrapy
import json
from anime_statistics.db_filter.MySqlConn import MysqlConn


class AnninfospiderSpider(scrapy.Spider):
    name = "AnnInfo"
    allowed_domains = ["animenewsnetwork.com"]
    conn = MysqlConn()
    cur = conn.start_conn()

    def __init__(self, *args, **kwargs):
        super(AnninfospiderSpider, self).__init__(*args, **kwargs)
        self.start_urls = []
        f = file('ann_base_info.json')
        s = json.load(f)
        f.close()
        i = 0
        while i < len(s):
            item = s[i]
            i += 1
            self.start_urls.append('http://www.animenewsnetwork.com' + item['url'])

    def parse(self, response):
        res = response.xpath('//h1[@id="page_header"]/text()').re(r'([^\(\)]+)(\s\(([^\(\)]+)\))*$')
        name_eng = [res[0]]
        name_jap = []
        atype = res[-1]

        alternatives = response.xpath('//div[@id="infotype-2"]/div[@class="tab"]/text()')
        for alter in alternatives:
            t = alter.re(r'([^\(\)]+)(\s\(([\w|\W]+)\))*$')
            if t[2] == 'Japanese':
                name_jap.append(t[0])
            elif t[2] == '':
                name_eng.append(t[0])

        related = response.xpath('//div[@id="infotype-related"]/a/@href').extract()
        genres = response.xpath('//div[@id="infotype-30"]/span/a/text()').extract()
        themes = response.xpath('//div[@id="infotype-31"]/span/a/text()').extract()
        objectionable = response.xpath(
            '//div[@id="infotype-17"]/span/span[@title="(bloody violence and/or swearing and/or nudity)"]/text()').extract()
        if len(objectionable) > 0:
            objectionable = objectionable[0]
        else:
            objectionable = ''
        summary = response.xpath('//div[@id="infotype-12"]/*/text()').extract()
        if len(summary) > 0:
            summary.pop(0)
        else:
            summary = ''
        running = response.xpath('//div[@id="infotype-4"]/span/text()').extract()
        if len(running) > 0:
            running = running[0]
        else:
            running = ''
        eps = response.xpath('//div[@id="infotype-3"]/span/text()').extract()
        if len(eps) > 0:
            eps = eps[0]
        else:
            eps = 0
        vintage = response.xpath('//div[@id="infotype-7"]/span/text()').extract()
        if len(vintage) > 0:
            vintage = vintage[0]
        else:
            vintage = ''
        opening = response.xpath('//div[@id="infotype-11"]/div[@class="tab"]/text()').extract()
        ending = response.xpath('//div[@id="infotype-24"]/div[@class="tab"]/text()').extract()

        values = [
            ','.join(name_eng),
            ','.join(name_jap),
            atype,
            response.url,
            ','.join(related),
            ','.join(genres),
            ','.join(themes),
            objectionable,
            ' '.join(summary),
            running,
            eps,
            vintage,
            json.dumps(opening),
            json.dumps(ending)
        ]

        self.cur.execute(
            'insert into ann_anime_info (name_english, name_japanese, anime_type, url, related_anime, genres, themes, objectionable_content, plot_summary, running_time, number_of_episodes, vintage, opening, ending) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',
            values)

    def closed(self, reason):
        self.conn.close()

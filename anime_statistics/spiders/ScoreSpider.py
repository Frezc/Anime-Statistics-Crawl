# -*- coding: utf-8 -*-
import scrapy
import time
import re
from anime_statistics.db_filter.MySqlConn import MysqlConn


class ScoreSpider(scrapy.Spider):
    name = "ScoreSpider"
    allowed_domains = [
        "animenewsnetwork.com", "bangumi.tv", "bgm.tv", "animesachi.com"
    ]

    conn = MysqlConn()
    cur = conn.start_conn()

    bgm_score = []
    sati_score = []

    def __init__(self, *args, **kwargs):
        super(ScoreSpider, self).__init__(**kwargs)
        self.table = "Rank" + time.strftime('%Y%m%d')
        self.cur.execute('CREATE TABLE ' + self.table + ' LIKE score_template', )
        self.cur.execute('SELECT * FROM relate_info')
        infos = self.cur.fetchall()
        # print infos

        for info in infos:
            self.cur.execute(
                'insert INTO ' + self.table + ' (relate_id, name, name_english, name_chinese, ann_url, bgm_url, sati_url, air_date) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)',
                info)
        self.conn.commit()

        self.start_urls = []
        self.start_urls.append(
            'http://www.animenewsnetwork.com/encyclopedia/ratings-anime.php?top50=best_bayesian&n=5000')
        for i in range(1, 136):
            self.start_urls.append('http://bangumi.tv/anime/browser?sort=rank&page=' + str(i))

        for i in range(1, 27):
            self.start_urls.append(
                'http://www.animesachi.com/visitor/osusume_' + str(
                    i) + '.html?image=off&sort=mean_down&state=startOrEnd&mean=50&data=20')

    def parse(self, response):
        if response.url.find('animenewsnetwork.com') != -1:
            self.parse_ann(response)
        elif response.url.find('animesachi.com') != -1:
            self.parse_sati(response)
        else:
            self.parse_bgm(response)

    def parse_ann(self, response):
        ann_scores = []
        holders = response.xpath('//tr[@bgcolor="#EEEEEE"]')
        host = 'http://www.animenewsnetwork.com'
        i = 1
        for holder in holders:
            url = holder.xpath('td[@class="t"]/a/@href').extract()[0]
            rid = self.fetch_id_by_url(host + url, 'ann_url')
            if rid != -1:
                name_english = holder.xpath('td[@class="t"]/a/text()').extract()[0]
                score, votes = holder.xpath('td[@class="r"]/text()').extract()
                score = float(score)
                votes = int(votes)
                ann_scores.append([score, votes, name_english, i, rid])
                i += 1
        ann_scores = self.rank_by_votes(ann_scores)

        self.cur.executemany('update ' + self.table + ' SET ann_score = %s, ann_votes = %s, name_english = %s, ann_score_rank = %s, ann_pop_rank = %s WHERE relate_id = %s',
                             ann_scores)

    def parse_bgm(self, response):
        holders = response.xpath('//ul[@id="browserItemList"]/li')
        host = 'http://bangumi.tv'
        for holder in holders:
            url = holder.xpath('div[@class="inner"]/h3/a/@href').extract()[0]
            rid = self.fetch_id_by_url(host + url, 'bgm_url')
            if rid != -1:
                score = holder.xpath('div[@class="inner"]/p[@class="rateInfo"]/small[@class="fade"]/text()').extract()[0]
                score = float(score)
                votes = holder.xpath('div[@class="inner"]/p[@class="rateInfo"]/span[@class="tip_j"]/text()').extract()[0]
                regGroup = re.search(ur'\((\d+)人评分\)', votes)
                if regGroup is not None:
                    votes = int(regGroup.group(1))
                else:
                    votes = 0

                self.bgm_score.append([score, votes, rid])

    def parse_sati(self, response):
        holders = response.xpath('//table[@class="normal"]/tr[position()>1]')
        pre_url = 'http://www.animesachi.com/visitor/'
        for holder in holders:
            url = holder.xpath('td/a/@href').extract()[0]
            rid = self.fetch_id_by_url(pre_url + url, 'sati_url')
            if rid != -1:
                score = holder.xpath('td[2]/strong/text()').extract()[0]
                score = float(score) / 10
                votes = holder.xpath('td[3]/text()').extract()[0]
                votes = int(votes)

                self.sati_score.append([score, votes, rid])

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

    @staticmethod
    def rank_by_score(scores, i_score=0, i_insert=-1):
        ranked_scores = sorted(scores, key=lambda scores: scores[i_score], reverse=1)
        i = 1
        for ranked_score in ranked_scores:
            ranked_score.insert(i_insert, i)
            i += 1

        return ranked_scores

    @staticmethod
    def rank_by_votes(scores, i_votes=1, i_insert=-1):
        """
        :param scores: 带有分数的插入结构数组
        :param i_votes: 投票人数索引
        :param i_insert: 插入位置索引
        :return: 插入后的新列表
        """
        ranked_scores = sorted(scores, key=lambda votes: votes[i_votes], reverse=1)
        i = 1
        for ranked_score in ranked_scores:
            ranked_score.insert(i_insert, i)
            i += 1

        return ranked_scores

    def closed(self, reason):
        b_s = self.rank_by_score(self.bgm_score)
        b_s = self.rank_by_votes(b_s)
        self.cur.executemany('update ' + self.table + ' SET bgm_score = %s, bgm_votes = %s, bgm_score_rank = %s, bgm_pop_rank = %s WHERE relate_id = %s',
                             b_s)
        s_s = self.rank_by_score(self.sati_score)
        s_s = self.rank_by_votes(s_s)
        self.cur.executemany('update ' + self.table + ' SET sati_score = %s, sati_votes = %s, sati_score_rank = %s, sati_pop_rank = %s WHERE relate_id = %s',
                             s_s)
        self.conn.close()

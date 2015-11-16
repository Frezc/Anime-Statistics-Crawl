# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

'''
from twisted.enterprise import adbapi
import datetime
import MySQLdb.cursors


class MySqlPipeline(object):

    def __init__(self):
        self.dbpool = adbapi.ConnectionPool('MySQLdb',
                                           db='anime_statistics',
                                           user='root',
                                           passwd='a504021398',
                                           cursorclass=MySQLdb.cursors.DictCursor,
                                           charset='utf8',
                                           use_unicode=True)

    def process_item(self, item, spider):
        query = self.dbpool.runInteraction(self._conditional_insert, item)

'''
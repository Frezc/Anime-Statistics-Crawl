# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class AnimeStatisticsItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class ANNAnimeBaseInfo(scrapy.Item):
    url = scrapy.Field()


class ANNAnimeInfo(ANNAnimeBaseInfo):
    name_english = scrapy.Field()
    name_japanese = scrapy.Field()
    # name_korean = scrapy.Field()
    # name_portuguese = scrapy.Field()
    # name_russian = scrapy.Field()
    # name_arabic = scrapy.Field()
    # name_chinese_taiwan = scrapy.Field()
    # name_french = scrapy.Field()
    # name_swedish = scrapy.Field()
    # name_spanish = scrapy.Field()
    # name_polish = scrapy.Field()
    related_anime = scrapy.Field()
    type = scrapy.Field()
    genres = scrapy.Field()
    themes = scrapy.Field()
    objectionable_content = scrapy.Field()
    plot_summary = scrapy.Field()
    running_time = scrapy.Field()
    number_of_episodes = scrapy.Field()
    vintage = scrapy.Field()
    opening = scrapy.Field()
    ending = scrapy.Field()

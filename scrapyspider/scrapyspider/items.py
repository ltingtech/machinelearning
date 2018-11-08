# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ScrapyspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

#定义电影对应的item类
class DoubanMovieItem(scrapy.Item):
	ranking = scrapy.Field()
	movie_name = scrapy.Field()
	score = scrapy.Field()
	score_num = scrapy.Field()


class House58Item(scrapy.Item):
	desc = scrapy.Field()
	'''
	type = scrapy.Field()
	address = scrapy.Field()
	size = scrapy.Field()
	area = scrapy.Field()
	owner = scrapy.Field()
	'''

class TiebaJXNUItem(scrapy.Item):
	reply_count = scrapy.Field()
	title = scrapy.Field()
	#content = scrapy.Field()
	#uname = scrapy.Field()
	#uid = scrapy.Field()

class TiebaItem(scrapy.Item):
	user_info = scrapy.Field()


class BBTQuestionItem(scrapy.Item):
	title = scrapy.Field()
	url = scrapy.Field()
	reply_count = scrapy.Field()
	




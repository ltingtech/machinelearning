# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.exceptions import DropItem
import json
import codecs
from scrapyspider.items import LendPlatformItem
from scrapyspider.items import LendPlatDetailItem
from scrapyspider.items import PlatformDataItem
from scrapyspider.items import platformLevelItem
from scrapyspider.items import platformCoreDataItem
from scrapyspider.items import platformCommerceItem

class ScrapyspiderPipeline(object):
    def process_item(self, item, spider):
        return item

class LendPlatformPipeline(object):
	def __init__(self):
		self.file_1 = codecs.open('../data/lendPlatform.json', 'w', encoding='utf-8')
		self.file_2 = codecs.open('../data/lendPlatformDetail.json', 'w', encoding='utf-8')
		self.file_3 = codecs.open('../data/platformData.json', 'w', encoding='utf-8')
		self.file_4 = codecs.open('../data/platformLevel.json', 'w', encoding='utf-8')
		self.file_5 = codecs.open('../data/platformCoreData.json', 'w', encoding='utf-8')	
		self.file_6 = codecs.open('../data/platformCommerce.json', 'w', encoding='utf-8')
	def process_item(self, item, spider):
		if isinstance(item, LendPlatformItem):
			line = json.dumps(dict(item), encoding="utf-8") + "\n"
			self.file_1.write(line)
			return item	
			#if isinstance(item, LendPlatformItem):
		if isinstance(item, LendPlatDetailItem):
			line = json.dumps(dict(item), encoding="utf-8") + "\n"
			self.file_2.write(line)
			return item
		if isinstance(item, PlatformDataItem):
			line = json.dumps(dict(item), encoding="utf-8") + "\n"
			self.file_3.write(line)
			return item
		if isinstance(item, platformLevelItem):
			line = json.dumps(dict(item), encoding="utf-8") + "\n"
			self.file_4.write(line)
			return item
		if isinstance(item, platformCoreDataItem):
			line = json.dumps(dict(item), encoding="utf-8") + "\n"
			self.file_5.write(line)
			return item
		if isinstance(item, platformCommerceItem):
			line = json.dumps(dict(item), encoding="utf-8") + "\n"
			self.file_6.write(line)
			return item

	def spider_closed(self, spider):
		self.file_1.close()
		self.file_2.close()
		self.file_3.close()
		self.file_4.close()
		self.file_5.close()
		self.file_6.close()
		
		

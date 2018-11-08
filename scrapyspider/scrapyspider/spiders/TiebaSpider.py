#-*-coding:utf-8-*-

from scrapy.spiders import Spider
from scrapyspider.items import TiebaItem
from scrapy import Request
from lxml import etree

class TiebaJXNUSpider(Spider):
	name = "tieba"
	allowed_domains = ['tieba.baidu.com']
	headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36',
    }	

	def start_requests(self):
		url = "https://tieba.baidu.com/f?ie=utf-8&kw=%E9%BB%91%E4%B8%AD%E4%BB%8B&fr=search"
		yield Request(url, headers = self.headers)

	def parse(self, response):
		#调试代码
		from scrapy.shell import inspect_response
		inspect_response(response, self)
		
		#response = response.replace(r'<!--','').replace(r'-->','')
		item = TiebaItem()
		boxs = response.xpath('//li[contains(@class,"j_thread_list")]')
		for box in boxs:
			item['user_info'] = box.xpath('.//@data-field').extract()[0]
			yield item

#-*-coding:utf-8-*-

from scrapy.spiders import Spider
from scrapyspider.items import TiebaJXNUItem
from scrapy import Request
from lxml import etree

class TiebaJXNUSpider(Spider):
	name = "tieba_jxnu"
	headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36',
    }	

	def start_requests(self):
		url = "http://tieba.baidu.com/f?ie=utf-8&kw=%E6%B1%9F%E8%A5%BF%E5%B8%88%E8%8C%83%E5%A4%A7%E5%AD%A6&red_tag=p0533156969"
		yield Request(url, headers = self.headers)

	def parse(self, response):
		#调试代码
		from scrapy.shell import inspect_response
		inspect_response(response, self)
		
		#response = response.replace(r'<!--','').replace(r'-->','')
		item = TiebaJXNUItem()
		#response = response.replace(r'<!--','"').replace(r'-->','"')
		articles = response.xpath('//ul[@class="threadlist_bright j_threadlist_bright"]/li')
		for article in articles:	
			item['reply_count'] = article.xpath('.//div[@class="col2_left j_threadlist_li_left"]/span[@class="threadlist_rep_num center_text"]/text()').extract()[0]
			item['title'] = article.xpath('.//div[@class="threadlist_title pull_left j_th_tit "]/a/text()').extract()[0]
		next_url = response.xpath('//a[@class="next pagination-item "]/@href').extract()	
		if next_url:
			yield Request(next_url, headers=self.headers)

#-*-coding:utf-8-*-

from scrapy import Request
from scrapy.spiders import Spider
from scrapyspider.items import House58Item

class House58Spider(Spider):
	name = 'house58'
	headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36',
    }
	def start_requests(self):
		url = "https://bj.58.com/chuzu/0/?PGTID=0d3090a7-0000-1746-62ae-69658c05dead&ClickID=2"
		yield Request(url, headers=self.headers)
	
	def parse(self, response):
		from scrapy.shell import inspect_response
		inspect_response(response, self)	
	
		item = House58Item()
		houses = response.xpath('//ul[@class="listUl"]/li')
		for house in houses:	
			item['desc'] = house.xpath('.//div[@class="des"]/h2/a/text()').extract()[0].strip()
			yield item
		next_url = response.xpath('//a[@class="next"]/@href').extract()[0]
		if next_url:
			url = next_url + "PGTID=0d3090a7-0000-1a9a-f860-ef8b181ecc56&ClickID=2"
			yield Request(url, headers=self.headers)

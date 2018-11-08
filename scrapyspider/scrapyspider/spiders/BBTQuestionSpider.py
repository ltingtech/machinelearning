#-*- coding:utf-8-*-

from scrapy.spiders import Spider
from scrapyspider.items import BBTQuestionItem
from scrapy import Request
import re

class BBTQuestionSpider(Spider):
	name = "babytree_question"
	headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36',
    }

		
	def start_requests(self):
		url = "http://www.babytree.com/ask/myqa__view~mlist,tab~D,pg~1"
		yield Request(url, headers=self.headers)


	def parse(self, response):
		#from scrapy.shell import inspect_response
		#inspect_response(response, self)
		
		item = BBTQuestionItem()
		solved_questions = response.xpath('//div[contains(@class, "section-main")]/div[@class="question-list question-list-solved"]/ul/li')
		for question in solved_questions:
			item['title'] = question.xpath('.//p[@class="list-title"]/a/text()').extract()[0]
			item['url'] = question.xpath('.//p[@class="list-title"]/a/@href').extract()[0]
			reply_count_str = question.xpath('.//p[@class="list-answer"]/text()').extract()[0]
			num_list = re.findall('\d+', reply_count_str)
			item['reply_count'] = num_list[0]			
			yield item
		curr_pg = question.xpath('//div[@class="pagejump"]/span[@class="current"]/text()').extract()[0]
		curr_pg = int(curr_pg)
		total_pg_str = question.xpath('//div[@class="pagejump"]/span[@class="page-number"]/text()').extract()[0]
		num_list = re.findall('\d+', total_pg_str)
		total_pg= int(num_list[0])
		if (curr_pg < total_pg):
			next_url = "http://www.babytree.com/ask/myqa__view~mlist,tab~D,pg~" + str(curr_pg + 1)
			yield Request(next_url, headers = self.headers)

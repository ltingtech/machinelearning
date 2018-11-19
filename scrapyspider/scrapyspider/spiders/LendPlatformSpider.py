#-*-coding:utf-8-*-


from scrapy.spiders import Spider
from scrapyspider.items import LendPlatformItem
from scrapyspider.items import LendPlatDetailItem
from scrapyspider.items import PlatformDataItem
from scrapyspider.items import platformLevelItem
from scrapy import Request
from scrapyspider.items import platformCoreDataItem
from scrapyspider.items import platformCommerceItem
import re

class LendPlatformSpider(Spider):
	name = "lend_platform"
	
	headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36',
    }
	
	def start_requests(self):
		url = "https://www.wdzj.com/dangan/search?filter"
		yield Request(url, headers = self.headers)
	
	def parse(self, response):
		'''	
		from scrapy.shell import inspect_response
		inspect_response(response, self)
		'''
		company_list = response.xpath('//ul[@class="terraceList"]/li')
		for company in company_list:
			#info_dict = {}
			info_dict = LendPlatformItem()
			name = company.xpath('./div[@class="itemTitle"]/h2/a/text()').extract()[0]
			meta_dict = {}
			meta_dict['name'] = name
			info_dict['company'] = name
			risk_info= company.xpath('./div[@class="itemTitle"]/h2/div/ul/li/text()').extract()
			if len(risk_info) != 0:
				info_dict['company_risk'] = risk_info[0]
			else:
				info_dict['company_risk'] = "正常"
			tag_list = []
			tags = company.xpath('./div[@class="itemTitle"]/div[@class="itemTitleTag tag"]')
			for tag in tags:
				tag_str = tag.xpath('./em/text()').extract()[0]
				tag_list.append(tag_str)
			info_dict['tag_list'] = ",".join(tag_list)
			company_info = company.xpath('./div[@class="itemCon clearfix"]/a[@class="itemConLeft"]/div')
			if len(company_info) == 5 :
				info_dict['interest_rate'] = company_info[0].xpath('./label[@class="biaotag"]/em/text()').extract()[0]
				info_dict['wait_pay_balance'] = company_info[1].xpath('./text()').extract()[0]
				info_dict['online_address'] = company_info[2].xpath('./text()').extract()[0]
				info_dict['online_time'] = company_info[3].xpath('./text()').extract()[0]
				evaluate_list = company_info[4].xpath('./span/text()').extract()
				info_dict['evaluate'] = "@".join(evaluate_list)
				info_dict['total_score'] = company_info[4].xpath('./strong/text()').extract()[0]
				info_dict['reply_count'] = company_info[4].xpath('./em/text()').extract()[0]
				yield info_dict
				#进入下级页面，将上层信息代入
				detail_url = company.xpath('./div[@class="itemTitle"]/h2/a/@href').extract()[0]
				detail_url = response.urljoin(detail_url)
				
				yield Request(detail_url, headers=self.headers, callback=self.parse_detail_page, meta=meta_dict)
			else:
				continue
		next_page = response.xpath('(//div[@class="searchPagelist"]/div[@class="pageList"]/a[@class="pageindex"])[last()]/@currentnum').extract()[0]
		next_url = "https://www.wdzj.com/dangan/search?filter&currentPage=" + next_page
		yield Request(next_url, headers=self.headers)		
						
	def parse_detail_page(self, response):
		'''
		info_dict = response.meta
		item = LendPlatformItem()
		item['company'] = info_dict['company']
		item['company_risk'] = info_dict['company_risk']
		item['tag_list'] = info_dict['tag_list']
		item['interest_rate'] = info_dict['interest_rate']
		item['wait_pay_balance'] = info_dict['wait_pay_balance']
		item['online_address'] = info_dict['online_address']
		item['online_time'] = info_dict['online_time']
		item['evaluate'] = info_dict['evaluate']
		item['total_score'] = info_dict['total_score']
		item['reply_count'] = info_dict['reply_count']
		'''
		#from scrapy.shell import inspect_response
		#inspect_response(response, self)
		
		item = LendPlatDetailItem()	
		item['company'] = response.meta['name']
		company_info = response.xpath('//div[@class="header-da-rt"]/div[@class="left"]/div[@class="pt-info"]/div[@class="box lbor"]')
		item['investment_horizon'] = company_info[1].xpath('./span/b[@class="tab_common_data"]/text()').extract()[0]
		item['yestoday_bargain'] = company_info[3].xpath('./span/b[@class="tab_common_data"]/text()').extract()[0]
		unit = company_info[3].xpath('./span/text()').extract()[0]
		item['yestoday_bargain'] = item['yestoday_bargain'] + unit
		item['yestoday_wait_pay'] = company_info[4].xpath('./span/b[@class="tab_common_data"]/text()').extract()[0]
		unit = company_info[4].xpath('./span/text()').extract()[0]
		item['yestoday_wait_pay'] = item['yestoday_wait_pay'] + unit
		desc_list = response.xpath('//div[@class="bgbox-bt zzfwbox"]/dl')
		resource = desc_list[0].xpath('./dd')
		item['registered_fund'] = resource[0].xpath('./div[@class="r"]/text()').extract()[0].strip()
		item['bank_depository'] = resource[1].xpath('./div[@class="r"]/text()').extract()[0].strip()
		item['invest_record'] = resource[2].xpath('./div[@class="r"]/text()').extract()[0].strip()
		item['association'] = resource[3].xpath('./div[@class="r"]/text()').extract()[0].strip()
		item['ICP'] = resource[4].xpath('./div[@class="r"]/text()').extract()[0].strip()

		service = desc_list[1].xpath('./dd')
		item['automatic_bid'] = service[0].xpath('./div[@class="r"]/text()').extract()[0].strip()
		item['debt_transform'] = service[1].xpath('./div[@class="r"]/text()').extract()[0].strip()
		item['bid_guarantee'] = service[2].xpath('./div[@class="r"]/text()').extract()[0].strip()
		item['guarantee_model'] = service[3].xpath('./div[@class="r"]/text()').extract()[0].strip() 
				

		#高管列表
		#management_list = response.xpath('//ul[@class="gglist"]/li')
		introduce_map = {}
		introduce_list = response.xpath('//div[@class="da-ggjj"]/div')
		gg_list = []
		if len(introduce_list) > 0:
			management_list = introduce_list[0].xpath('./ul[@class="gglist"]/li')
			del introduce_list[0]
			for introduce in introduce_list:
				name = introduce.xpath('./div/b[@class="name"]/text()').extract()[0]
				introduce_map[name] = {}
				img = introduce.xpath('./img[@class="img"]/@src').extract()[0]
				profile = introduce.xpath('./div/p[@class="cen"]/text()').extract()[0]
				introduce_map[name]['img'] = img
				introduce_map[name]['profile'] = profile 
			for managementor in management_list:
				name = managementor.xpath('./a/span/text()').extract()[0]
				job_title = managementor.xpath('./a/p/text()').extract()[0]
				introduce_map[name]['job_title'] = job_title.strip()
			item['managementor'] = introduce_map
		yield item

		#平台数据
		
		platform_fee_list = response.xpath('//div[@class="tab-cont"]/div')
		platform_fee = platform_fee_list[2]
		fee_list = platform_fee.xpath('./div[@class="da-ptfy"]/dl')
		if len(fee_list) == 5:
			fee_item = PlatformDataItem()
			fee_item['company'] = response.meta['name']
			fee_item['admin_expense'] = fee_list[0].xpath('./dt/em/text()').extract()[0].strip()
			fee_item['withdraw_expense'] = fee_list[1].xpath('./dt/em/text()').extract()[0].strip()
			fee_item['recharge_expense'] = fee_list[2].xpath('./dt/em/text()').extract()[0].strip()
			fee_item['transfer_expense'] = fee_list[3].xpath('./dt/em/text()').extract()[0].strip()
			fee_item['vip_expense'] = fee_list[4].xpath('./dt/em/text()').extract()[0].strip()	
			yield fee_item

		#解析评级页面
		tab_list = response.xpath('//div[@class="common-header-nav"]/a')
		for tab in tab_list:	
			next_url = tab.xpath('./@href').extract()[0].strip()
			if re.match('.*shuju', next_url):
				next_url = "http:" + next_url
				yield Request(next_url, headers=self.headers, callback=self.parse_data, meta=response.meta)
			if re.match('.*pingji', next_url):
				next_url = "http:" + next_url
				#next_url = tab.xpath('./@href').extract()[0]
				yield Request(next_url, headers=self.headers, callback=self.parse_level, meta=response.meta)
			if re.match('.*gongshang', next_url):
				next_url = "http:" + next_url
				#next_url = tab.xpath('./@href').extract()[0]
				yield Request(next_url, headers=self.headers, callback=self.parse_commerce, meta=response.meta)
				


	#解析评级数据
	def parse_level(self, response):
		#from scrapy.shell import inspect_response
		#inspect_response(response, self)

		item = platformLevelItem()
		item['company'] = response.meta['name']
		#level_data = response.xpath('//div[@class="detail-radar clearfix"]/div[@class="fr"]/div')
		#explain_word = level_data[0].xpath('./span')
		#item['develop_index'] = explain_word[0].xpath('./text()').extract()[0]
		#item['level_rank'] = expain_word[0].xpath('./text()').extract()[0]
		score_data =  response.xpath('//div[@class="detail-radar clearfix"]/div[@class="fr"]/ul')
		score_list = score_data[0].xpath('./li')
		item['turnover_score'] = score_list[0].xpath('./div[@class="rate-data"]/text()').extract()[0].strip()
		item['person_score'] = score_list[1].xpath('./div[@class="rate-data"]/text()').extract()[0].strip()
		item['tech_score'] = score_list[2].xpath('./div[@class="rate-data"]/text()').extract()[0].strip()
		item['criterion_score'] = score_list[3].xpath('./div[@class="rate-data"]/text()').extract()[0].strip()
		item['pry_score'] = score_list[4].xpath('./div[@class="rate-data"]/text()').extract()[0].strip()		
		score_list = score_data[1].xpath('./li')
		item['pinpai_score'] = score_list[0].xpath('./div[@class="rate-data"]/text()').extract()[0].strip()
		item['transparent_score'] = score_list[1].xpath('./div[@class="rate-data"]/text()').extract()[0].strip()
		item['scatter_score'] = score_list[2].xpath('./div[@class="rate-data"]/text()').extract()[0].strip()
		item['liquidity_score'] = score_list[3].xpath('./div[@class="rate-data"]/text()').extract()[0].strip()
		yield item


	#解析数据
	def parse_data(self, response):
		
		#from scrapy.shell import inspect_response
		#inspect_response(response, self)

		item = platformCoreDataItem()
		item['company'] = response.meta['name']
		core_data = response.xpath('//div[@class="detail-radar clearfix"]/div[@class="fr"]/ul')
		item['turnover'] = core_data[0].xpath('./li[position()=1]/div[position()=1]/text()').extract()[0].strip()
		item['wait_pay'] = core_data[0].xpath('./li[position()=2]/div[position()=1]/text()').extract()[0].strip()
		item['interest'] = core_data[0].xpath('./li[position()=3]/div[position()=1]/text()').extract()[0].strip()
		item['mean_period'] = core_data[0].xpath('./li[position()=4]/div[position()=1]/text()').extract()[0].strip()
		item['inverst_person'] = core_data[0].xpath('./li[position()=5]/div[position()=1]/text()').extract()[0].strip()
		item['mean_invest'] = core_data[1].xpath('./li[position()=1]/div[position()=1]/text()').extract()[0].strip()
		item['wait_invest'] = core_data[1].xpath('./li[position()=2]/div[position()=1]/text()').extract()[0].strip()
		item['lend_count'] = core_data[1].xpath('./li[position()=3]/div[position()=1]/text()').extract()[0].strip()
		item['mean_lend'] = core_data[1].xpath('./li[position()=4]/div[position()=1]/text()').extract()[0].strip()
		item['lend_biaoshu'] = core_data[1].xpath('./li[position()=5]/div[position()=1]/text()').extract()[0].strip()
		item['wait_pay_lend'] = core_data[2].xpath('./li[position()=1]/div[position()=1]/text()').extract()[0].strip()

		yield item

	#解析工商备案
	def parse_commerce(self, response):
		item = platformCommerceItem()
		
		#from scrapy.shell import inspect_response
		#inspect_response(response, self)
		
		item['company'] = response.meta['name']
		
		commerce_info = response.xpath('//div[@class="gs-box"]/div[@class="left"]/div[@class="lcen"]/table/tr')
		item['name'] = commerce_info[0].xpath('./td[position()=2]/text()').extract()[0].strip()
		item['social_code'] = commerce_info[0].xpath('./td[position()=4]/text()').extract()[0].strip()
		
		item['owner'] = commerce_info[1].xpath('./td[position()=2]/text()').extract()[0].strip()
		item['register_fund'] = commerce_info[1].xpath('./td[position()=4]/text()').extract()[0].strip()
		item['category'] = commerce_info[2].xpath('./td[position()=2]/text()').extract()[0].strip()
		item['fund_fact'] = commerce_info[2].xpath('./td[position()=4]/text()').extract()[0].strip()
		item['register_addr'] = commerce_info[3].xpath('./td[position()=2]/text()').extract()[0].strip()
		item['open_time'] = commerce_info[3].xpath('./td[position()=4]/text()').extract()[0].strip()
		item['register_status'] = commerce_info[4].xpath('./td[position()=2]/text()').extract()[0].strip()
		item['deadline'] = commerce_info[4].xpath('./td[position()=4]/text()').extract()[0].strip()
		item['register_location'] = commerce_info[5].xpath('./td[position()=2]/text()').extract()[0].strip()
		item['audit_time'] = commerce_info[5].xpath('./td[position()=4]/text()').extract()[0].strip()
		item['copy_domain'] = commerce_info[6].xpath('./td[position()=2]/text()').extract()[0].strip()
		item['copy_time'] = commerce_info[6].xpath('./td[position()=4]/text()').extract()[0].strip()
		
		item['copy_location'] = commerce_info[7].xpath('./td[position()=2]/text()').extract()[0].strip()
		item['copy_quantity'] = commerce_info[7].xpath('./td[position()=4]/text()').extract()[0].strip()
		item['ICP'] = commerce_info[8].xpath('./td[position()=2]/text()').extract()[0].strip()
		item['ICP_certificate'] = commerce_info[8].xpath('./td[position()=4]/text()').extract()[0].strip()
		old_name = commerce_info[9].xpath('./td[position()=2]/text()').extract()
		if len(old_name) > 0:
			item['old_name'] = old_name[0].strip()	
		else:
			item['old_name'] = ""
		item['bussiness_scope'] = commerce_info[10].xpath('./td[position()=2]/p/text()').extract()[0].strip()
		
		#股权信息
		shareholder_list = response.xpath('//div[@id="gqInfoBox"]/div[@class="table-ic-box"]/table[@class="table-ic"]/tbody[@class="tbody"]/tr')
		shareholder_res = []
		for holder in shareholder_list:
			info = {}
			info['name'] = holder.xpath('./td[position()=1]/text()').extract()[0].strip()
			info['percent'] = holder.xpath('./td[position()=2]/text()').extract()[0].strip()
			info['fund'] = holder.xpath('./td[position()=3]/text()').extract()[0].strip()
			shareholder_res.append(info)
		item['shareholder'] = shareholder_res
		
		#变更记录
		gq_box = response.xpath('//div[@class="gq-box"]')
		if len(gq_box) >= 3 :
			if len(gq_box) == 3:
				manage_change = gq_box[1]
			else:	
				manage_change = gq_box[2]
			change_detail = manage_change.xpath('./div[@class="table-ic-box"]/table[@class="table-ic"]/tbody[@class="tbody"]/tr')
			change_res = []
			for change in change_detail:
				info_ele = {}
				info_ele['time'] = change.xpath('./td[position()=1]/text()').extract()[0].strip()
				info_ele['type'] = change.xpath('./td[position()=2]/text()').extract()[0].strip()
				info_ele['before'] = change.xpath('./td[position()=3]/text()').extract()[0].strip()
				info_ele['after'] = change.xpath('./td[position()=4]/text()').extract()[0].strip()
				change_res.append(info_ele)
				'''	
				from scrapy.shell import inspect_response
				inspect_response(response, self)
				'''
			item['manage_change'] = change_res
			abnormal_manage = []
			if len(gq_box) == 3:
				abnormal_record = gq_box[2]
			else:	
				abnormal_record = gq_box[3]
			change_detail = abnormal_record.xpath('./div[@class="table-ic-box"]/table[@class="table-ic"]/tbody[@class="tbody"]/tr')
			for change in change_detail:
				element = {}
				td_list = change.xpath('./td')
				if len(td_list) < 7:
					continue
				else :
					element['cause'] = td_list[1].xpath('./text()').extract()[0].strip()
					element['time'] = td_list[2].xpath('./text()').extract()[0].strip()
					element['input_dec_loc'] = td_list[3].xpath('./text()').extract()[0].strip()
					element['remove_cause'] = td_list[4].xpath('./text()').extract()[0].strip()
					element['remove_time'] = td_list[5].xpath('./text()').extract()[0].strip()
					element['rem_dec_loc'] = td_list[6].xpath('./text()').extract()[0].strip()
					abnormal_manage.append(element)
		
			item['abnormal_management'] = abnormal_manage
		else:
			item['manage_change'] = []
			item['abnormal_management'] = []
	
		yield item














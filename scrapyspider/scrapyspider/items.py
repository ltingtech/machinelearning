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

class LendPlatformItem(scrapy.Item):
	company = scrapy.Field()  #公司名称
	company_risk = scrapy.Field() #风险预警
	tag_list = scrapy.Field()  #公司标签
	interest_rate = scrapy.Field()  # 参考利率
	wait_pay_balance = scrapy.Field() #待还款金额 
	online_time = scrapy.Field() #上线时间
	online_address = scrapy.Field() #上线地址
	evaluate = scrapy.Field()	   #网友印象
	total_score = scrapy.Field()   #综合评价
	reply_count = scrapy.Field()   #用户点评数
	#investment_horizon = scrapy.Field() # 投资周期
	#reply_score = scrapy.Field()       #用户点评得分
	#yestoday_bargain = scrapy.Field()  #昨日成交量
	#yestoday_wait_pay = scrapy.Field()  #昨日待还金额

class LendPlatDetailItem(scrapy.Item):
	company = scrapy.Field()
	investment_horizon = scrapy.Field() # 投资周期
	yestoday_bargain = scrapy.Field()  #昨日成交量
	yestoday_wait_pay = scrapy.Field()  #昨日待还金额
	registered_fund = scrapy.Field()  #注册资金
	automatic_bid = scrapy.Field()  #自动投标
	bank_depository = scrapy.Field()  #	银行存管
	debt_transform = scrapy.Field() #债权转让
	invest_record = scrapy.Field() #融资记录
	bid_guarantee = scrapy.Field() #投标保障
	association = scrapy.Field() #监管协会
	guarantee_model = scrapy.Field() #保障模式
	ICP = scrapy.Field()	 #ICP
	managementor = scrapy.Field()  # 高管

class PlatformDataItem(scrapy.Item):
	company = scrapy.Field()
	admin_expense = scrapy.Field()
	withdraw_expense = scrapy.Field()
	recharge_expense = scrapy.Field()
	transfer_expense = scrapy.Field()
	vip_expense = scrapy.Field()
	

class platformLevelItem(scrapy.Item):
	company = scrapy.Field()
	#develop_index = scrapy.Field()
	#level_rank = scrapy.Field()
	turnover_score = scrapy.Field()
	person_score = scrapy.Field()
	tech_score = scrapy.Field()
	criterion_score = scrapy.Field()
	pry_score = scrapy.Field()
	pinpai_score = scrapy.Field()
	transparent_score = scrapy.Field()
	scatter_score = scrapy.Field()
	liquidity_score = scrapy.Field()

class platformCoreDataItem(scrapy.Item):
	company = scrapy.Field()
	turnover = scrapy.Field()
	wait_pay = scrapy.Field()
	interest = scrapy.Field()
	mean_period = scrapy.Field()
	inverst_person = scrapy.Field()
	mean_invest = scrapy.Field()
	wait_invest = scrapy.Field()
	lend_count = scrapy.Field()
	mean_lend = scrapy.Field()
	lend_biaoshu = scrapy.Field()
	wait_pay_lend = scrapy.Field()

class platformCommerceItem(scrapy.Item):
	company = scrapy.Field()
	name = scrapy.Field()
	social_code = scrapy.Field()
	owner = scrapy.Field()
	register_fund = scrapy.Field()
	category = scrapy.Field()
	fund_fact = scrapy.Field()
	register_addr = scrapy.Field()
	open_time = scrapy.Field()
	register_status = scrapy.Field()
	deadline = scrapy.Field()
	register_location = scrapy.Field()
	audit_time = scrapy.Field()
	copy_domain = scrapy.Field()
	copy_time = scrapy.Field()
	copy_location = scrapy.Field()
	copy_quantity = scrapy.Field()
	ICP = scrapy.Field()
	ICP_certificate = scrapy.Field()
	old_name = scrapy.Field()
	bussiness_scope = scrapy.Field()
	shareholder = scrapy.Field()
	manage_change = scrapy.Field()
	abnormal_management = scrapy.Field()
	













	







	




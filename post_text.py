# -*- coding: utf-8 -*-
# @Author: lim
# @Email: 940711277@qq.com
# @Date:  2017-11-21 17:46:13
# @Last Modified by:  lim
# @Last Modified time:  2017-11-21 18:03:19
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import time
import random
import requests
from lxml import etree
from config import NAME, PASSWORD, userId


def qiushibaike():
	"""get a text to post"""
	url = "https://www.qiushibaike.com/"
	headers = {
		"Host":"www.qiushibaike.com",
		"Connection":"keep-alive",
		"Cache-Control":"max-age=0",
		"User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36",
		"Upgrade-Insecure-Requests":"1",
		"Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
		"Accept-Encoding":"gzip, deflate, br",
		"Accept-Language":"zh-CN,zh;q=0.9",
		}
	try:
		r = requests.get(url,headers=headers)
		if r.status_code == 200 and len(r.text)>10000:
			textList = []
			page = r.text
			xml = etree.HTML(page)
			itemList = xml.xpath("//div[@id='content']/div/div[@id='content-left']/div//div[@class='content']")
			for item in itemList:		
				text = item.xpath('string(.)')
				text = text.replace(' ','').replace('\n','').replace('\t','').replace('\n\t','').strip()
				textList.append(text)
			return textList
		else:
			print('get a error')
			return ['Sorry everyone,there are some problem.The new piece is coming soon---A tiny robot belong to lim---.']
	except:		
		print('get a error')
		return ['Sorry everyone,there are some problem.The new piece is coming soon---A tiny robot belong to lim---.']



def main(userId):
	"""to crawl piece to my weibo"""
	headers = {
	"Host":"weibo.com",
	"Connection":"keep-alive",
	"Content-Length":"158",
	"Origin":"https://weibo.com",
	"X-Requested-With":"XMLHttpRequest",
	"User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36",
	"Content-Type":"application/x-www-form-urlencoded",
	"Referer":"https://weibo.com/{}/home".format(userId),
	"Accept":"*/*",
	"Accept-Encoding":"gzip, deflate, br",
	}

	while True:
		with open('cookies.txt') as f:
			con = f.read()
		cookies = eval(con)
		url = 'https://weibo.com/aj/mblog/add?ajwvr=6&__rnd={}'.format(int(1000*time.time()))
		text_list = qiushibaike()
		if len(text_list)>1:
			n = 50
			while True:
				text = random.choice(text_list)
				if len(text)>20:
					break
				n-=1
				if n==0:
					text='Sorry everyone,there are some problem.The new piece is coming soon'
					break
			text = text + '---A tiny robot belong to lim---'
		else:
			text = text_list[0]
		data = {
		"location":"v6_content_home",
		"text":text,
		"appkey":"",
		"style_type":"1",
		"pic_id":"",
		"tid":"",
		"pdetail":"",
		"rank":"0",
		"rankid":"",
		"module":"stissue",
		"pub_source":"main_",
		"pub_type":"dialog",
		"isPri":"0",
		"_t":"0",	
		}
		r = requests.post(url =url,headers=headers,cookies=cookies,data=data)
		if r.status_code == 200:
			print ('post success')
		else:
			print ('---something wrong ,now going to flush cookies---')
			content = do_login(NAME, PASSWORD)
			with open('cookies.txt','w') as f:
				f.write(str(content))
		time.sleep(1800)


if __name__ == '__main__':
	main(userId)
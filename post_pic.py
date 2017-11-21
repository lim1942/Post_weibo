# -*- coding: utf-8 -*-
# @Author: lim
# @Email: 940711277@qq.com
# @Date:  2017-11-21 14:06:40
# @Last Modified by:  lim
# @Last Modified time:  2017-11-21 18:01:01

import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import requests
import time
import base64
from config import NAME, PASSWORD, userId, userName

F = open('text.txt')
G = open('pic_url.txt')

def post_msg(userId,text,pic_id):
	"""to crawl piece to my weibo"""

	url = 'https://weibo.com/aj/mblog/add?ajwvr=6&__rnd={}'.format(int(1000*time.time()))

	headers = {
	"Host":"weibo.com",
	"Connection":"keep-alive",
	"Content-Length":"158",
	"Origin":"https://weibo.com",
	"X-Requested-With":"XMLHttpRequest",
	"User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36",
	"Content-Type":"application/x-www-form-urlencoded",
	"Referer":"https://weibo.com/u/{}/home".format(userId),
	"Accept":"*/*",
	"Accept-Encoding":"gzip, deflate, br",
	}

	with open('cookies.txt') as f:
		con = f.read()
	cookies = eval(con)

	data = {
	"location":"v6_content_home",
	"text":text,
	"appkey":"",
	"style_type":"1",
	"pic_id":pic_id,
	"tid":"",
	"pdetail":"",
	"gif_ids":'',
	"rank":"0",
	"rankid":"",
	"module":"stissue",
	"pub_source":"main_",
	"updata_img_num":"1",
	"pub_type":"dialog",
	"isPri":"0",
	"_t":"0",	
	}

	r = requests.post(url =url,headers=headers,cookies=cookies,data=data)
	if r.status_code == 200:
		print ('post success')
	else:
		print( '---something wrong ,now going to flush cookies---')
		content = do_login(NAME, PASSWORD)
		with open('cookies.txt','w') as f:
			f.write(str(content))



def get_text():
	try:
		con = F.readline().replace('\n','')+'---by几米'
		return con
	except:
		return 'something wrong,process can not get a text to post,so sorry!'


def get_pic_id(userId,userName):
	"""upload to picture to weibo server get to pic_id to post msg"""

	headers = {
	"Host":"weibo.com",
	"Connection":"keep-alive",
	"Origin":"https://weibo.com",
	"X-Requested-With":"XMLHttpRequest",
	"User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36",
	"Content-Type":"application/x-www-form-urlencoded",
	"Referer":"https://weibo.com/u/{}/home".format(userId),
	"Accept":"*/*",
	"Accept-Encoding":"gzip, deflate, br",
	}

	with open('cookies.txt') as f:
		con = f.read()
	cookies = eval(con)

	try:
		url = G.readline().replace('\n','')
		r = requests.get(url)
		if r.status_code == 200:
			content = r.content
		else:
			with open('b.jpg','rb') as f:
				content = f.read()
	except:
		with open('b.jpg','rb') as f:
				content = f.read()	

	b64_data = base64.b64encode(content)
	data = {'b64_data':b64_data}
	url = 'https://picupload.weibo.com/interface/pic_upload.php?cb=https%3A%2F%2Fweibo.com%2Faj%2Fstatic%2Fupimgback.html%3F_wv%3D5%26callback%3DSTK_ijax_{}&mime=image%2Fjpeg&data=base64&url=weibo.com%2Fu%2F{}&markpos=1&logo=1&nick=%40lim{}&marks=0&app=miniblog&s=rdxt&pri=0&file_source=1'
	url = url.format(str(int(time.time()*1000000)),userId,userName)	

	try:
		r = requests.post(url=url,headers=headers,cookies=cookies,data=data)
		if r.status_code == 200:
			pid = r.url.split('pid=')[-1]
		else:
			pid = '006OKj2Ggy1flptapxdyvj30zk0sg1kx'
		return pid
	except:
		return '006OKj2Ggy1flptapxdyvj30zk0sg1kx'


def main():
	while True:
		text = get_text()
		pid = get_pic_id(userId,userName)
		print('get a pid')
		post_msg(userId,text,pid)
		time.sleep(2400)


if __name__ == '__main__':
	main()

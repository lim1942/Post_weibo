# -*- coding: utf-8 -*-
# @Author: lim
# @Date:   2017-11-06 22:19:18
# @Last Modified by:   lim
# @Last Modified time:  2017-11-21 18:05:57
import time
import re
import base64
import rsa
import requests
import binascii
from urllib import quote_plus


headers = {
	# "Host":"login.sina.com.cn",
	"Connection":"keep-alive",
	"User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36",
	"Accept":"*/*",
	"Accept-Encoding":"gzip, deflate, br",
	"Accept-Language":"zh-CN,zh;q=0.9",
	}


def get_encodename(name):
    """name must be string"""
    username_quote = quote_plus(str(name))
    username_base64 = base64.b64encode(username_quote.encode("utf-8"))
    return username_base64.decode("utf-8")


def get_password(password, servertime, nonce, pubkey):
	"""get a encrypt password"""
	rsa_publickey = int(pubkey, 16)
	key = rsa.PublicKey(rsa_publickey, 65537)
	message = str(servertime) + '\t' + str(nonce) + '\n' + str(password)
	passwd = rsa.encrypt(message, key)
	passwd = binascii.b2a_hex(passwd)
	return passwd


def get_server_data(su):
	"""prelogin to get some fields"""
	pre_url = "https://login.sina.com.cn/sso/prelogin.php?entry=weibo&callback=sinaSSOController.preloginCallBack&su="
	pre_url = pre_url + su + "&rsakt=mod&checkpin=1&client=ssologin.js(v1.4.19)&_="
	prelogin_url = pre_url + str(int(time.time() * 1000))
	pre_data_res = requests.get(prelogin_url, headers=headers)

	sever_data = eval(pre_data_res.content.decode("utf-8").replace("sinaSSOController.preloginCallBack", ''))
	return sever_data



def get_redirect(name, data, post_url,session):
	"""get the redirect url for get the cookies"""
	
	logining_page = session.post(post_url, data=data, headers=headers)
	login_loop = logining_page.content.decode("GBK")
	if 'retcode=101' in login_loop:
	    return ''

	if 'retcode=2070' in login_loop:
	    return 'pinerror'

	if 'retcode=4049' in login_loop:
	    return 'login_need_pincode'


	pa = r'location\.replace\([\'"](.*?)[\'"]\)'
	return re.findall(pa, login_loop)[0]



def login_no_pincode(name, password, server_data,session):
	"""real login first times"""
	post_url = 'https://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.19)'

	servertime = server_data["servertime"]
	nonce = server_data['nonce']
	rsakv = server_data["rsakv"]
	pubkey = server_data["pubkey"]
	sp = get_password(password, servertime, nonce, pubkey)

	data = {
	'encoding': 'UTF-8',
	'entry': 'weibo',
	'from': '',
	'gateway': '1',
	'nonce': nonce,
	'pagerefer': "",
	'prelt': 173,
	'pwencode': 'rsa2',
	"returntype": "META",
	'rsakv': rsakv,
	'savestate': '7',
	'servertime': servertime,
	'service': 'miniblog',
	'sp': sp,
	'sr': '1366*768',
	'su': get_encodename(name),
	'useticket': '1',
	'vsnf': '1',
	'url': 'https://weibo.com/ajaxlogin.php?framelogin=1&callback=parent.sinaSSOController.feedBackUrlCallBack'
	}

	rs = get_redirect(name, data, post_url,session)
	return rs




def do_login(name,password):
	"""func to dispatch"""
	session = requests.Session()
	su = get_encodename(name)
	server_data = get_server_data(su)
	if server_data['showpin']:
		print ("login need pincode")
	else:
		rs = login_no_pincode(name, password, server_data,session)
		r = session.get(rs,headers=headers)
		return session.cookies.get_dict()


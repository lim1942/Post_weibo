# -*- coding: utf-8 -*-
# @Author: lim
# @Email: 940711277@qq.com
# @Date:  2017-11-20 19:23:37
# @Last Modified by:  lim
# @Last Modified time:  2017-11-21 18:29:04

import time
from login import do_login
from config import NAME, PASSWORD

while True:
	print ('--process to flush cookies--')
	content = do_login(NAME, PASSWORD)
	with open('cookies.txt','w') as f:
		f.write(str(content))
	time.sleep(82800)
	print ('--flush cookies successful--')
	# break
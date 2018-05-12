# -*- coding=UTF-8 -*-
# python2.7
# pip install requests
# pip install lxml
# pip install BeautifulSoup

# 说明：当遇到不懂的词语，通过终端启用该脚本可以快速翻译，并且自动记录下来形成一个个人专属的生词库。
#  支持多字典切换。

import requests, lxml, re
from bs4 import BeautifulSoup

# 写入文件
def add_word(word):

	with open('dic.txt', 'a') as fw:
			fw.write(word)

# 验证是否重复
def search_same_word(word):
	try:
		with open('dic.txt', 'r') as fr:
			for words in fr:
				if word == words:
					print '-- Already exists...'
					return False
					break
			else:
				return True
	except:
		# 创建 utf-8 的文件
		with open('dic.txt', 'a') as fw:
			fw.write('')
		with open('dic.txt', 'r') as fr:
			for words in fr:
				if word == words:
					print '-- It maybe has some mistakes...'
					return False
					break
			else:
				return True

# 多词典切换
def dic_switch(word):
	while True:
		if you_dao(word) == False:
			if bai_du(word) == False:
				continue
			else:
				break
		else:
			break

# 有道词典
def you_dao(word):

	# 网址构造
	youdao_url = 'http://dict.youdao.com/w/' + word + '/#keyfrom=dict.top'

	# 定制请求头
	yd_headers = {
		'User-Agent' : 'Mozilla/5.0 (Android; Mobile; rv:14.0) Gecko/14.0 Firefox/14.0',
  	  	'Referer':'http://dict.youdao.com'
	}

	try:

		r = requests.get(youdao_url, headers = yd_headers, timeout = 3)
		html = BeautifulSoup(r.text, "lxml")

		for conten in html.find_all("div", class_="trans-wrapper clearfix"):
			j = conten.find_all("ul")
			soup = BeautifulSoup(str(j), "lxml")

			# 解码二进制的字符串
			translate = soup.get_text("", strip = True).decode('unicode-escape')  + '\n'
		
			print translate
			word = word + "\n"
			if search_same_word(word) == True:
				add_word(word)
				# 用 utf-8 编码
				add_word(translate.encode('utf-8'))
				add_word('\n')
				return True
				break

	except Exception, e: # 第一个异常处理
		return False


# 百度词典
def bai_du(word):
	# 网址构造
	baidu_url = 'http://dict.baidu.com/s?wd=' + word
	# 定制请求头
	bd_headers = {
		'User-Agent' : 'Mozilla/5.0 (Android; Mobile; rv:14.0) Gecko/14.0 Firefox/14.0',
	  	'Referer':'http://dict.baidu.com'
	}

	# 抓取网页
	try:

		r = requests.get(baidu_url, headers = bd_headers, timeout = 3)
		html = BeautifulSoup(r.text, "lxml")

		for conten in html.find_all("div", class_="en-mean"):
			j = conten.find_all("div")
			soup = BeautifulSoup(str(j), "lxml")
			# 解码乱码的字符串
			translate = soup.get_text("\n", strip = True).decode('unicode-escape')  + '\n' 
			translate = re.sub(re.compile("\.\\n"), ". ", translate)
			print translate
			word = word + "\n"
			if search_same_word(word) == True:
				add_word(word)
				# 用 utf-8 编码
				add_word(translate.encode('utf-8'))
				add_word('\n')
				return True
				break

	except Exception, e:
		return False

# 循环执行
while True:

	print '-- Please input a english word:'

	word = str(raw_input('>> '))

	if word == "@":
		pass
	elif "#" in word:
		# 先用 gb2312 解码，再用 utf-8 编码
		# gb2312，gbk，big5等要转换为utf8，则要先到（decode）unicode，再到（encode）utf8
		word = word.decode("gbk") + '\n'
		add_word(word.encode('utf-8'))
	else:
		dic_switch(word)

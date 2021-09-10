"""
1、利用爬虫爬取ID网站信息
2、利用正则匹配出ID
3、把不同的ID写入一个字符串，或者首先保存在一个文件
4、把字符串(或文件)写入Windows配置文本
5、如果可能，操纵CMD执行刷新指令
6、CMD能直接运行该程序(即快捷方式)
"""

import re
from urllib import request 
import threading
import time
import os

class ChangeId(object):
	def __init__(self, url_dict):
		self.url_dict = url_dict
		self.string = ''

	def get_id(self):
	
		for id_url, web_name in self.url_dict.items():
			response_data = request.urlopen(id_url)
			response_txt = response_data.read().decode('utf-8') # 不加decode会出现cannot use a string pattern on a bytes-like object
			id_list = re.findall('<a href=\"https://www\.ipaddress\.com/ipv4/(.*?)">', response_txt)
			id_list_length = int(len(id_list)/2)  # 不知道为什么用re.findall()会重复值，所以只能用这个笨方法把重复的去掉

			for i in range(id_list_length):
				str_1 = str(id_list[i] + web_name)
				self.string +=str_1 + '\n'
		self.string = '\n\n# GitHub Start \n' + self.string +'# GitHub End \n'

	def cnf_file(self):

		with open(r'C:\Windows\System32\drivers\etc\hosts', 'r') as f:

			file_txt = f.read()
			txt = re.search('# GitHub Start ([\s\S]*)# GitHub End', file_txt )  # 本来想用更牛逼的办法去替换的，所以用了正则
			txt = txt.group()

	
		with open(r'C:\Windows\System32\drivers\etc\hosts', 'a') as f_1:  # 每次写成'w'，txt的内容就给我整没了

			loc = file_txt.find(txt)
			f_1.seek(loc)
			f_1.truncate()
			f_1.write(self.string)
		
		print('修改完成')


	def start(self):

		thread = threading.Thread(target=self.get_id)
		thread.start()
		thread.join()


if __name__ == '__main__':
	
	url_dict = {
	'https://github.com.ipaddress.com/':'github.com',
	'https://fastly.net.ipaddress.com/github.global.ssl.fastly.net':'github.global.ssl.fastly.net',
	'https://github.com.ipaddress.com/assets-cdn.github.com':'assets-cdn.github.com'
	}
	changeid = ChangeId(url_dict)
	changeid.start()
	changeid.cnf_file()
	os.system('ipconfig /flushdns')



# -*- coding: UTF-8 -*-
import string

import requests
import Mysql
from bs4 import BeautifulSoup

url = "https://apkpure.com"
proxies = {'https': "SOCKS5://127.0.0.1:1080"}


def get_soup(arg):
	request = requests.get(url + arg, proxies=proxies, timeout=1)
	soup = BeautifulSoup(request.text, "html.parser")
	return soup


def get_categorys():
	tags = get_soup("/app").find_all("ul", class_="index-category cicon")
	for tag in tags:
		for link in tag.find_all("a"):
			Mysql.insert_category(link.attrs['href'])


def get_detail_page(arg):
	for i in range(10):
		if Mysql.search_apks(arg, i + 1) < 10:
			try:
				tags = get_soup(arg + "?page=" + str(i + 1)).find_all("div", class_="category-template-title")
				for tag in tags:
					for link in tag.find_all("a"):
						Mysql.insert_apks(arg, i + 1, link.attrs['href'])
			except Exception, e:
				print e


def get_detail_apk(arg):
	try:
		html = get_soup(arg)
		tag = html.find("span", itemprop="fileSize")
		if tag is None:
			tag = html.find("span", class_="fsize")
		str_size = tag.text.split(" ")[0]
		if str_size[0:1] == "(":
			str_size = str_size[1:]
			print str_size
		size = string.atof(str_size)

		if tag.text.split(" ")[1] == "KB":
			size /= 1024
		if tag.text.split(" ")[1] == "GB":
			size *= 1024

		is_google = 0
		button = html.find_all("a", class_="ga")[1]
		link = button.attrs['href'].split("?")[0]
		if link == "https://play.google.com/store/apps/details":
			is_google = 1

		Mysql.update_apk_size(arg, size, is_google)
	except Exception, e:
		print e


def get_download_link(arg):
	try:
		html = get_soup(arg + "/download?from=details")
		Mysql.update_apk_link(arg, html.find("a", id="download_link").attrs["href"])
	except Exception, e:
		print e

if __name__ == "__main__":
	# 爬取分类信息
	# get_categorys()
	# 根据分类信息爬取 apk 名字与连接
	# categorys = Mysql.get_all_categorys()
	# for category in categorys:
	#	 get_detail_page(category)
	# 根据 url 爬取 apk 文件的大小、来源
	# apks = Mysql.get_no_size_apks()
	# for apk in apks:
	#	get_detail_apk(apk)
	# 根据 url 爬取 apk 的下载链接
	# apks = Mysql.get_no_link_apks()
	# for apk in apks:
	#	get_download_link(apk)
	# 获取所有文件大小满足所传入参数的 apk 的下载链接 5079
	apks = Mysql.get_all_download_link(0, 25)
	f = open("download_links.txt", "w")
	for apk in apks:
		f.write(apk.link)
		f.write("\n")
	f.close()



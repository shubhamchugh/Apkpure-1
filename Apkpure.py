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


if __name__ == "__main__":
	# get_categorys()
	# categorys = Mysql.get_all_categorys()
	# for category in categorys:
	#	get_detail_page(category)
	print "hello"

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
	categorys = list()
	for tag in tags:
		for link in tag.find_all("a"):
			Mysql.insert_category(link.attrs['href'][1:])
			categorys.append(link.attrs['href'])
	return categorys


def get_detail_page(arg):
	part_apps = set()
	for i in range(10):
		tags = get_soup(arg + "?page=" + str(i + 1)).find_all("div", class_="category-template-title")
		for tag in tags:
			for link in tag.find_all("a"):
				part_apps.add(link.attrs['href'])
				print link.attrs['href']
	return part_apps

if __name__ == "__main__":
	get_categorys()
	# apps = set()
	# for category in get_categorys():
	# 	apps |= get_detail_page(category)
	#
	# for app in apps:
	# 	print app
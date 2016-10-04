import MySQLdb


def init():
	conn = MySQLdb.connect(host='localhost', port=3306, user='root', passwd='5LOVEysq', db='Apkpure')
	return conn


def close(conn):
	cur = conn.cursor()
	cur.close()
	conn.commit()
	conn.close()


def search_category(conn, name):
	cur = conn.cursor()
	sql = "select count(*) from category where name = %s"
	cur.execute(sql, [name])
	count = cur.fetchone()[0]
	return count


def insert_category(name):
	conn = init()
	cur = conn.cursor()
	count = search_category(conn, name)
	if count == 0:
		sql = "insert into category(name) values (%s)"
		cur.execute(sql, [name])
		close(conn)


def get_all_categorys():
	conn = init()
	cur = conn.cursor()
	sql = "select * from category"
	cur.execute(sql)
	results = cur.fetchall()
	categorys = list()
	for r in results:
		categorys.append(r[1])
	return categorys


def search_apks(category, page):
	conn = init()
	cur = conn.cursor()
	sql = "select count(*) from apk_info where category = %s and page = %s"
	cur.execute(sql, [category, page])
	count = cur.fetchone()[0]
	return count


def insert_apks(category, page, url):
	conn = init()
	cur = conn.cursor()
	sql = "insert into apk_info(category, page, url, size) values (%s, %s, %s, 0)"
	cur.execute(sql, [category, page, url])
	close(conn)


def get_no_size_apks():
	conn = init()
	cur = conn.cursor()
	sql = "select * from apk_info where size = 0"
	cur.execute(sql)
	results = cur.fetchall()
	apks = list()
	for r in results:
		apks.append(r[3])
	return apks


def update_apk_size(url, size, is_google):
	conn = init()
	cur = conn.cursor()
	sql = "update apk_info set size = %s, isGoogle = %s where url = %s"
	cur.execute(sql, [size, is_google, url])
	close(conn)


def get_no_link_apks():
	conn = init()
	cur = conn.cursor()
	sql = "select * from apk_info where size > 0 and download_link is NULL"
	cur.execute(sql)
	results = cur.fetchall()
	apks = list()
	for r in results:
		apks.append(r[3])
	return apks


def update_apk_link(url, link):
	conn = init()
	cur = conn.cursor()
	sql = "update apk_info set download_link = %s where url = %s"
	cur.execute(sql, [link, url])
	close(conn)


class apk:
	def __init__(self, size, link):
		self.size = size
		self.link = link


def get_apks(size):
	conn = init()
	cur = conn.cursor()
	sql = "select * from apk_info where size > 0 and size <= %s order by size"
	cur.execute(sql, [size])
	results = cur.fetchall()
	apks = list()
	for r in results:
		apk_info = apk(r[4], r[5])
		apks.append(apk_info)
	return apks


def update_apk_download_link(url, link):
	conn = init()
	cur = conn.cursor()
	sql = "update apk_info set download_link = %s where url = %s"
	cur.execute(sql, [link, url])
	close(conn)

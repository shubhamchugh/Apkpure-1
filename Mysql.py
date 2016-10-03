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
	count = search_category(conn, url)
	sql = "insert into apk_info(category, page, url, size) values (%s, %s, %s, 0)"
	cur.execute(sql, [category, page, url])
	close(conn)

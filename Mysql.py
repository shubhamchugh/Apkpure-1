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

import sqlite3

conn = sqlite3.connect('database_test.db')
cur = conn.cursor()
cur.execute("SELECT r_review from mobiles1")
rows = cur.fetchall()
for row in rows:
	print(row[0].encode("UTF-8"))
conn.close()

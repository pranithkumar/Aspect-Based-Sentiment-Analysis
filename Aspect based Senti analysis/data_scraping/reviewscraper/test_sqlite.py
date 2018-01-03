import sqlite3
import json

traffic = json.load(open('flipkartreviews.json'))
conn = sqlite3.connect('database_test.db')
conn.execute('CREATE TABLE mobiles1 (r_title TEXT, r_rating TEXT, r_review BLOB)')
cur = conn.cursor()
for review in traffic:
    rev = review["review"]
    rat = review["rating"]
    tit = review["title"]
    cur.execute("INSERT INTO mobiles1 (r_title,r_rating,) VALUES (?,?,?,?)",(nm,addr,city,pin) )
    con.commit()
    #print key
#conn.execute('CREATE TABLE mobiles (product TEXT, r_title TEXT, r_rating TEXT, r_review BLOB)')
#print "table formed successfully"
conn.close()

import sqlite3
import json

traffic = json.load(open('data/flipkart/honor-6x-gold-32-gb.json'))
conn = sqlite3.connect('database_test.db')
#conn.execute('CREATE TABLE mobiles1 (r_title TEXT, r_rating TEXT, r_review BLOB)')
cur = conn.cursor()
for review in traffic:
    rev = review["review"]
    rat = review["rating"]
    tit = review["title"]
    cur.execute("INSERT INTO mobiles1 (r_title,r_rating,r_review) VALUES (?,?,?)",(tit,rat,rev) )
    conn.commit()
    #print key
#conn.execute('CREATE TABLE mobiles (product TEXT, r_title TEXT, r_rating TEXT, r_review BLOB)')
#print "table formed successfully"
conn.close()

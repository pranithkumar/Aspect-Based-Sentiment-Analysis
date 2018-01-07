import sqlite3
import json
'''
with open('data/mobiles.json') as file:
          traffic = json.load(file) '''
traffic = json.load(open('data/Cell_Phones_and_Accessories_5.json'))
conn = sqlite3.connect('database_mobiles.db')
conn.execute('CREATE TABLE mobiles1 (rr_id TEXT, r_title TEXT, r_rating TEXT, r_review BLOB, r_date TEXT)')
cur = conn.cursor()
for review in traffic:
    rev = review["reviewText"]
    rating = review["overall"]
    title = review["summary"]
    revId = review["reviewerID"]
    revTime = review["reviewTime"]
    cur.execute("INSERT INTO mobiles1 (rr_id,r_title,r_rating,r_review,r_date) VALUES (?,?,?,?,?)",(revId,title,rating,rev,revTime) )
    conn.commit()
    #print key
#conn.execute('CREATE TABLE mobiles (product TEXT, r_title TEXT, r_rating TEXT, r_review BLOB)')
print "table formed successfully"
conn.close()
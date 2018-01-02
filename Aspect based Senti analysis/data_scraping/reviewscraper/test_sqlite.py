import sqlite3
import json

traffic = json.load(open('amazonreviews.json'))
conn = sqlite3.connect('database_test.db')

someitem = traffic.itervalues().next()
columns = list(someitem.keys())
print columns
#conn.execute('CREATE TABLE mobiles (product TEXT, r_title TEXT, r_rating TEXT, r_review BLOB)')
#print "table formed successfully"
conn.close()

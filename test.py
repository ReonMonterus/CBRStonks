import sqlite3
import json

db = "./stonkdb.db"
conn = sqlite3.connect(db)
c = conn.cursor()
userid = '214097127960215553'
username = "stuff"
ticker = "$JAM"
shares = 10
c.execute("SELECT * from 'Users' WHERE UserID = '" + userid + "'")
col_names = [cn[0] for cn in c.description]
col_names = col_names[3:]
print(col_names)
info = c.fetchall()
print(info)
stonks = info[0][3:]
print(stonks)
holdqty = ""
holdticker = ""
for idx,values in enumerate(stonks):
    if values > 0:
        holdqty = str(holdqty) + str(values) + "\n"
        holdticker = str(holdticker) + "$" + str(col_names[idx]) + "\n"
print(holdqty)
print(holdticker)
# stonks = info[3:64]
# userstonklist = ""
# for values in stonks:
#     if values[2] > 0:
#         userstonklist = str(userstonklist) + values
# print(userstonklist)
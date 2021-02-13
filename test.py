import sqlite3
import json

db = "./stonkdb.db"
conn = sqlite3.connect(db)
c = conn.cursor()
userid = '297924849639227393'
username = "stuff"
ticker = "$JAM"
shares = 10
c.execute("SELECT * from 'Users' WHERE UserID = '" + userid + "'")
col_names = [cn[0] for cn in c.description]
col_names = col_names[3:]
print(col_names)
info = c.fetchone()
print(info)
stonks = info[3:]
print(stonks)
holdqty = ""
holdticker = ""
networth = int(info[2])
cash = str(info[2])
stonks = info[3:]
for idx,values in enumerate(stonks):
    if values > 0:
        holdqty = str(holdqty) + str(values) + "\n"
        holdticker = str(holdticker) + "$" + str(col_names[idx]) + "\n"
        c.execute("SELECT Price FROM Stonks WHERE ticker = '$" + col_names[idx] + "'")
        stonkvalue = c.fetchone()
        print(col_names[idx], values)
        iterstonkvalue = stonkvalue[0] * values
        print(str(col_names[idx])+" worth $"+str(iterstonkvalue))
        networth = networth + iterstonkvalue
        print("$"+str(networth))
# stonks = info[3:64]
# userstonklist = ""
# for values in stonks:
#     if values[2] > 0:
#         userstonklist = str(userstonklist) + values
# print(userstonklist)
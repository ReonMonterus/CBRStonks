import sqlite3

db = "./stonkdb.db"
conn = sqlite3.connect(db)
c = conn.cursor()
c.execute("SELECT * FROM Users")
col_names = [cn[0] for cn in c.description]
col_names = col_names[3:]
info = c.fetchone()
stonks = info[3:]
for idx,values in enumerate(stonks):
    print(col_names[idx])
    c.execute("UPDATE Stonks SET Outstanding = (select sum(" + str(col_names[idx]) + ") from Users) WHERE ticker = '$" + str(col_names[idx]) + "'")
conn.commit()
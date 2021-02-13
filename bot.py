import discord
import os
import sqlite3
from disputils import BotEmbedPaginator

client = discord.Client()
db = "./stonkdb.db"
conn = sqlite3.connect(db)
c = conn.cursor()

@client.event
async def on_message(message):
    if message.content.startswith('$stonk account'):
        try:
            userid = str(message.author.id)
            username = str(message.author)
            c.execute("SELECT * from 'Users' WHERE UserID = '" + userid + "'")
            col_names = [cn[0] for cn in c.description]
            col_names = col_names[3:]
            info = c.fetchall()
            if info == []:
                c.execute("INSERT INTO Users(userid,username,money) VALUES ('" + userid + "','" + username + "',100000)")
                conn.commit()
                embed = discord.Embed()
                embed.set_author(name="Stonks Bot")
                embed.color = 0xf1c40f
                embed.add_field(name="Welcome!", value=message.author.mention + " you may now trade for tendies!")
                await message.channel.send(embed=embed)
            else:
                holdqty = ""
                holdticker = ""
                cash = str(info[0][2])
                stonks = info[0][3:]
                for idx,values in enumerate(stonks):
                    if values > 0:
                        holdqty = str(holdqty) + str(values) + "\n"
                        holdticker = str(holdticker) + "$" + str(col_names[idx]) + "\n" 
                if holdqty == "":
                    embed = discord.Embed()
                    embed.set_author(name="Stonks Bot")
                    embed.color = 0xf1c40f
                    embed.title = "Current info for " + str(username)
                    embed.add_field(name="Cash on hand", value="$" + cash)
                    await message.channel.send(embed=embed)
                else:
                    embed = discord.Embed()
                    embed.set_author(name="Stonks Bot")
                    embed.color = 0xf1c40f
                    embed.title = "Current info for " + str(username)
                    embed.add_field(name="Cash on hand", value="$" + cash)
                    embed.add_field(name="Ticker", value=holdticker)
                    embed.add_field(name="Held QTY", value=holdqty)
                    await message.channel.send(embed=embed)
        except:
            embed = discord.Embed()
            embed.set_author(name="Stonks Bot")
            embed.color = 0xf1c40f
            embed.add_field(name="Congrats!", value="You input something that caused an unexpected error, if you think the thing you did should work, let someone from BC know.")
            await message.channel.send(embed=embed)
    elif message.content.startswith('$stonk price'):
        try:
            username = str(message.author)
            cmd1,cmd2,ticker = message.content.upper().split(" ")
            c.execute("SELECT Price,Name FROM Stonks WHERE Ticker = '" + ticker + "'")
            priceresult = c.fetchone()
            try:
                price = str(priceresult[0])
                stonkname = str(priceresult[1])
            except:
                embed = discord.Embed()
                embed.set_author(name="Stonks Bot")
                embed.color = 0xf1c40f
                embed.add_field(name="Symbol Error", value="You've entered an invalid symbol!")
                await message.channel.send(embed=embed)
            else:
                embed = discord.Embed()
                embed.set_author(name="Stonks Bot")
                embed.color = 0xf1c40f
                embed.add_field(name="Current price for " + stonkname, value = "$" + price)
                await message.channel.send(embed=embed)
        except:
            embed = discord.Embed()
            embed.set_author(name="Stonks Bot")
            embed.color = 0xf1c40f
            embed.add_field(name="Congrats!", value="You input something that caused an unexpected error, if you think the thing you did should work, let someone from BC know.")
            await message.channel.send(embed=embed)
    elif message.content.startswith('$stonk buy'):
        try:
            username = str(message.author)
            userid = str(message.author.id)
            cmd1,cmd2,ticker,shares = message.content.upper().split(" ")
            c.execute("SELECT " + ticker[1:] + ",Money FROM Users WHERE UserID = " + userid)
            buyuserresult = c.fetchone()
            money = int(buyuserresult[1])
            curshares = int(buyuserresult[0])
            if int(shares) < 1:
                embed = discord.Embed()
                embed.set_author(name="Stonks Bot")
                embed.color = 0xf1c40f
                embed.add_field(name="Buy Order Failure", value="No cheating the system pal!")
                await message.channel.send(embed=embed)
            else:
                try:
                    c.execute("SELECT Price,Name FROM Stonks WHERE Ticker = '" + ticker + "'")
                    buyresult = c.fetchone()
                    cost = int(buyresult[0])*int(shares)
                    buyname = str(buyresult[1])
                    newsum = int(money)-int(cost)
                    newbuyshares = int(curshares) + int(shares)
                    if cost > money:
                        embed = discord.Embed()
                        embed.set_author(name="Stonks Bot")
                        embed.color = 0xf1c40f
                        embed.add_field(name="Buy Order Failure", value="You don't have enough money to buy that many shares!")
                        await message.channel.send(embed=embed)
                    else:
                        c.execute("UPDATE Users set " + ticker[1:] + " = " + str(newbuyshares) + " WHERE UserID = " + userid)
                        c.execute("UPDATE Users set Money = " + str(newsum) + " WHERE UserID = " + userid)
                        conn.commit()
                        embed = discord.Embed()
                        embed.set_author(name="Stonks Bot")
                        embed.color = 0xf1c40f
                        embed.add_field(name="Buy Order Success!", value="Congrats! You purchased " + shares + " shares of " + buyname + " worth $" + str(cost))
                        await message.channel.send(embed=embed)
                except:
                    embed = discord.Embed()
                    embed.set_author(name="Stonks Bot")
                    embed.color = 0xf1c40f
                    embed.add_field(name="General Error", value="You've either input a wrong symbol or need to enter $stonk account to make an account first")
                    await message.channel.send(embed=embed)
        except:
            embed = discord.Embed()
            embed.set_author(name="Stonks Bot")
            embed.color = 0xf1c40f
            embed.add_field(name="Congrats!", value="You input something that caused an unexpected error, if you think the thing you did should work, let someone from BC know.")
            await message.channel.send(embed=embed)
    elif message.content.startswith('$stonk help'):
        try:
            embed = discord.Embed()
            embed.set_author(name="Stonks Bot")
            embed.color = 0xf1c40f
            embed.title = "So you need to know how to make tendies?"
            embed.add_field(name="$stonk account", value="I'll show you your account info or make an account if you don't have one")
            embed.add_field(name="$stonk buy $TIC X", value="Where $TIC is your ticker and X is how many shares you want to buy, I'll make an order to buy that many shares")
            embed.add_field(name="$stonk sell $TIC X", value="Where $TIC is your ticker and X is how many shares you want to sell, I'll make an order to sell that many shares")
            embed.add_field(name="$stonk market", value="I'll show you the current prices of all shares available")
            embed.add_field(name="$stonk price $TIC", value="Where $TIC is your ticker, I'll tell you how much it costs")
            await message.channel.send(embed=embed)
        except:
            embed = discord.Embed()
            embed.set_author(name="Stonks Bot")
            embed.color = 0xf1c40f
            embed.add_field(name="Congrats!", value="You input something that caused an unexpected error, if you think the thing you did should work, let someone from BC know.")
            await message.channel.send(embed=embed)
    elif message.content.startswith('$stonk sell'):
        try:
            username = str(message.author)
            userid = str(message.author.id)
            cmd1,cmd2,ticker,shares = message.content.upper().split(" ")
            c.execute("SELECT " + ticker[1:] + ",Money FROM Users WHERE UserID = " + userid)
            selluserresult = c.fetchone()
            availshares = int(selluserresult[0])
            money = int(selluserresult[1])
            if int(shares) < 1:
                embed = discord.Embed()
                embed.set_author(name="Stonks Bot")
                embed.color = 0xf1c40f
                embed.add_field(name="Sell Order Failure", value="No cheating the system pal!")
                await message.channel.send(embed=embed)
            else:
                try:
                    c.execute("SELECT Price,Name FROM Stonks WHERE Ticker = '" + ticker + "'")
                    sellresult = c.fetchone()
                    profit = int(sellresult[0])*int(shares)
                    sellname = str(sellresult[1])
                    newsellsum = int(money)+int(profit)
                    newshares = int(availshares)-int(shares)
                    if int(shares) > int(availshares):
                        embed = discord.Embed()
                        embed.set_author(name="Stonks Bot")
                        embed.color = 0xf1c40f
                        embed.add_field(name="Sell Order Failure", value="You don't have that many shares!")
                        await message.channel.send(embed=embed)
                    else:
                        c.execute("UPDATE Users set " + ticker[1:] + " = " + str(newshares) + " WHERE UserID = " + userid)
                        c.execute("UPDATE Users set Money = " + str(newsellsum) + " WHERE UserID = " + userid)
                        conn.commit()
                        embed = discord.Embed()
                        embed.set_author(name="Stonks Bot")
                        embed.color = 0xf1c40f
                        embed.add_field(name="Sell Order Success!", value="Congrats! You sold " + shares + " shares of " + sellname + " worth $" + str(profit))
                        await message.channel.send(embed=embed)
                except:
                    embed = discord.Embed()
                    embed.set_author(name="Stonks Bot")
                    embed.color = 0xf1c40f
                    embed.add_field(name="General Error", value="You've either input a wrong symbol or need to enter $stonk account to make an account first")
                    await message.channel.send(embed=embed)
        except:
            embed = discord.Embed()
            embed.set_author(name="Stonks Bot")
            embed.color = 0xf1c40f
            embed.add_field(name="Congrats!", value="You input something that caused an unexpected error, if you think the thing you did should work, let someone from BC know.")
            await message.channel.send(embed=embed)
    elif message.content.startswith('$stonk market'):
        try:
            username = str(message.author)
            userid = str(message.author.id)
            c.execute("SELECT * from Stonks ORDER BY Price DESC")
            stonklist = c.fetchall()
            embed = discord.Embed()
            embed.set_author(name="Stonks Bot")
            embed.color = 0xf1c40f
            namelist = ""
            tickerlist = ""
            pricelist = ""
            for rows in stonklist:
                namelist = str(namelist) + str(rows[0]) + "\n"
                tickerlist = str(tickerlist) + str(rows[1]) + "\n"
                pricelist = str(pricelist) + "$" + str(rows[2]) + "\n"
            embed.add_field(name="Civ Names", value=namelist)
            embed.add_field(name="Ticker", value=tickerlist)
            embed.add_field(name="Prices", value=pricelist)
            await message.channel.send(embed=embed)
        except:
            embed = discord.Embed()
            embed.set_author(name="Stonks Bot")
            embed.color = 0xf1c40f
            embed.add_field(name="Congrats!", value="You input something that caused an unexpected error, if you think the thing you did should work, let someone from BC know.")
            await message.channel.send(embed=embed)

client.run('ODA2NzQ0MzQzNjgyNDgyMTc2.YBt5OA.4_oGlA_gZbe2Mcadim74dKkAt0Q')
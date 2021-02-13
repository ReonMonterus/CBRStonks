import discord
import os
import sqlite3

client = discord.Client()
db = "./stonkdb.db"
conn = sqlite3.connect(db)
c = conn.cursor()

@client.event
async def on_message(message):
    if message.content.startswith('$stonk account'):
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
            networth = int(info[0][2])
            cash = str(info[0][2])
            stonks = info[0][3:]
            for idx,values in enumerate(stonks):
                if values > 0:
                    holdqty = str(holdqty) + str(values) + "\n"
                    holdticker = str(holdticker) + "$" + str(col_names[idx]) + "\n"
                    c.execute("SELECT Price FROM Stonks WHERE ticker = '$" + col_names[idx] + "'")
                    iterstonkvalue = c.fetchall()
                    iterstonkvalue = iterstonkvalue[0][0] * values
                    networth = networth + iterstonkvalue
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
                embed.add_field(name="Ticker", value=holdticker, inline=True)
                embed.add_field(name="Held QTY", value=holdqty, inline=True)
                embed.add_field(name="Cash on hand", value="$" + cash, inline=False)
                embed.add_field(name="Current Net Worth", value= "$" + str(networth), inline = False)
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
    elif message.content.startswith('$stonk help'):
        embed = discord.Embed()
        embed.set_author(name="Stonks Bot")
        embed.color = 0xf1c40f
        embed.title = "So you need to know how to make tendies?"
        embed.add_field(name="$stonk account", value="I'll show you your account info or make an account if you don't have one")
        embed.add_field(name="$stonk market", value="I'll show you the current prices of all shares available while the market is open")
        embed.add_field(name="$stonk price $TIC", value="Where $TIC is your ticker, I'll tell you how much it costs")
        embed.add_field(name="$stonk price person or @person", value="I can spy on someone else's account if you like! Make sure to use their discord name (not server nick), and be specific! @them if you want them to know!")
        await message.channel.send(embed=embed)
    elif message.content.startswith('$stonk market'):
        username = str(message.author)
        userid = str(message.author.id)
        embed = discord.Embed()
        embed.set_author(name="Stonks Bot")
        embed.color = 0xf1c40f
        embed.add_field(name="Market is Closed", value="Come back next week after the PR releases")
        await message.channel.send(embed=embed)
    elif message.content.startswith("$stonk spy"):
        cmd1,cmd2,spyuser = message.content.split(" ")
        try:
            cfn = re.findall("\d+", spyuser)[0].isnumeric()
        except:
            cfn = False
        if cfn:
            userid = re.findall("\d+", spyuser)[0]
            c.execute("SELECT * from 'Users' WHERE UserID = '" + str(userid) + "'")
        else:
            c.execute("SELECT * from 'Users' WHERE Username like '" + str(spyuser) + "%'")
        username = str(message.author)
        col_names = [cn[0] for cn in c.description]
        col_names = col_names[3:]
        info = c.fetchone()
        holdqty = ""
        holdticker = ""
        if info == None:
            embed = discord.Embed()
            embed.set_author(name="Stonks Bot")
            embed.color = 0xf1c40f
            embed.add_field(name="Sorry!", value="I couldn't find anyone to spy on with the name you gave me, try being more specific!")
            await message.channel.send(embed=embed)
        else:
            username = str(info[1])
            networth = int(info[2])
            cash = str(info[2])
            stonks = info[3:]
            for idx,values in enumerate(stonks):
                if values > 0:
                    holdqty = str(holdqty) + str(values) + "\n"
                    holdticker = str(holdticker) + "$" + str(col_names[idx]) + "\n"
                    c.execute("SELECT Price FROM Stonks WHERE ticker = '$" + col_names[idx] + "'")
                    iterstonkvalue = c.fetchone()
                    iterstonkvalue = iterstonkvalue[0] * values
                    networth = networth + iterstonkvalue
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
                embed.add_field(name="Ticker", value=holdticker, inline=True)
                embed.add_field(name="Held QTY", value=holdqty, inline=True)
                embed.add_field(name="Cash on hand", value="$" + cash, inline=False)
                embed.add_field(name="Current Net Worth", value= "$" + str(networth), inline = False)
                await message.channel.send(embed=embed)

client.run('ODA2NzQ0MzQzNjgyNDgyMTc2.YBt5OA.4_oGlA_gZbe2Mcadim74dKkAt0Q')
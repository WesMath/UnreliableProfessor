import discord
import time
import random
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import datetime
import sqlite3
import math
import re


def contains(somestring, sub):#Helper function to rewrite pieces of code- eventually I won't use contains/in, but for now it'll do
    if sub in somestring:
        return True
    else:
        return False

def valid(regexpr, content):#Custom function defined in SQLite connection to test against values
    try:
        if re.match(regexpr, content) is None:
            #print(0)
            return 0
        else:
            print(1, regexpr)
            return 1
    except Exception as e:#Was for debugging purposes
        print(str(e))

client = discord.Client()



@client.event
async def on_ready():
    print("Logged in successfully.")
    global the_server
    for serv in client.servers:
        the_server = serv
    print(serv)

@client.event
async def on_message(message):
    meant_for_bot = False
    for user in message.mentions:
        if user.id == client.user.id:
            print("Meant for us!")
            meant_for_bot = True
            break
    if not meant_for_bot:
        #print("Not meant for us...")
        return
	#print("Message: " + message.content)
    #print("Got here")
	# test command
    if contains(message.content, "up tonight?"):
	    await client.send_message(message.channel, "Yes, I am up!")
    elif contains(message.content, "go away for now"):
            await client.send_message(message.channel, "I will return with a vengeance.")
            #client.logout()
    elif contains(message.content, "SING!"):
        lyricsRAW = """Humidity's rising, Barometer's getting low
According to all sources, the street's the place to go
Cause tonight for the first time
Just about half-past ten
For the first time in history
It's gonna start raining men.
It's Raining Men! Hallelujah!"""
        lyrics = lyricsRAW.split('\n')
        for line in lyrics:
            await client.send_message(message.channel, line)
            time.sleep(1)#For dramatic effect
    elif contains(message.content, "Markov"):
        user = message.author#Will eventually split/generalize into user-specific and channel aggregate
        args = message.content.split("Markov")
        if len(args) > 1:
            txtuser = args[1][1::]#strip whitespace
            for u in the_server.members:
                if u.name == txtuser:
                    user = u
        for chan in the_server.channels:
            if chan.name == "help_corner":
                the_channel = chan
        markov = {"BEG_TOKEN":[]}
        count = 0
        async for mess in client.logs_from(the_channel, limit=1000):
            if mess.author.id == user.id:
                count += 1
                try:
                    print(mess.content)
                except UnicodeEncodeError:
                    continue
                split = mess.content.split(" ")
                if "<@" not in split[0]:
                    markov["BEG_TOKEN"].append(split[0])
                else:
                    try:
                        markov["BEG_TOKEN"].append(split[1])
                    except:
                        continue
                for i in range(len(split)-1):
                    if split[i] not in markov and "<@" not in split[i]:
                        markov[split[i]] = [split[i+1]]
                    elif "<@" not in split[i]:
                        markov[split[i]].append(split[i+1])
                if split[len(split) - 1] not in markov:
                        markov[split[len(split) - 1]] = ["END_TOKEN"]
                else:
                    markov[split[len(split) - 1]].append("END_TOKEN")
        print(markov)
        print(count, len(markov["BEG_TOKEN"]))
        next_word = markov["BEG_TOKEN"][random.randint(0,len(markov["BEG_TOKEN"])-1)]
        output = ""
        while next_word != "END_TOKEN":
            randChooser = random.randint(0,len(markov[next_word])-1)
            print(output, randChooser)
            output += " " + next_word
            next_word = markov[next_word][randChooser]
        await client.send_message(message.channel, output)
    elif contains(message.content, "!ebook"):
        await client.send_message(message.channel, "I have received your request, {}".format(message.author.name))
        """r = requests.get("http://www.packtpub.com/packt/offers/free-learning")
        data = r.text
        print(data)"""

        site= "http://www.packtpub.com/packt/offers/free-learning"
        hdr = {'User-Agent': 'Mozilla/5.0'}
        req = Request(site,headers=hdr)
        page = urlopen(req)
        print(page)
        soup = BeautifulSoup(page, "lxml")
        for title in soup.find_all('h2', limit=1):
            print(title)
            output = "The book of the day is:\n" + str(title)
            now = datetime.datetime.now()
            t = datetime.timedelta(hours=18)
            nowdelta = datetime.timedelta(hours=now.hour)
            delta = t - nowdelta
            secs = delta.total_seconds()
            hours = (secs / 3600) % 24
            time_remaining = "You have less than {} hours remaining to claim this book:\nhttps://www.packtpub.com/packt/offers/free-learning".format(hours)
            await client.send_message(message.channel, output)
            await client.send_message(message.channel, time_remaining)
    elif contains(message.content, "search"):
        spaced_out = message.content.split("search")[1][1::].split(" ")[0]
        print(message.content.split("search")[1][1::])
        desired_search = "%" + message.content.split("search")[1][1::]+ "%"
        try:
            print("spaced out is {}".format(spaced_out))
            pageNum = int(spaced_out) - 1
            print("int casting succeeded")
            desired_search = "%"+desired_search.split(" ", 1)[1]
            max_num = (pageNum * 10) + 9
            resultCount = pageNum * 10
        except ValueError:
            print("int casting failed")
            max_num = 9
            resultCount = 0
            pageNum = 0
            #then there's no prepended number
        conn = sqlite3.connect("bookdb.sqlite")#Keep all information about database hidden, since incoming requests aren't sanitized- can't trust a server with pentesters on it
        conn.create_function("valid", 2, valid)#create ability to regex check entries
        c = conn.cursor()
        print(desired_search)
        """c.execute("SELECT * FROM CompSciBooks WHERE name LIKE ?", (desired_search,))#Old way of searching using rudimentary string matching
        all_rows = c.fetchall()
        print(all_rows)"""

        desire = desired_search.replace("%", "")
        regchars = "/+*?{}.:\[],^$=!<>-&_"
        plain = True
        for char in regchars:
            if char in desire:
                plain = False
                break
        if plain:
            print("We got a plain one over here")
            desire = "(?i).*" + desire + ".*"
        print("desired search term is {}".format(desire))
        c.execute("SELECT * FROM CompSciBooks WHERE valid(?, name) = 1", (desire,))
        da_rows = c.fetchall()
        print(da_rows)
        
        """print(len(all_rows), len(da_rows))
        for row in all_rows:
            if row not in da_rows:
                print(row)"""
        output = "```Page {} of {}```\n".format(pageNum + 1, math.ceil(len(da_rows)/10))
        resourceCount = 0
        for row in da_rows:
            if resourceCount > max_num:
                break
            elif resourceCount >= resultCount:
                output += str(resourceCount) + ". " + row[0] + "\n" + row[1] + "\n"
            resourceCount += 1
        await client.send_message(message.channel, output)
    elif contains(message.content, "help"):
        await client.send_message(message.channel, "Hi! I'm a horrible mistake. I do parlor tricks and ebook searches.")
    elif contains(message.content, "author"):
        await client.send_message(message.channel, "<@310860026816233473> maintains me. Sometimes. When he's in a good mood.")
    elif contains(message.content, "source"):
        await client.send_message(message.channel, "My source code is not stored in a Github repo (yet), so PM <@310860026816233473> for details or code samples.")
    else:#default case for usage
        await client.send_message(message.channel, """*@It'sRainingMen up tonight?*
Lets you know if I'm accepting commands
*@It'sRainingMen go away for now*
Currently a broken(?) command to shut down the bot. I'll be removing this soon
*@It'sRainingMen Markov <username>*
Takes messages sent recently in #help_corner and generates new text from <username> (defaults to self). No error handling, so it will probably crash if you're not active there.
*@It'sRainingMen !ebook*
Posts packt's free ebook of the day and how many hours you have left to claim it
*@It'sRainingMen search <pageNumber> <regex>*
Retrieves page of ebook search results for specified regex (defaults to first page and basic string search)
*@It'sRainingMen SING!*
Grab a chair and listen to me hum a few bars from the Weather Girls""")

                                  
"""
BookPenguin: Welcome to BookPengiun, powered by Lenny Remastered!

To search for a book enter !ebooks followed by regex or Regular Expression that represents your desired output.
Here is an example: !ebooks Java

Books are shown in pages where each page contains a list of 10 items. To see the results of another page, simply precede your regex with a page number.
Here is an example: !ebooks 3 Java

To see this help menu again, simply enter !ebooks.
If you have any further questions, don't hesitate to ping @shadow!

Happy Hunting!"""        

key = open('appkey.txt', 'r')#Read API key from text file in directory (which git ignores)
thekey = key.read()
key.close()
client.run(thekey)#Initialize a connection using application token

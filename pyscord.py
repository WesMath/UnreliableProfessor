import discord
import time
import random
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import datetime
import sqlite3
import math
import re
import json
import urllib.request
import time
from threading import Thread
import asyncio
import multiprocessing as mp


class MyException(Exception):
    pass

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

global client
client = discord.Client()
global the_dates
the_dates = ""
global testing


def worker():
    print("worker reached")
    #loop = asyncio.get_event_loop()
    #loop.run_until_complete(subscriptions())

""""@asyncio.coroutine    
async def subscriptions():
    while(True):
        #Sleep after checking time:
        now = datetime.datetime.now()
        desired = -1
        secs = 1
        if now.hour >= 7 and now.hour < 19:
            desired = 1 #for ebook
            t = datetime.timedelta(hours=15, minutes=15)
            current = datetime.timedelta(hours=now.hour, minutes=now.minute)
            delta = t - current
            secs = delta.total_seconds()
            if secs < 0:
                secs *= -1
        elif now.hour >= 19 or now.hour < 7:
            desired = 0 #for poem
            t = datetime.timedelta(hours=7)
            current = datetime.timedelta(hours=now.hour, minutes=now.minute)
            delta = t - current
            secs = delta.total_seconds()
            if secs < 0:
                secs *= -1
        else:
            print("Never should reach here")
        print("Ready to sleep for {} seconds.".format(secs))
        time.sleep(secs)
        #Send out appropriate message
        for chan in the_server.channels:
            #print(chan.name)
            if chan.name == "bot_testing":
                print("Found correct channel")
                testing = chan
        conn = sqlite3.connect("subscriptions.sqlite")
        c = conn.cursor()
        if desired == 1:
            c.execute("SELECT id FROM Subscriptions WHERE ebook = 1")
            da_people = c.fetchall()
            print("ebook wanted")
            print(da_people)
            print(client)
            #await client.send_message(testing, "Here's your ebook")
            site= "http://www.packtpub.com/packt/offers/free-learning"
            hdr = {'User-Agent': 'Mozilla/5.0'}
            req = Request(site,headers=hdr)
            page = urlopen(req)
            #print(page)
            soup = BeautifulSoup(page, "lxml")
            for title in soup.find_all('h2', limit=1):
                #print(title.getText())
                output = "The book of the day is:\n__**" + title.getText()+"**__"
            t = datetime.timedelta(hours=18)
            nowdelta = datetime.timedelta(hours=now.hour)
            delta = t - nowdelta
            secs = delta.total_seconds()
            #print("The time between now and 6 in hours has been {}".format(secs / 3600))
            hours = (secs / 3600) % 24
            time_remaining = "\nYou have less than {} hours remaining to claim this book:\nhttps://www.packtpub.com/packt/offers/free-learning".format(str(hours).strip(".0"))
            await client.send_message(testing, output+time_remaining)
            output = ""
            for person in da_people:
                output += "<@"+person[0]+">, "
            await client.send_message(testing, output)
        elif desired == 0:
            c.execute("SELECT id FROM Subscriptions WHERE poem = 1")
            da_people = c.fetchall()
            print("poem wanted")
            print(da_people)
            #await client.send_message(testing, "I got a poem for you- just kidding, this is a placeholder.")
            day = datetime.date.today()
            #31 days in a month to prevent overlap
            hashable = day.month*31 + day.day
            print(client)
            client.send_message(testing,"The poem of the day is:\nhttp://www.bartleby.com/265/"+str((421*hashable)%424)+".html")
            #use coprimes to generate unique nums
            output = ""
            for person in da_people:
                output += "<@"+person[0]+">, "
            client.send_message(testing, output)
        ""ValueError: sleep length must be non negative
           Ready to sleep for 0.0 seconds
           Ready to sleep for -60.0 seconds
           Found correct channel
           One user listed""
        c.close()
        time.sleep(120) #Prevents repeated calling"""






@client.event
async def on_ready():
    print("Logged in successfully.")
    global the_server
    for serv in client.servers:
        the_server = serv
    #print(serv)
    #subscriptions_thread().start()
    """sub_process = mp.Process(target=worker)
    print("assigned Process")
    sub_process.start()
    print("process started")"""

@client.event
async def on_message(message):
    now = datetime.datetime.now()
    want_resource = True
    if now.hour == 8 or now.hour == 20:
        search_term = ""
        today = datetime.datetime.today()
        if today.month < 10:
            search_term += "0" + str(today.month)
        else:
            search_term += str(today.month)
        search_term += "-"
        if today.day < 10:
            search_term += "0" + str(today.day)
        else:
            search_term += str(today.day)
        search_term += "-" + str(today.year)
        if now.hour == 8:
            search_term += "a"
        else:
            search_term += "b"
        #search_term += "\n"
        print(search_term)
        global the_dates
        for line in the_dates.splitlines():
            print(line)
            if line == search_term:
                want_resource = False
        if want_resource:
            the_dates += search_term + "\n"
    if(want_resource):
        #testing = "placeholder"
        for chan in the_server.channels:
            #print(chan.name)
            if chan.name == "bot_testing":
                print("Found correct channel")
                testing = chan
        conn = sqlite3.connect("subscriptions.sqlite")
        c = conn.cursor()
        if now.hour == 20:
            c.execute("SELECT id FROM Subscriptions WHERE ebook = 1")
            da_people = c.fetchall()
            print("ebook wanted")
            print(da_people)
            print(client)
            # await client.send_message(testing, "Here's your ebook")
            site = "http://www.packtpub.com/packt/offers/free-learning"
            hdr = {'User-Agent': 'Mozilla/5.0'}
            req = Request(site, headers=hdr)
            page = urlopen(req)
            # print(page)
            soup = BeautifulSoup(page, "lxml")
            for title in soup.find_all('h2', limit=1):
                # print(title.getText())
                output = "The book of the day is:\n__**" + title.getText() + "**__"
            t = datetime.timedelta(hours=18)
            nowdelta = datetime.timedelta(hours=now.hour)
            delta = t - nowdelta
            secs = delta.total_seconds()
            # print("The time between now and 6 in hours has been {}".format(secs / 3600))
            hours = (secs / 3600) % 24
            time_remaining = "\nYou have less than {} hours remaining to claim this book:\nhttps://www.packtpub.com/packt/offers/free-learning".format(
                str(hours).strip(".0"))
            await client.send_message(testing, output + time_remaining)
            output = ""
            for person in da_people:
                output += "<@" + person[0] + ">, "
            await client.send_message(testing, output)
        elif now.hour == 8:
            c.execute("SELECT id FROM Subscriptions WHERE poem = 1")
            da_people = c.fetchall()
            print("poem wanted")
            print(da_people)
            # await client.send_message(testing, "I got a poem for you- just kidding, this is a placeholder.")
            day = datetime.date.today()
            # 31 days in a month to prevent overlap
            hashable = day.month * 31 + day.day
            print(client)
            await client.send_message(testing, "The poem of the day is:\nhttp://www.bartleby.com/265/" + str(
                (421 * hashable) % 424) + ".html")
            # use coprimes to generate unique nums
            output = ""
            for person in da_people:
                output += "<@" + person[0] + ">, "
            await client.send_message(testing, output)
        c.close()
    meant_for_bot = False
    #if message.channel.is_private is False:
    for user in message.mentions:
        if user.id == client.user.id:
            #print("Meant for us!")
            meant_for_bot = True
            break
    """elif "Ozymandias" not in message.author.name:#Changed the name and then infinite messages happened
        meant_for_bot = True"""
    correct_channel = False
    if message.channel.is_private is True or message.channel.name in ["bot_spam", "bot_testing"]:
        correct_channel = True
    if not meant_for_bot:
        #print("Not meant for us...")
        return
	#print("Message: " + message.content)
    #print("Got here")
    if contains(message.content, "sneakyOBSOLETE2"):#So I can run 2 versions at once and only have one reply to me
        return
    if not correct_channel:
        await client.send_message(message.channel, "Please confine all bot interaction to #bot_spam, #bot_testing, or private direct messages to the bot.")
        return
    if contains(message.content, "up tonight?"):
	    await client.send_message(message.channel, "Yes, I am up!")
    elif contains(message.content, "go away for now"):
        can_issue = False
        if contains((message.author.name), "Kapusta"):
            can_issue = True
        #else:
        for role in message.author.roles:
            if str(role) == "Admins" or str(role) == "Moderator":
                can_issue = True
                break
        if not can_issue:
            return
        await client.send_message(message.channel, "I will return with a vengeance.")
        client.close()
        print(client.is_closed, client.is_logged_in)
        time.sleep(600) #Blocks processing of messages and eventually times out connection
    elif contains(message.content, "SING!") or contains(message.content, "localWeather"):
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
            time.sleep(1.2)#For dramatic effect
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
        #print(markov)
        #print(count, len(markov["BEG_TOKEN"]))
        next_word = markov["BEG_TOKEN"][random.randint(0,len(markov["BEG_TOKEN"])-1)]
        output = ""
        while next_word != "END_TOKEN":
            randChooser = random.randint(0,len(markov[next_word])-1)
            #print(output, randChooser)
            output += " " + next_word
            next_word = markov[next_word][randChooser]
        await client.send_message(message.channel, output)
        """elif contains(message.content, "ebook"):
        await client.send_message(message.channel, "I have received your request, {}".format(message.author.name))
        r = requests.get("http://www.packtpub.com/packt/offers/free-learning")
        data = r.text
        print(data)

        site= "http://www.packtpub.com/packt/offers/free-learning"
        hdr = {'User-Agent': 'Mozilla/5.0'}
        req = Request(site,headers=hdr)
        page = urlopen(req)
        #print(page)
        soup = BeautifulSoup(page, "lxml")
        for title in soup.find_all('h2', limit=1):
            #print(title.getText())
            output = "The book of the day is:\n__**" + title.getText()+"**__"
        now = datetime.datetime.now()
        t = datetime.timedelta(hours=18)
        nowdelta = datetime.timedelta(hours=now.hour)
        delta = t - nowdelta
        secs = delta.total_seconds()
        #print("The time between now and 6 in hours has been {}".format(secs / 3600))
        hours = (secs / 3600) % 24
        time_remaining = "\nYou have less than {} hours remaining to claim this book:\nhttps://www.packtpub.com/packt/offers/free-learning".format(str(hours).strip(".0"))
        await client.send_message(message.channel, output+time_remaining)
        await client.send_message(message.channel, time_remaining)"""
    elif contains(message.content, "search"):
        spaced_out = message.content.split("search")[1][1::].split(" ")[0]
        print(message.content.split("search")[1][1::])
        desired_search = "%" + message.content.split("search")[1][1::]+ "%"
        try:
            #print("spaced out is {}".format(spaced_out))
            pageNum = int(spaced_out) - 1
            #print("int casting succeeded")
            desired_search = "%"+desired_search.split(" ", 1)[1]
            max_num = (pageNum * 10) + 9
            resultCount = pageNum * 10
        except ValueError:
            #print("int casting failed")
            max_num = 9
            resultCount = 0
            pageNum = 0
            #then there's no prepended number
        conn = sqlite3.connect("bookdb.sqlite")#Keep all information about database hidden, since incoming requests aren't sanitized- can't trust a server with pentesters on it
        conn.create_function("valid", 2, valid)#create ability to regex check entries
        c = conn.cursor()
        #print(desired_search)
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
        #print(da_rows)
        
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
    elif contains(message.content, "weather"):
        #insert Helsinki weather api
        key = open('weather_api.txt', 'r')#Read API key from text file in directory
        with urllib.request.urlopen("http://api.openweathermap.org/data/2.5/weather?q=Helsinki&APPID="+key.read()) as url:
            data = json.loads(url.read().decode())
            output = "In Helsinki, "+data['weather'][0]['description']+'.\n'
            output += "The temperature is "+ str(((9/5)*(float(data['main']['temp'])-273) + 32))[0:4] +" degrees Fahrenheit and {} degrees Celsius.".format(str(float(data['main']['temp'])-273)[0:4])
            await client.send_message(message.channel, output)
            await client.send_message(message.channel, "If you'd like to see weather in your local area, type @Ozymandias localWeather <your_area>")
        """elif contains(message.content, "poem"):
        day = datetime.date.today()

        #31 days in a month to prevent overlap

        hashable = day.month*31 + day.day

        await client.send_message(message.channel,"The poem of the day is:\nhttp://www.bartleby.com/265/"+str((421*hashable)%424)+".html")
        #use coprimes to generate unique nums"""
    elif contains(message.content, "server time"):
        await client.send_message(message.channel, datetime.datetime.now())
    elif contains(message.content, "subscribe "):
        desired_sub = message.content.split("subscribe ")[1]
        conn = sqlite3.connect("subscriptions.sqlite")
        c = conn.cursor()
        print("desired sub is " +desired_sub)
        if desired_sub == "all":
            if "unsubscribe" not in message.content:
                c.execute("UPDATE {tn} SET ebook = 1, poem = 1 WHERE id = ?".format(tn="Subscriptions"), (message.author.id,))
                await client.send_message(message.channel, "Subscribing you to both!")
            else:
                c.execute("UPDATE {tn} SET ebook = 0, poem = 0 WHERE id = ?".format(tn="Subscriptions"), (message.author.id,))
                await client.send_message(message.channel, "Removing you from all subscriptions")

        elif desired_sub == "ebook" or desired_sub == "poem":
            c.execute("SELECT {sub} from Subscriptions WHERE id = ?".format(sub=desired_sub), (message.author.id,))
            rows = c.fetchall()
            val = (int(rows[0][0]) + 1)%2
            c.execute("UPDATE {tn} SET {sub} = ? WHERE id = ?".format(tn="Subscriptions", sub=desired_sub), (val, message.author.id,))
            await client.send_message(message.channel,"Changed subscription status {} to ".format(val)+desired_sub)
        conn.commit()
        conn.close()
        """Have a database where rows are user IDs and columns are various types of subscription- default to 0, 1 means tag, 2 means message, 3 means tag and message
@bot subscribe 2 ebook
edit row value
@bot unsubscribe ebook
edit row value to 0

ebookAnnounced.txt, poemAnnounced.txt
both contain digits of last date/time announced
if not within current timeframe, wipe files and replace with current time
then do tagged message:
query where user's values for ____ = 1 or 3, then assemble a string
then do messages:
query, then look up users by ID, and message

@bot unsubscribe all
query ID, turn all values to 0

@bot subscribe new or help
Talks about digit and usage system"""
    else:#default case for usage
        await client.send_message(message.channel, """*@Ozymandias up tonight?*
Lets you know if I'm accepting commands
*@Ozymandias Markov <username>*
Takes messages sent recently in #help_corner and generates new text from <username> (defaults to self). No error handling, so it will probably crash if you're not active there.
*@Ozymandias search <pageNumber> <regex>*
Retrieves page of ebook search results for specified regex (defaults to first page and basic string search)
*@Ozymandias SING!*
Grab a chair and listen to me hum a few bars from the Weather Girls
*@Ozymandias weather*
Fetches the current weather outside
*@Ozymandias (un)subscribe <arg>*
Signs you up to be tagged (or removes you from the list) for the ebook, poem, or all (use those 3 keywords)""")

@asyncio.coroutine
def main_task(token):
    yield from client.login(token)
    yield from client.connect()



key = open('appkey.txt', 'r')#Read API key from text file in directory (which git ignores)
thekey = key.read()
key.close()
#client.run(thekey)#Initialize a connection using application token
loop = asyncio.get_event_loop()
try:
    loop.run_until_complete(main_task(thekey))
except:
    loop.run_until_complete(client.logout())
finally:
    loop.close()
print("Finished completely.")

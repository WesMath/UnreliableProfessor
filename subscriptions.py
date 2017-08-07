import discord
import sqlite3
from bs4 import BeautifulSoup
import datetime
from urllib.request import Request, urlopen

client = discord.Client()

@client.event
async def on_ready():
    print("Logged in successfully.")
    for serv in client.servers:
        the_server = serv
    for chan in the_server.channels:
        #print(chan.name)
        if chan.name == "bot_testing":
            print("Found correct channel")
            testing = chan
            await client.send_message(testing, "I'm keeping my activities confined to here; don't you worry, Kapusta.")
    conn = sqlite3.connect("subscriptions.sqlite")
    c = conn.cursor()
    
    c.execute("SELECT id FROM Subscriptions WHERE ebook = 1")
    da_people = c.fetchall()
    print(da_people)
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
    now = datetime.datetime.now()
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

    c.execute("SELECT id FROM Subscriptions WHERE poem = 1")
    da_people = c.fetchall()
    print(da_people)
    #await client.send_message(testing, "I got a poem for you- just kidding, this is a placeholder.")
    day = datetime.date.today()
    #31 days in a month to prevent overlap
    hashable = day.month*31 + day.day
    await client.send_message(testing,"The poem of the day is:\nhttp://www.bartleby.com/265/"+str((421*hashable)%424)+".html")
    #use coprimes to generate unique nums
    output = ""
    for person in da_people:
        output += "<@"+person[0]+">, "
    await client.send_message(testing, output)

key = open('appkey.txt', 'r')#Read API key from text file in directory (which git ignores)
thekey = key.read()
key.close()
client.run(thekey)#Initialize a connection using application token

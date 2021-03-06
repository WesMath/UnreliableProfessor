import discord
import sqlite3
from bs4 import BeautifulSoup
import datetime
from urllib.request import Request, urlopen
import sys
import time


client = discord.Client()

"""
/home/ec2-user/discord_bot/UnreliableProfessor/
kill $(ps aux | grep -m 1 subscriptionspy | grep -Po 'ec2-user \d+ ' | grep -Po '\d\d+')
"""
@client.event
async def on_ready():
    print("Logged in for the first time")
    global the_server
    for serv in client.servers:
        the_server = serv
    while(True):
        #Sleep after checking time:
        now = datetime.datetime.now()
        desired = -1
        secs = 1
        if now.hour >= 7 and now.hour < 19:
            desired = 1 #for ebook
            t = datetime.timedelta(hours=17, minutes=35)
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
        #secs = 1 #OVERRIDE FOR DEBUGGING PURPOSES
        print("Ready to sleep for {} seconds.".format(secs))
        time.sleep(secs)
        #Send out appropriate message
        for chan in the_server.channels:
            #print(chan.name)
            if chan.name == "resources":
                print("Found correct channel")
                testing = chan
                #await client.send_message(testing, "THIS IS NOT WORKING AND DRIVING ME MAD")
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
        """ValueError: sleep length must be non negative
           Ready to sleep for 0.0 seconds
           Ready to sleep for -60.0 seconds
           Found correct channel
           One user listed"""
        c.close()
        time.sleep(120) #Prevents repeated calling


key = open('appkey.txt', 'r')#Read API key from text file in directory (which git ignores)
thekey = key.read()
key.close()
client.run(thekey)#Initialize a connection using application token
print("got here")

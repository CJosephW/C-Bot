import discord
import os
from os import environ
import tweepy
import random
from datetime import date
from discord.ext import tasks, commands
from discord.ext.tasks import loop
import requests
import json
import asyncio
#r = requests.get("https://api.tenor.com/v1/search_suggestions?key=%s&q=%s&limit=%s" % (apikey, search, lmt))

consumer_key= environ.get("TWITTER_CONSUMER_KEY")
consumer_secret=environ.get("TWITTER_CONSUMER_SECRET")
access_token_key=environ.get("TWITTER_ACCESS_KEY")
access_token_secret=environ.get("TWITTER_TOKEN_SECRET")

tenor_key = environ.get("TENOR_KEY")

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token_key, access_token_secret)

api = tweepy.API(auth)

birthday_gif = 'happy birthday'

birthday_dict = {
    "<@!157658976434126848>" : "04/04"
}

r = requests.get("https://api.tenor.com/v1/search?key=%s&q=%s&limit=%s" % (tenor_key, birthday_gif, 50))
print("https://api.tenor.com/v1/search?key=%s&q=%s&limit=%s" % (tenor_key, birthday_gif, 50))
data = r.content
gif_json = json.loads(data)
print(gif_json)
gif_urls = []
for gif in gif_json['results']:
    gif_urls.append(gif['url'])

birthday_wish_channel = 616731567439478785
TOKEN = environ.get('CBOT_TOKEN')
client = discord.Client()


    
@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')
    
@client.event
async def on_message(message):
    print(message.author.name)
    if message.author == client.user:
        return
    print(message.content)
     #recent_tweets = api.user_timeline(screen_name = user, count = 200)

    if 'randomtweet' in message.content.lower():
        message_split = message.content.split()
        usern = message_split[1]
        recent_tweets = []
        for item in tweepy.Cursor(api.user_timeline, screen_name=usern, count=1300,since_id=None, max_id=None,trim_user=True,exclude_replies=True,contributor_details=False,include_entities=False ).items(1300):
                recent_tweets.append(item)

        random_tweet_int = random.randint(0, len(recent_tweets))

        random_tweet = recent_tweets[random_tweet_int]

        await message.channel.send(f"https://twitter.com/{usern}/status/{random_tweet.id}")

    if 'add-birthday' in message.content.lower():
        sorted_message = message.content.split()

        birthday_dict[sorted_message[1]] = sorted_message[2]
        await message.channel.send('added %s on %s' %(sorted_message[1], sorted_message[2]))
    if 'cpoll' in message.content.lower():

        message_channel = client.get_channel(367796816625926146)

        #and str(reaction.emoji) == '✅'

        poll_message = await message_channel.send(f"***{message.content[6:]}***")
        await poll_message.add_reaction(emoji ='✅')
        await poll_message.add_reaction(emoji = '❌')
        
        check_count = 1
        cross_count = 1
        def pred(m):
            return m.author == message.author and m.channel == message.channel
            
        try:
            msg = await client.wait_for('end_poll', check=pred, timeout=60.0)

        except asyncio.TimeoutError:
            await message_channel.send('You took too long...')
        else:
            await message_channel.send('poll ended')


@tasks.loop(hours = 24)
async def check_birthdays():
    print('fuck off')
    message_channel = client.get_channel(616731567439478785)
    today = date.today()
    d3 = today.strftime("%m/%d")
    for key in birthday_dict:
        if birthday_dict[key] == d3:
            gif_int = random.randint(0, len(gif_urls))
            await message_channel.send('Happy Birthday %s \n %s' % (key, gif_urls[gif_int]))

@check_birthdays.before_loop
async def before_check():
    await client.wait_until_ready()

    print('bot ready')
client.run(TOKEN)
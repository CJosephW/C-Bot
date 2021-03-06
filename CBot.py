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
import requests

url = "your imgur album api link"

consumer_key= environ.get("TWITTER_CONSUMER_KEY")
consumer_secret=environ.get("TWITTER_CONSUMER_SECRET")
access_token_key=environ.get("TWITTER_ACCESS_KEY")
access_token_secret=environ.get("TWITTER_TOKEN_SECRET")


payload = {}
files = {}
headers = {
    'Authorization' : 'Client-ID your client id'
}

response = requests.request("GET", url, headers=headers, data = payload, files = files)

print(response.text.encode('utf8'))

tenor_key = environ.get("TENOR_KEY")

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token_key, access_token_secret)

api = tweepy.API(auth)

birthday_gif = 'happy birthday'

birthday_dict = {
}

r = requests.get("https://api.tenor.com/v1/search?key=%s&q=%s&limit=%s" % (tenor_key, birthday_gif, 50))
print("https://api.tenor.com/v1/search?key=%s&q=%s&limit=%s" % (tenor_key, birthday_gif, 50))
data = r.content
gif_json = json.loads(data)
gif_urls = []
for gif in gif_json['results']:
    gif_urls.append(gif['url'])

imgur_content = response.content
imgur_response = json.loads(imgur_content)

cameron_pictures = []
for picture in imgur_response['data']:
    cameron_pictures.append(picture['link'])
    print(picture['link'])

birthday_wish_channel = 616731567439478785
TOKEN = environ.get('CBOT_TOKEN')
client = discord.Client()


    
@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')
    
@client.event
async def on_message(message):

    if message.author == client.user:
        return

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

    if 'cool_guy' in message.content.lower():
        random_picture = random.choice(cameron_pictures)
        await message.channel.send(random_picture)
    if 'cpoll' in message.content.lower():
        message_channel = client.get_channel(616731567439478785)
        poll_message = await message.channel.send(f"***{message.content[6:]}***")
        
        await poll_message.add_reaction(emoji ='✅')
        await poll_message.add_reaction(emoji = '❌')

        def pred(m):
            return m.author == message.author and m.channel == message.channel and m.content == "end_poll"
            
        try:
            msg = await client.wait_for('message', check=pred, timeout=1000.0)
            reactions = (await message_channel.fetch_message(poll_message.id)).reactions
            check_count = 0
            cross_count = 0

            for reaction in reactions:
                if reaction.emoji == '✅':
                    check_count = reaction.count
                if reaction.emoji == '❌':
                    cross_count = reaction.count

            if check_count > cross_count:
                await message_channel.send(f'The poll has ened with overall vote being ***YES*** (YES: {check_count}, NO: {cross_count})')
            if check_count < cross_count:
                await message_channel.send(f'The poll has ened with overall vote being ***NO*** (YES: {check_count}, NO: {cross_count})')
            if check_count == cross_count:
                await message_channel.send('***POLL RESULT***: \n https://tenor.com/view/mark-wahlberg-wahlberg-tie-oscar-gif-9081826')
            await poll_message.delete()

        except asyncio.TimeoutError:
            await message_channel.send('The timer has run out here are the results')
            
            if check_count > cross_count:
                await message_channel.send(f'The poll has ened with overall vote being ***YES*** (YES: {check_count}, NO: {cross_count})')
            if check_count < cross_count:
                await message_channel.send(f'The poll has ened with overall vote being ***NO*** (YES: {check_count}, NO: {cross_count})')
            if check_count == cross_count:
                await message_channel.send('***POLL RESULT***: \n https://tenor.com/view/mark-wahlberg-wahlberg-tie-oscar-gif-9081826')
            
            await poll_message.delete()


@tasks.loop(hours = 24)
async def check_birthdays():
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
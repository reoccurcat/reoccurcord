# Copyright (C) 2021-present reoccurcat
# This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
# You should have received a copy of the GNU General Public License along with this program.  If not, see <http://www.gnu.org/licenses/>.


###### SORTED IMPORTS FOR CLEANER LOOK ######

from ast import alias
import config
import random
import aiohttp
import discord  # removed "from discord import embeds", doesn't do anything
import requests
import asyncio
import os
import importlib
import sys
import shutil
import json
import cryptography
import binascii
#import time
#import concurrent.futures
#import bot
#import psutil 
from discord.ext import commands
from cryptography.fernet import Fernet
from bs4 import BeautifulSoup
from discord.ext import commands

##############################################

"""
requests and urllib are blocking. Do not use these libraries within your asynchronous code. 
(http://discordpy.readthedocs.io/en/latest/faq.html#what-does-blocking-mean)

discord.py uses aiohttp, so it should already be installed.
"""

async def getdata(url):  # switch from requests module to aiohttp (see above for reason)
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            r = await response.text()  
    return r

class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.cooldown(1,5,commands.BucketType.user)
    async def add(self, ctx, *numbers): # creates a list of input (I haven't typecasted to (int) due to multitude of reasons)
        """Adds multiple numbers together"""
        if len(numbers) <= 1:
            return await ctx.reply("Provide at least two or more numbers!", mention_author=False)
        new_list = [] # initializing new list
        for number in numbers: # iterating over the original list of numbers
            try:
               new_number = float(number) # conver the output to integer
               new_list.append([new_number, str(number)])
               continue # append the converted string along with the string as a list
            except (TypeError, ValueError):
               continue # if a string is passed, pass it
        equation = " + ".join([num[1] for num in new_list]) #iterate over our new_list to get the string part of numbers and join them
        total = sum([num[0] for num in new_list]) # iterate over the new_list and add all the appended float numbers together
        em = discord.Embed(title = f"**__Input:__**\n```py\n{equation}\n```\n**__Output:__**\n```py\n{total}\n```", color = discord.Color.blue()) # send both the input and output
        await ctx.reply(embed=em, mention_author=False)

    
    @commands.command(aliases=['choices'])
    @commands.cooldown(1,5,commands.BucketType.user)
    async def choose(self, ctx, *, choices):
        '''Chooses randomly between multiple choices'''
        if "@everyone" in choices or "@here" in choices:
            em = discord.Embed(title = "Nice try, sadly that won't work here.", color = discord.Color.red())
            return await ctx.reply(embed=em, mention_author=False)
        em = discord.Embed(title = random.choice(choices), color = discord.Color.blue())
        await ctx.reply(embed=em, mention_author=False)
        
    @commands.command()
    @commands.cooldown(2,8,commands.BucketType.user)
    async def deadchat(self, ctx):
        # totally useful command btw
        await ctx.message.delete()
        rand = random.randint(1,3)
        em = discord.Embed(title="dead chat xd", color=discord.Color.blue())
        if rand == 1:
            em.set_image(url="https://images-ext-2.discordapp.net/external/VkYcIzxshSNt1r63cWY9zMP9aEi6XGI5BkaS-Y8l8sM/https/media.discordapp.net/attachments/841435792274751519/847285207349854208/deadchat.gif")
        elif rand == 2:
            em.set_image(url="https://media.discordapp.net/attachments/850045054923964447/855157429968568360/tenor_1.gif")
        elif rand == 3:
            em.set_image(url="https://tenor.com/view/chat-dead-gif-18627672")
        await ctx.send(embed=em)
    
    @commands.command(aliases=["emote"])
    @commands.cooldown(1,10,commands.BucketType.user)
    async def emoji(self, ctx, emoji : discord.Emoji = None):
        """Gets the info of an emoji"""
        if emoji is None:
            em = discord.Embed(title="No emoji given", description = f"Please use `{config.prefix}emoji <emoji>`.", color = discord.Color.red())
            await ctx.reply(embed=em, mention_author=False)
        try:
            em = discord.Embed(timestamp=emoji.created_at, color = discord.Color.blue())
            em.set_author(name=emoji.name, icon_url=emoji.url)
            em.set_thumbnail(url=emoji.url)
            em.set_footer(text="Created on")
            em.add_field(name="ID", value=emoji.id)
            em.add_field(name="Usage", value=f"`{emoji}`")
            em.add_field(name="URL", value=f"[click here]({emoji.url})") # masked links instead of actually sending the full link
            await ctx.reply(embed=em, mention_author=False)
        except IndexError:
            em = discord.Embed(title="Error", description="There was an error fetching the emoji. The most likely cause is that it's from a server the bot isn't in.", color = discord.Color.red())

    @commands.command()
    @commands.cooldown(1,10,commands.BucketType.user)
    async def f(self, ctx, *, message2):
        """Puts an interative 'f in the chat' embed into the chat"""
        em = discord.Embed(title = f"F in the chat to: **{message2}**", color=discord.Color.blue())
        msg = await ctx.reply(embed=em, mention_author=False)
        await msg.add_reaction('🇫')
        def check(reaction, user):
            return msg == reaction.message
        usersreacted = []
        donotaccept = self.bot.user.name
        while True:
            try:
                reaction, user = await self.bot.wait_for('reaction_add', check=check, timeout=30)
            except asyncio.TimeoutError:
                new_msg = await ctx.fetch_message(msg.id)
                number = len([x for x in await new_msg.reactions[0].users().flatten() if not x.bot])
                em3 = discord.Embed(title = f"F in the chat to: **{message2}**", color=discord.Color.blue())
                multipleusers = f"{', '.join(usersreacted)}"
                em3.add_field(name="Users who paid respects", value=f"{multipleusers}\n**A total of {number} people paid their respects.**")
                return await msg.edit(embed=em3)
                #return await ctx.send(f"A total of {number} people paid their respects to **{message2}**.")
            else:
                #try:
                #    for user in usersreacted:
                #        emoji = self.bot.emoji
                #        await msg.remove_reaction("🇫", user.id)
                #except discord.Forbidden:
                #    pass
                if str(reaction.emoji) == "🇫":
                    if user.name in usersreacted:
                        continue
                    if user.name == donotaccept:
                        continue
                    usersreacted.append(user.name)
                    #await ctx.send(f"**{user.name}** has paid their respects.")
                    em2 = discord.Embed(title = f"F in the chat to: **{message2}**", color=discord.Color.blue())
                    multipleusers = f"{', '.join(usersreacted)}"
                    em2.add_field(name="Users who paid respects", value=f"{multipleusers}")
                    await msg.edit(embed=em2)

    @commands.command(aliases=['img', 'findimage', 'fetchimage'])
    @commands.cooldown(1,30,commands.BucketType.user)
    async def image(self, ctx, *, query):
        """Search for images using searx"""
        query = query.replace(" ", "+")
        embed = discord.Embed(title="Image Search")
        embed.set_author(name=f"{ctx.author.name}#{ctx.author.discriminator}", icon_url=ctx.author.avatar_url)
        if not os.path.exists('cache'):
            os.makedirs('cache')
        if os.path.isfile(f'cache/{query}.py'):
            sys.path.insert(0, './cache')
            #print("Using cache file:\n")
            importedquery = importlib.import_module(f"{str(query)}")
            images = importedquery.cache
            embed.set_footer(text=f"Images from this query currently are from the cache.\nTo clear the cache, try running {config.prefix}help clearcache")
        else:
            images = []
            htmldata = await getdata(f'https://searx.prvcy.eu/search?q={query}&categories=images')
            #print(f"https://www.bing.com/images/search?q={str(newquery)}")
            soup = BeautifulSoup(htmldata, 'html.parser')
            for item in soup.find_all('img'):
                if "explicit" not in str(item):
                    try:
                        replace1 = item['src'].replace("%3A", ":")
                        replace2 = replace1.replace("%2F", "/")
                        if "gstatic" in replace2:
                            replace3 = replace2.replace("%3F", "?")
                            replace4 = replace3.replace("%3D", "=")
                            replace5 = replace4.replace("%26", "?")
                            lefttext = replace5.split("?usqp")[0]
                            replace6 = lefttext.replace("?usqp", "")
                            righttext = replace6.split("/image_proxy?url=")[1]
                            #print(righttext)
                            images.append(righttext)
                        else:
                            replace3 = replace2.replace("%3F", "/")
                            replace4 = replace3.replace("%3D", "/")
                            replace5 = replace4.replace("%26", "?")
                            righttext = replace5.split("/image_proxy?url=")[1]
                            #print(righttext)
                            images.append(righttext)
                        f = open(f"cache/{query}.py", "w")
                        f.write(f"cache = {images}")
                        f.close()
                        embed.set_footer(text="Images of your query were cached.")
                    except Exception as e:
                        #print(e)
                        pass                        
        printimage = random.choice(images)
        embed.set_image(url=printimage)
        await ctx.reply(embed=embed, mention_author=False)


    @commands.command()
    @commands.cooldown(2,5,commands.BucketType.user)
    async def listcache(self, ctx):
        """Lists the image/web search cache files"""
        try:
            em = discord.Embed(title="Image Cache Files", description=f"`{', '.join(os.listdir('./cache/'))}`", color=discord.Color.blue())
            await ctx.reply(embed=em, mention_author=False)
        except OSError:
            em = discord.Embed(title="Error", description="No cache folder could be found.", color=discord.Color.red())
            await ctx.reply(embed=em, mention_author=False)


    @commands.command()
    @commands.cooldown(2,5,commands.BucketType.user)
    async def clearcache(self, ctx, cachefile = None):
        """Clears the image cache"""
        try:
            cachefile = cachefile.replace(" ", "+")
        except AttributeError:
            pass
        if cachefile is None:
            shutil.rmtree("./cache")
            em = discord.Embed(title="Image Cache Directory Cleared", description="The `./cache` directory has been cleared. Images will take a few seconds longer to fetch as they recache.", color=discord.Color.green())
            await ctx.reply(embed=em, mention_author=False)
        else:
            if os.path.isfile(f'cache/{cachefile}.py'):
                os.remove(f"./cache/{cachefile}.py")
                em = discord.Embed(title="Image Cache Directory Cleared", description=f"The `./cache/{cachefile}.py` file has been deleted. Images will take a few seconds longer to fetch as they recache.", color=discord.Color.green())
                await ctx.reply(embed=em, mention_author=False)
            else:
                em = discord.Embed(title="No cache file found.", description=f"There was no cache file found at `./cogs/{cachefile}.py`.", color=discord.Color.red())
                await ctx.reply(embed=em, mention_author=False)
                
    @commands.command(aliases=['rd'])
    @commands.cooldown(2,5,commands.BucketType.user)
    async def reddit(self, ctx, *, name):
        """Gets a random post from a subreddit on Reddit"""
        posts = []
        subreddit = f"{name}"
        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://www.reddit.com/r/{subreddit}/.json") as r:
                response = await r.json()
                try:
                 for i in response['data']['children']:
                    posts.append(i['data'])
                except KeyError:
                    return await ctx.reply("The subreddit you provided doesn't exist!", mention_author=False)
                try:
                 post = random.choice([p for p in posts if not p['stickied'] or p['is_self']])
                except IndexError:
                    return await ctx.reply("The subreddit you provided doesn't exist!", mention_author=False)
                if post['over_18'] is True and ctx.channel.nsfw is False:
                    return await ctx.reply("Failed to get a post from that subreddit, try again in an NSFW channel.", mention_author=False)
                title = str(post['title'])
        embed=discord.Embed(title=f'{title}', colour=0xaf85ff, url=f"https://reddit.com/{post['permalink']}")
        embed.set_footer(text=f"{post['upvote_ratio'] * 100:,}% Upvotes | Posted to r/{post['subreddit']}")
        embed.set_image(url=post['url'])
        await ctx.reply(embed=embed, mention_author=False)
    
    @commands.command(aliases=['weblook', 'websitepic', 'webpic'])
    @commands.cooldown(1,30,commands.BucketType.user)
    async def websitepeek(self, ctx, *, url: str):
        """Gets a screenshot of a website"""
        async with ctx.typing(), aiohttp.ClientSession() as session:
            screener = "http://magmachain.herokuapp.com/api/v1"
            async with session.post(screener, headers=dict(website=url)) as r:
                website = (await r.json())["snapshot"]
                em = discord.Embed(color=discord.Color.blue())
                em.set_image(url=website)
                await ctx.reply(embed=em, mention_author=False)

    @commands.command(aliases=['search', 'searx', 'google'])
    @commands.cooldown(1,30,commands.BucketType.user)
    async def websearch(self, ctx, *, query):
        """Searches the web for whatever you have it search for and returns a list of links"""
        query = query.replace(" ", "+")
        if not os.path.exists('cache'):
            os.makedirs('cache')
        if os.path.isfile(f'cache/{query}_web.py'):
            sys.path.insert(0, './cache')
            #print("Using cache file:\n")
            importedquery = importlib.import_module(f"{str(query)}_web")
            allresults = importedquery.cache
        else:
            htmldata = await getdata(f'https://searx.prvcy.eu/search?q={query}')
            #print(f"https://www.bing.com/images/search?q={str(newquery)}")
            soup = BeautifulSoup(htmldata, 'html.parser')
            allresults = []
            for item in soup.find_all("a"):
                #print(item)
                item = str(item).split('" rel=')[0]
                try:
                    item = str(item).split('href="')[1]
                    if item[0] == "/":
                        continue
                    if "</a>" in item:
                        continue
                    if str(query) not in item:
                        continue
                    if "archive" in item:
                        continue
                    try:
                        item = item.split("?")[0]
                    except:
                        pass
                    allresults.append(item)
                except Exception as e:
                    print(e)
                    pass
            for item in soup.find_all("aria-labelledby"):
                print(item)
            if '"' in query:
                query = query.replace('"', "'")
            f = open(f"cache/{query}_web.py", "w")
            f.write(f"cache = {allresults}")
            f.close()
        em = discord.Embed(title="Web Search Results", description=f"reoccurcord found **{len(allresults)}** results.")
        try:
            em.add_field(name="URLs Returned", value="\n".join(allresults))
        except Exception:
            em.add_field(name="Error", value="Too many urls fetched (dev is working on a fix)")
        await ctx.reply(embed=em, mention_author=False)

    @commands.command(aliases=['anime'])
    @commands.cooldown(1,15,commands.BucketType.user)
    async def animeinfo(self, ctx, query):
        """Gets info on an anime"""
        try:
            query = query.replace(" ", "%20")
            apiurl = f"https://kitsu.io/api/edge/anime?filter[text]={str(query)}&page[limit]=1"
            r = requests.get(apiurl).text
            data = json.loads(str(r)) 

            em = discord.Embed(color=discord.Color.blue())
            em.set_thumbnail(url=data["data"][0]["attributes"]["posterImage"]["original"])
            languages = ["en", "en_jp", "en_us", "ja_jp"]
            usablelangs = []
            language2 = []
            langen = 0
            for lang in languages:
                try:
                    language = data["data"][0]["attributes"]["titles"][f"{lang}"]
                    #language = lang
                    if langen == 1:
                        if lang == "en_us":
                            continue
                        elif lang == "en":
                            continue
                    else:
                        if lang == "en_us":
                            lang = lang.replace("en_us", "English (en_us): ") 
                            langen = 1
                        elif lang == "en":
                            lang = lang.replace("en", "English (en): ")
                            langen = 1
                    lang = lang.replace("en_us", "English (en_us): ").replace("en_jp", "English (en_jp): ").replace("ja_jp", "Japanese (ja_jp): ".replace("en", "English (en): "))
                    usablelangs.append(f"{lang}{language}")
                except KeyError:
                    continue
            em.set_author(name="Anime Info")
            em.add_field(name="Anime Name", value=f"\n".join(usablelangs))
            em.add_field(name="Description", value=data["data"][0]["attributes"]["description"].split("\n")[0])
            em.add_field(name="Status", value=data["data"][0]["attributes"]["status"])
            em.add_field(name="Age Rating", value=f'{data["data"][0]["attributes"]["ageRating"]} | {data["data"][0]["attributes"]["ageRatingGuide"]}')
            await ctx.reply(embed=em, mention_author=False)
            #print(data["data"][0]["attributes"]["titles"]["en"] + " (" + data["data"][0]["attributes"]["titles"]["ja_jp"] + ')\n')
            #print(data["data"][0]["attributes"]["synopsis"] + '\n')
            #print(data["data"][0]["attributes"]["status"])
            #print(data["data", "0", "attributes"])
        except IndexError:
            em = discord.Embed(title="Error", color=discord.Color.red())
            em.add_field(name="There was an error running the command", value="The bot probably couldn't find an anime with that name.")
            await ctx.reply(embed=em, mention_author=False)

    @commands.command(aliases=['kitty', 'kitten', 'cat'])
    @commands.cooldown(1,10,commands.BucketType.user)
    async def catpic(self, ctx):
        """Gets a photo of a cat"""
        apiurl = "https://api.thecatapi.com/v1/images/search"
        r = requests.get(apiurl).text
        #print(r)
        data = json.loads(r) 
        #print(data)
        em = discord.Embed(color=discord.Color.blue())
        #em.set_thumbnail(url=str(data["url"][0]))
        caticon = 'http://icons.iconarchive.com/icons/google/noto-emoji-animals-nature/1024/22221-cat-icon.png'
        em.set_author(name="Cat Picture", icon_url=caticon)
        for item in data:
            em.set_image(url=item["url"])
        await ctx.reply(embed=em, mention_author=False)

    @commands.command(aliases=['identifyanime'])
    @commands.cooldown(1,15,commands.BucketType.user)
    async def findanime(self, ctx, link=None):
        """Finds an anime from an attached image. This command will take attached media and links."""
        try:
            if link is None:
                link = ctx.message.attachments[0].url
            apiurl = f"https://api.trace.moe/search?url={link}"
            r = requests.get(apiurl).text
            #print(r)
            data = json.loads(r) 
            #print(data)
            em = discord.Embed(color=discord.Color.blue())
            #em.set_thumbnail(url=str(data["url"][0]))
            #print(data)
            # Here we define our query as a multi-line string
            query = '''
            query ($id: Int) { # Define which variables will be used in the query (id)
            Media (id: $id, type: ANIME) { # Insert our variables into the query arguments (id) (type: ANIME is hard-coded in the query)
                id
                title {
                romaji
                english
                native
                }
            }
            }
            '''
            # Define our query variables and values that will be used in the query request
            variables = {
                'id': data["result"][0]["anilist"]
            }
            url = 'https://graphql.anilist.co'
            # Make the HTTP Api request
            response = requests.post(url, json={'query': query, 'variables': variables}).text
            data2 = json.loads(response)
            languages = ["english", "romaji", "native"]
            usablelangs = []
            for lang in languages:
                if data2["data"]["Media"]["title"][f'{lang}'] is not None:
                    if lang == "native":
                        lang2 = "japanese (native)"
                    else:
                        lang2 = lang
                    usablelangs.append(f"{lang2}: " + data2["data"]["Media"]["title"][str(lang)])
            em.set_author(name="Anime Identifier")
            #print(data)
            em.set_thumbnail(url=str(data["result"][0]["image"]))
            em.add_field(name="Anime Names", value=str('\n'.join(usablelangs)))
            em.add_field(name="Episode", value=data["result"][0]["episode"])
            percent = data["result"][0]["similarity"]
            percent = percent*100
            em.add_field(name="Similarity", value=str(round(percent, 2)))
            link = str(data["result"][0]["video"])
            em.add_field(name="Matched Clip", value=f'[Video Link]({link})')
            em.set_footer(text=f"Try running {config.prefix}animeinfo with the anime name to get more info!")
            await ctx.reply(embed=em, mention_author=False)
        except KeyError:
            em = discord.Embed(title="Error", color=discord.Color.red())
            em.add_field(name="There was an error running the command", value="You may have not provided a valid input. The bot will only accept images/videos/gifs either with the link provided or attached to the message. Another cause could have been the bot maybe didn't find an anime.")
            await ctx.reply(embed=em, mention_author=False)

    @commands.command(aliases=["encrypt", "encryptmessage"])
    @commands.cooldown(1,15,commands.BucketType.user)
    async def encryptmsg(self, ctx, *, message):
        """Encrypts your message with a random key that is generated and messaged to you."""
        message = bytes(message, "utf-8")
        await ctx.message.delete()
        key = Fernet.generate_key()
        encrypted = Fernet(key).encrypt(message)
        embed = discord.Embed(title="Encrypted message", description=f"`{encrypted.decode()}`", color=discord.Color.blue())
        embed.set_author(name=f"{ctx.author.name}#{ctx.author.discriminator}", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)
        user = self.bot.get_user(ctx.message.author.id)
        embed = discord.Embed(title="Encryption Key", description=f"Your decryption key is `{key.decode()}`.", color=discord.Color.blue())
        embed.set_author(name=f"{ctx.author.name}#{ctx.author.discriminator}", icon_url=ctx.author.avatar_url)
        await user.send(embed=embed)


    @commands.command(aliases=["decrypt", "decryptmessage"])
    @commands.cooldown(1,15,commands.BucketType.user)
    async def decryptmsg(self, ctx, *, message):
        """Decrypts your encrypted message. Requires the encryption key."""
        def check(message: discord.Message):
            return message.channel == ctx.channel and message.author != ctx.me
        embed = discord.Embed(title="Decryption Key", description="Please put in the key that was provided with the encrypted message.", color=discord.Color.blue())
        embed.set_author(name=f"{ctx.author.name}#{ctx.author.discriminator}", icon_url=ctx.author.avatar_url)
        msg = await ctx.send(embed=embed)
        providekey = await self.bot.wait_for('message', check=check)
        key = bytes(providekey.content, "utf-8")
        await providekey.delete()
        try:
            decrypted = Fernet(key).decrypt(bytes(message, "utf-8"))
            embed = discord.Embed(title="Decrypted message", description=f"`{decrypted.decode()}`", color=discord.Color.blue())
            embed.set_author(name=f"{ctx.author.name}#{ctx.author.discriminator}", icon_url=ctx.author.avatar_url)
            await msg.edit(embed=embed)
        except (cryptography.fernet.InvalidToken, TypeError, binascii.Error):
            embed = discord.Embed(title="Error", description="This is the incorrect key to decrypt this message.", color=discord.Color.red())
            embed.set_author(name=f"{ctx.author.name}#{ctx.author.discriminator}", icon_url=ctx.author.avatar_url)
            await msg.edit(embed=embed)

def setup(bot):
    bot.add_cog(Fun(bot))

# Copyright (C) 2021-present reoccurcat
# This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
# You should have received a copy of the GNU General Public License along with this program.  If not, see <http://www.gnu.org/licenses/>.


###### SORTED IMPORTS FOR CLEANER LOOK ######

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
import aiofiles
from discord.ext import commands
from cryptography.fernet import Fernet
from bs4 import BeautifulSoup
from nudenet import NudeClassifier
from nudenet import NudeDetector

classifier = NudeClassifier()
detector = NudeDetector()
sys.path.insert(0, "data/roleplay")

async def getdata(url):  # switch from requests module to aiohttp (see above for reason)
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            r = await response.text()  
    return r

async def downloadimage(url):
    if not os.path.exists("cache"):
        os.mkdir("cache")
    tempimage = f"cache/tempimage{random.randint(1, 10)}.jpg"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            f = await aiofiles.open(tempimage, mode='wb')
            await f.write(await response.read())
            await f.close()
    return tempimage

async def getunsafe(url, censor=None):
    threshold = 25
    tempimage = f"cache/tempimage{random.randint(1, 10)}.jpg"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            f = await aiofiles.open(tempimage, mode='wb')
            await f.write(await response.read())
            await f.close()
    if censor is not None:
        censoredimage = f'{tempimage.split(".")[0]}-censored.jpg'
        detector.censor(tempimage, out_path=censoredimage, visualize=False)
    detection = classifier.classify(tempimage)
    detection = detection[tempimage]["unsafe"]
    detection = detection*100
    detection = round(detection, 2)
    os.remove(tempimage)
    if detection >= threshold:
        nsfw = True
        if censor is not None and censoredimage is not None:
            try:
                if bool(censoredimage):
                    if detection >= threshold:
                        return nsfw, detection, censoredimage
            except UnboundLocalError:
                censoredimage = False
                return nsfw, detection, censoredimage
        else:
            censoredimage = False
            return nsfw, detection, censoredimage
    else:
        nsfw = False
        censoredimage = False
        return nsfw, detection, censoredimage

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
        em = discord.Embed(title = "Adding", color = discord.Color.blue()) # send both the input and output
        em.add_field(name="**__Input__**", value=f"```py\n{str(equation)}\n```")
        em.add_field(name="**__Output__**", value=f"```py3\n{str(total)}\n```")
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
    #@commands.cooldown(1,30,commands.BucketType.user)
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
            em = discord.Embed(title="Image Search", description="Images are getting cached. Please wait...")
            em.set_author(name=f"{ctx.author.name}#{ctx.author.discriminator}", icon_url=ctx.author.avatar_url)
            await ctx.reply(embed=em)
            images = []
            htmldata = await getdata(f'https://searx.bar/search?q={query}&categories=images')
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
                        print(e)                        
        printimage = random.choice(images)
        if not isinstance(ctx.channel, discord.channel.DMChannel):
            if ctx.channel.nsfw is False:
                nsfw, detection, censoredimage = await getunsafe(printimage)
                if nsfw is True:
                    embed = discord.Embed(title="Possible NSFW Blocked!", color=discord.Color.red()) 
                    embed.add_field(name="Detection Percent", value=str(detection))
                    embed.add_field(name="What is this?", value="This bot automatically finds and blocks NSFW (Not Safe For Work) content. This content was detected as NSFW.")
                    await ctx.send(embed=embed)
                    return
        else:
            nsfw, detection, censoredimage = await getunsafe(printimage)
            if nsfw is True:
                embed = discord.Embed(title="Possible NSFW Blocked!", color=discord.Color.red()) 
                embed.add_field(name="Detection Percent", value=str(detection))
                embed.add_field(name="What is this?", value="This bot automatically finds and blocks NSFW (Not Safe For Work) content. This content was detected as NSFW.")
                await ctx.send(embed=embed)
                return
        embed.set_image(url=printimage)
        await ctx.send(embed=embed)


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
            htmldata = await getdata(f'https://searx.bar/search?q={query}')
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
                    except AttributeError:
                        pass
                    allresults.append(item)
                except Exception as e:
                    print(e)
            for item in soup.find_all("aria-labelledby"):
                print(item)
            if '"' in query:
                query = query.replace('"', "'")
            f = open(f"cache/{query}_web.py", "w")
            f.write(f"cache = {allresults}")
            f.close()
        em = discord.Embed(title="Web Search Results", description=f"{self.bot.user.name} found **{len(allresults)}** results.")
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

    @commands.command()
    async def analyzeimage(self, ctx, censor=None, link=None):
        """Checks an image for NSFW content"""
        if link is None:
            link = ctx.message.attachments[0].url
        await ctx.message.delete()
        em = discord.Embed(title="Your image is being analyzed. Please wait...", color=discord.Color.red())
        em.set_author(icon_url="https://rc.reoccur.tech/assets/icon.gif", name="Image Analyzer")
        message1 = await ctx.send(embed=em)
        if censor is not None:
            nsfw, detection, censoredimage = await getunsafe(link, censor=True)  
        else:
            nsfw, detection, censoredimage = await getunsafe(link)  
        if nsfw is True:
            em = discord.Embed(color=discord.Color.red())
            em.set_author(icon_url="https://rc.reoccur.tech/assets/alert.png", name="Image Analyzer")
        else:
            em = discord.Embed(color=discord.Color.green())
            em.set_author(icon_url="https://rc.reoccur.tech/assets/checkmark.png", name="Image Analyzer")
        em.add_field(name="NSFW Verdict", value=str(nsfw))
        em.add_field(name="NSFW Detection", value=f"{str(detection)}%")
        em.set_footer(icon_url=ctx.author.avatar_url, text=f"{ctx.author.name}#{ctx.author.discriminator}")
        if censoredimage is not False:
            try:
                if bool(censoredimage):
                    file = discord.File(censoredimage, filename="censoredimage.jpg")
                    em.set_image(url="attachment://censoredimage.jpg")
                    await message1.delete()
                    await ctx.send(file=file, embed=em)
            except UnboundLocalError:
                pass
        else:
            await message1.delete()
            await ctx.send(embed=em)
    
    @commands.command()
    async def neko(self, ctx, choice = None, user: discord.User = None):
        """Use the command to see information on how to use it"""
        if choice == "slap":
            url = "http://api.nekos.fun:8080/api/slap"
            jsondata = await getdata(url)
            data = json.loads(jsondata)
            if os.path.isdir("data") is False:
                os.mkdir("data")
            if os.path.isdir("data/roleplay") is False:
                os.mkdir("data/roleplay")
            if os.path.isfile(f"data/roleplay/{user.id}_slap.py"):
                data2 = importlib.import_module(f"{str(user.id)}_slap")
                file = open(f"data/roleplay/{user.id}_slap.py", "r")
                readfile = file.read()
                file.close()
                slapnum2 = int(data2.slapnum) + 1
                readfile2 = readfile.replace(str(data2.slapnum), str(slapnum2))
                file = open(f"data/roleplay/{user.id}_slap.py", "w")
                file.write(readfile2)
                file.close()
                importlib.reload(data2)
            else:
                file = open(f"data/roleplay/{user.id}_slap.py", "w")
                file.write("slapnum = 1")
                file.close()
                data2 = importlib.import_module(f"{str(user.id)}_slap")
            em = discord.Embed(title=f"**{ctx.author.name}** slaps **{user.name}**!")
            em.set_image(url=data["image"])
            if data2.slapnum == 1:
                slapnum = "first"
            elif data2.slapnum == 2:
                slapnum = f"{data2.slapnum}nd"
            elif data2.slapnum == 3:
                slapnum = f"{data2.slapnum}rd"
            else:
                slapnum = f"{data2.slapnum}th"
            em.set_footer(text=f"This is their {slapnum} slap!")
            await ctx.send(embed=em)
        elif choice == "baka":
            url = "http://api.nekos.fun:8080/api/baka"
            jsondata = await getdata(url)
            data = json.loads(jsondata)
            em = discord.Embed(title="Baka!")
            em.set_image(url=data["image"])
            await ctx.send(embed=em)
        elif choice == "kiss":
            url = "http://api.nekos.fun:8080/api/kiss"
            jsondata = await getdata(url)
            data = json.loads(jsondata)
            if os.path.isdir("data") is False:
                os.mkdir("data")
            if os.path.isdir("data/roleplay") is False:
                os.mkdir("data/roleplay")
            if os.path.isfile(f"data/roleplay/{user.id}_kiss.py"):
                sys.path.insert(0, "data/roleplay")
                data2 = importlib.import_module(f"{str(user.id)}_kiss")
                file = open(f"data/roleplay/{user.id}_kiss.py", "r")
                readfile = file.read()
                file.close()
                kissnum2 = int(data2.kissnum)+1
                readfile = readfile.replace(str(data2.kissnum), str(kissnum2))
                file = open(f"data/roleplay/{user.id}_kiss.py", "w")
                file.write(readfile)
                file.close()
                importlib.reload(data2)
            else:
                sys.path.insert(0, "data/roleplay")
                file = open(f"data/roleplay/{user.id}_kiss.py", "w")
                file.write("kissnum = 1")
                file.close()
                data2 = importlib.import_module(f"{str(user.id)}_kiss")
            em = discord.Embed(title=f"**{ctx.author.name}** kisses **{user.name}**! Aww!")
            em.set_image(url=data["image"])
            if data2.kissnum == "1":
                kissnum = "first"
            elif data2.kissnum == "2":
                kissnum = f"{data2.kissnum}nd"
            elif data2.kissnum == "3":
                kissnum = f"{data2.kissnum}rd"
            else:
                kissnum = f"{data2.kissnum}th"
            em.set_footer(text=f"This is their {kissnum} kiss!")
            await ctx.send(embed=em)  
        elif choice == "cry":
            url = "http://api.nekos.fun:8080/api/cry"
            jsondata = await getdata(url)
            data = json.loads(jsondata)
            em = discord.Embed(title=f"**{ctx.author.name}** is crying!")
            em.set_image(url=data["image"])
            await ctx.send(embed=em)
        elif choice == "pat":
            url = "http://api.nekos.fun:8080/api/pat"
            jsondata = await getdata(url)
            data = json.loads(jsondata)
            if os.path.isdir("data") is False:
                os.mkdir("data")
            if os.path.isdir("data/roleplay") is False:
                os.mkdir("data/roleplay")
            if os.path.isfile(f"data/roleplay/{user.id}_pat.py"):
                sys.path.insert(0, "data/roleplay")
                data2 = importlib.import_module(f"{str(user.id)}_pat")
                file = open(f"data/roleplay/{user.id}_pat.py", "r")
                readfile = file.read()
                file.close()
                patnum2 = int(data2.patnum)+1
                readfile = readfile.replace(str(data2.patnum), str(patnum2))
                file = open(f"data/roleplay/{user.id}_pat.py", "w")
                file.write(readfile)
                file.close()
                importlib.reload(data2)
            else:
                sys.path.insert(0, "data/roleplay")
                file = open(f"data/roleplay/{user.id}_pat.py", "w")
                file.write("patnum = 1")
                file.close()
                data2 = importlib.import_module(f"{str(user.id)}_pat")
            em = discord.Embed(title=f"**{ctx.author.name}** pats **{user.name}**!")
            em.set_image(url=data["image"])
            if data2.patnum == 1:
                patnum = f"{data2.patnum}st"
            elif data2.patnum == 2:
                patnum = f"{data2.patnum}nd"
            elif data2.patnum == 3:
                patnum = f"{data2.patnum}rd"
            else:
                patnum = f"{data2.patnum}th"
            em.set_footer(text=f"This is their {patnum} pat!")
            await ctx.send(embed=em)  
        else:
            em = discord.Embed(title="Help", color=discord.Color.blue())
            em.add_field(name=f"`{config.prefix}neko cry`", value="Cri..")
            em.add_field(name=f"`{config.prefix}neko kiss (user id or mention)`", value="Give your special someone a kiss~")
            em.add_field(name=f"`{config.prefix}neko pat (userid or mention)`", value="If someone's good, give them a nice pat!")
            em.add_field(name=f"`{config.prefix}neko baka`", value="BAKA!")              
            await ctx.send(embed=em)

    @commands.command()
    @commands.cooldown(1,15,commands.BucketType.user)  
    async def shortenurl(self, ctx, url=None, endtext=None):
        """Use the command to see information on how to use it"""
        if endtext is not None:
            url = f"https://api.1pt.co/addURL?long={url}&short={endtext}"
        else:
            url = f"https://api.1pt.co/addURL?long={url}"
        jsondata = await getdata(url)
        data = json.loads(jsondata)
        em = discord.Embed(title="URL Shortened!", color=discord.Color.green())
        em.set_author(name="1pt.co", icon_url="https://raw.githubusercontent.com/paramt/1pt/master/resources/favicon/android-chrome-512x512.png")
        em.add_field(name="Shortened URL", value=f"https://1pt.co/{data['short']}")
        await ctx.reply(embed=em, mention_author=False)

    @commands.command()
    @commands.cooldown(1,15,commands.BucketType.user)  
    async def quote(self, ctx):
        """Fetches a random quote"""
        url = "https://api.fisenko.net/quotes"
        jsondata = await getdata(url)
        data = json.loads(jsondata)
        em = discord.Embed(title="Here's a quote for you:", description=f'"{data["text"]}" - {data["author"]}', color=discord.Color.green())
        await ctx.reply(embed=em, mention_author=False)
    
    @commands.command()
    @commands.cooldown(1,15,commands.BucketType.user)  
    async def compressimg(self, ctx, imgurl):
        """Use the command to see information on how to use it"""
        url = f"https://api.resmush.it/ws.php?img={imgurl}"
        jsondata = await getdata(url)
        data = json.loads(jsondata)
        em = discord.Embed(title="Here's your compressed image!", color=discord.Color.green())
        em.set_author(name="ReSmush.it Image Compression")
        try:
            em.add_field(name="Source Size", value=f"`{str(data['src_size'])}` bytes")
            em.add_field(name="New Size", value=f"`{str(data['dest_size'])}` bytes")
        except AttributeError:
            pass
        em.set_image(url=str(data["dest"]))
        await ctx.reply(embed=em, mention_author=False)

    @commands.command()
    @commands.cooldown(1,15,commands.BucketType.user)  
    async def unsplash(self, ctx, resolution=None):
        """Gets a random unsplash image"""
        em = discord.Embed(color=discord.Color.green())
        em.set_author(name="Lorem Picsum")
        randomnum = random.randint(1, 999999999999999)
        if resolution is not None:
            resolution = str(resolution)
            res1 = resolution.split("x")[0]
            res2 = resolution.split("x")[1]
            res2 = res2.replace("x", "")
            url = f"https://picsum.photos/{res1}/{res2}.jpg?random={str(randomnum)}"
        else:
            url = f"https://picsum.photos/1080/720.jpg?random={str(randomnum)}"
        filepath = await downloadimage(url)
        file = discord.File(filepath, filename="lorempicsum.jpg")
        em.set_image(url="attachment://lorempicsum.jpg")
        await ctx.reply(file=file, embed=em, mention_author=False)
        os.remove(filepath)

    @commands.command()
    @commands.cooldown(1,15,commands.BucketType.user)  
    async def doesnotexist(self, ctx, choice=None):
        """Gets a random unsplash image"""
        if choice == "person":
            em = discord.Embed(color=discord.Color.green())
            em.set_author(name="ThisPersonDoesNotExist")
            url = "https://thispersondoesnotexist.com/image"
            filepath = await downloadimage(url)
            file = discord.File(filepath, filename="persondoesntexist.jpg")
            em.set_image(url="attachment://persondoesntexist.jpg")
            em.set_footer(text="No, seriously, it doesn't exist.")
            await ctx.reply(file=file, embed=em, mention_author=False)
            os.remove(filepath)
        elif choice == "cat":
            em = discord.Embed(color=discord.Color.green())
            em.set_author(name="ThisCatDoesNotExist")
            url = "https://thiscatdoesnotexist.com/"
            filepath = await downloadimage(url)
            file = discord.File(filepath, filename="persondoesntexist.jpg")
            em.set_image(url="attachment://persondoesntexist.jpg")
            em.set_footer(text="No, seriously, they don't exist.")
            await ctx.reply(file=file, embed=em, mention_author=False)
            os.remove(filepath)
        else:
            em = discord.Embed(title="Help", color=discord.Color.blue())
            em.set_author(name="This(Thing)DoesNotExist")
            em.add_field(name=f"`{config.prefix}doesnotexist person`", value="Generates a person that doesn't exist")
            em.add_field(name=f"`{config.prefix}doesnotexist cat`", value="Generates a cat that doesn't exist")
            await ctx.reply(embed=em, mention_author=False)

    @commands.command()
    @commands.cooldown(1,15,commands.BucketType.user)  
    async def lengthenurl(self, ctx, url):
        """Á̴̧̡̢̜̝͕͓̅͜A̷̻̻̞̲̮̥̘̹͒̅͑̆͝Á̶̡̳͉̼̘̥̥̠̞͖͉̱̖̭̍A̶̖͕̦͍͕̝͂̋̎̎̈́͛̃̒̃A̵̢͔̼̯͖͇̪͖̹̗̗̠͌̀̍͋̊̕ͅẢ̶̛̦̖̮̜̪̭̖̜̱̲̩̬͐̂͆̔̎͗̆̄A̷̧̡̟̣̳̠̞͙̯̤̺̬͉̭͔̭͉͒͆̐̕A̷̜̙̜̦̮̣̯̱̫͍͇̰̙̋͆́̏͑̄̑̈́̂̏̐̅͆͘̚ͅÀ̶̧̢̛̲̮̠͈̞̜̻̈́̈́͆̃̊̈̎̄̿̍͝A̶̧̬̥̹͇͉̞͈̗͍̝͋̉̓̂Ą̶̜̳̖̈Ą̴̛̭͔̬̩̹̬̙̦͈̹̳͔̜͖̬̋̉̀̇̀̅̀̓́̃͊̀͛̍̕A̶̧̛̯̖͙͔̯̪̦̿͆̉̌̓̒̄̿̀A̷̡̙͇̰̥͎͌̑̈́̎͆̽̈́̈́̋A̷̦͚̤͓͈͈̬̳̩͖͓̺͔̙̪̦̐̈̓̈́̏̈͛͜A̸̢͚͓̩̦̮͔͇͎̻̺̠͕͔̖̹͊͛A̷̧̛̟͍̼̜̱̙̲͉͔͇͐̅̈́̌̓͐͐̋̆͐̒͛̚͘͝ͅĀ̶̙̥̤̜̹̰͐̈́̊̈́͜ͅA̵̮̜̗̟͎͗̐͠A̸͙̖̮̟͉͚̬̩̬̖̭̠̔͝A̶̜̽̒̀̈́̍̊͋̈́̋̊̓̒̀͝͝͝͝A̷͕̫̹̳̠̖̜̮̯̻͇͖͚̿͗͘Ȁ̷̲̣̘̭͌̎̄͒̃͆̌̾̽̇̓͊͝Ȃ̴̛̛͉͓̒̑͋̔̇̀̎̽̊̅̅̀̕̕A̷̧̡̺͉̺͇͚͓̺̞̫̖͍̞̥̰̍̈̀̌͐͗̍́̈́̒̈́̈́͠ͅÂ̶̧̯͇̜̙̭̟͍̮̺̭͑A̶̛̞̘̽̉̑̉̾͋̏̏̅̑̽͋͗̍A̷̰͋̑̆̿͋͊̓̐͝A̴̞̬̬͓̗̠̫͉̜̪͎̝̎̀̿̌͐̀̍͛̄͜ͅĄ̶̢̼̦̠͍͈̈̂͋̀̍͝Ã̴͙͈̯͈̮̤͐̃͒̈́̑̇Ą̸̺͓͕̘̥̖̱͎̑̾̊ͅȀ̷̧̨̬̺͚̫̠̮͕̞̺̗͖͈̥͔͉̾Ậ̵͇͎̝͚̥̞̦̺͋͊Ä̸̧̧̘͍͎͉̝͎͕͐̏̎͂͐̊̉̍̉̕Ä̸̢̢̨̨̲̟̯̣̮͉̘̰͍̝̙́̌̅̆̍̄̈́̓̌͜ͅA̴̹̥̩͔͍̝̩͍̼̪͋͜Ā̵̜͗̓̎̒̄̓̔̇͐͛͐̈́̍͌ͅA̴̡̢̛̙͎̗̖̫̙̼̻̜̬͈̒̀͌̋̋͌̈́͌̑̄̍̅͝͠A̷̩̣̬̹̪͘͠ͅȂ̸̡̛̫̱̩͎̮̻̗̾͋̇͌͒̒̈́̌̊̾̓͑ͅĄ̵̨̫̣͍͐͂͌̒̓͐͌͘Ą̵̛͚̘̩̙̜̑̇̄̈́̂̋͋̈́̇̔͑̚͘͘͜͝Ä̵̢̢̹̙͚͕̖͍̻̖͎̰͕́̇̕͜Ä̵̡̖̲̱͇̊̐̋̔̎͆̐̌͒̈́̊̾̚͝Ą̵̲͎̹͉͓͚͈̝̝̦̠̦̤̅̓́̓͗̔̏͑̊͘A̷̺̺̝̬̮͈̹̩͕̖̙̲̦̙̗̽́́̃̊̎̄͆̇͂̀͗͗̚͘͝͝Ă̶̧̰̼͙̑̽A̴̢̨̜͕͙͚̤̫̙̫̰̠͚͚̫̔͗̕Ä̴͇̼̩̜̫͖́̿̏́͆̾̾͛́͂͐̽͘̚͘̕͝A̶̳͎͚̣̼͒̊̂̃̐̓̚̕ͅA̵͑͛̚͠"""
        url = f"https://api.aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa.com/a?url={url}"
        data = await getdata(url)
        em = discord.Embed(title="U̵͈͐̈Ŗ̶̈́̏͆͐Ĺ̴́̔̍͜ ̴͝ͅL̷̯̜̈̈̊̈́͜e̶͔̗͇͐̈́͐̃n̴̻̫̓g̴̫̼͉̿̚͠͝t̸͔͚͚̆̊̉h̸̛͇͆͑e̷̢͈̙͌̋ͅṇ̸̢̝̈́̒̚e̸̫̻͑͂d̴͕̲̽͆!̷̞̯̺̃̂", color=discord.Color.green())
        em.set_author(name="aaa.aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa.com")
        em.add_field(name="L̶̳̠͇̄̕ȅ̸̪͎̯̍̎n̶͕̦̺͚͕̊̆g̵̢̨̝̓̎̐t̷̛͙̪̗̼̏͆̾̌͜͠h̷̡͖͍́͘ẻ̴̩̮̘͍̟̈́̽̎̓̑n̷̜̥̰͉̊̚ͅȩ̵̛̠ͅd̷̞̹͙͊̿̂̒ ̸͈͔͈͎̫̙̈́U̵͚̹̜̼̾̿͂́R̶̨̨̧͎͔̘͂̔̉L̸̬̯̬̫͎̝̊̄̕", value=f"`{str(data)}`")
        await ctx.reply(embed=em, mention_author=False)

def setup(bot):
    bot.add_cog(Fun(bot))

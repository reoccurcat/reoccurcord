# Copyright (C) 2021 reoccurcat
# This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
# You should have received a copy of the GNU General Public License along with this program.  If not, see <http://www.gnu.org/licenses/>.


###### SORTED IMPORTS FOR CLEANER LOOK ######

import bot
import psutil
import config
import random
import aiohttp
import discord  # removed "from discord import embeds", doesn't do anything
import requests
import time
import asyncio
import concurrent.futures 
import os
import importlib
import sys
import shutil
import json
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
    async def add(self, ctx, *integers): # creates a list of input (I haven't typecasted to (int) due to multitude of reasons)
        """Adds multiple numbers together."""
        if len(integers) <= 1:
            return await ctx.send("Provide at least two or more numbers!")
        
        new_list = [] # initializing new list
        for number in integers: # iterating over the original list of numbers
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

    
    @commands.command(description='For when you wanna settle the score some other way')
    async def choose(self, ctx, *choices: str):
        """Chooses between multiple choices.""" # removed unnecessary lines of code
        if "@everyone" in choices or "@here" in choices:
            em = discord.Embed(title = "Nice try, sadly that won't work here.", color = discord.Color.red())
            return await ctx.reply(embed=em, mention_author=False)
        em = discord.Embed(title = random.choice(choices), color = discord.Color.blue())
        await ctx.reply(embed=em, mention_author=False) 
    
    @commands.command(description='#emotes')
    async def emote(self, ctx, emote : discord.Emoji = None):
        """emote command"""
        if emote is None:
            em = discord.Embed(title="No emote given", description = f"Please use `{config.prefix[0]}emote <emote>`.", color = discord.Color.red())
            await ctx.reply(embed=em, mention_author=False)
        try:
            em = discord.Embed(timestamp=emote.created_at, color = discord.Color.blue())
            em.set_author(name=emote.name, icon_url=emote.url)
            em.set_thumbnail(url=emote.url)
            em.set_footer(text="Created on")
            em.add_field(name="ID", value=emote.id)
            em.add_field(name="Usage", value=f"`{emote}`")
            em.add_field(name="URL", value=f"[click here]({emote.url})") # masked links instead of actually sending the full link
            await ctx.reply(embed=em, mention_author=False)
        except IndexError:
            em = discord.Embed(title="Error", description="There was an error fetching the emote. The most likely cause is that it's from a server the bot isn't in.", color = discord.Color.red())

    @commands.command()
    async def f(self, ctx, *, message2):
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

    @commands.command()
    async def image(self, ctx, *, query):
        query = query.replace(" ", "+")
        if not os.path.exists('cache'):
            os.makedirs('cache')
        if os.path.isfile(f'cache/{query}.py'):
            sys.path.insert(0, './cache')
            #print("Using cache file:\n")
            importedquery = importlib.import_module(f"{str(query)}")
            images = importedquery.cache
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
                    except Exception as e:
                        #print(e)
                        pass                        
        printimage = random.choice(images)
        await ctx.send(str(printimage))


    @commands.command()
    async def listcache(self, ctx):
        try:
            em = discord.Embed(title="Image Cache Files", description=f"`{', '.join(os.listdir('./cache/'))}`", color=discord.Color.blue())
            await ctx.reply(embed=em, mention_author=False)
        except OSError:
            em = discord.Embed(title="Error", description="No cache folder could be found.", color=discord.Color.red())
            await ctx.reply(embed=em, mention_author=False)


    @commands.command()
    async def clearcache(self, ctx, clear = None):
        try:
            clear = clear.replace(" ", "+")
        except AttributeError:
            pass
        if clear is None:
            shutil.rmtree("./cache")
            em = discord.Embed(title="Image Cache Directory Cleared", description="The `./cache` directory has been cleared. Images will take a few seconds longer to fetch as they recache.", color=discord.Color.green())
            await ctx.reply(embed=em, mention_author=False)
        else:
            if os.path.isfile(f'cache/{clear}.py'):
                os.remove(f"./cache/{clear}.py")
                em = discord.Embed(title="Image Cache Directory Cleared", description=f"The `./cache/{clear}.py` file has been deleted. Images will take a few seconds longer to fetch as they recache.", color=discord.Color.green())
                await ctx.reply(embed=em, mention_author=False)
            else:
                em = discord.Embed(title="No cache file found.", description=f"There was no cache file found at `./cogs/{clear}.py`.", color=discord.Color.red())
                await ctx.reply(embed=em, mention_author=False)
                
    @commands.command(aliases=['rd'])
    @commands.cooldown(2,5,commands.BucketType.user)
    async def reddit(self, ctx, *, name):
        posts = []
        subreddit = f"{name}"
        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://www.reddit.com/r/{subreddit}/.json") as r:
                response = await r.json()
                try:
                 for i in response['data']['children']:
                    posts.append(i['data'])
                except KeyError:
                    return await ctx.send("The subreddit you provided doesn't exist!")
                try:
                 post = random.choice([p for p in posts if not p['stickied'] or p['is_self']])
                except IndexError:
                    return await ctx.send("The subreddit you provided doesn't exist!")
                if post['over_18'] is True and ctx.channel.nsfw is False:
                    return await ctx.send("Failed to get a post from that subreddit, try again in an NSFW channel.")
                title = str(post['title'])
        embed=discord.Embed(title=f'{title}', colour=0xaf85ff, url=f"https://reddit.com/{post['permalink']}")
        embed.set_footer(text=f"{post['upvote_ratio'] * 100:,}% Upvotes | Posted to r/{post['subreddit']}")
        embed.set_image(url=post['url'])
        await ctx.reply(embed=em, mention_author=False)
        
    @reddit.error
    async def on_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            seconds = round(error.retry_after, 2)
            return await ctx.send(f"You are being rated-limited, please try again in {seconds} seconds!")
    
    @commands.command()
    async def websitepeek(self, ctx, *, url: str):
        async with ctx.typing(), aiohttp.ClientSession() as session:
            screener = "http://magmachain.herokuapp.com/api/v1"
            async with session.post(screener, headers=dict(website=url)) as r:
                website = (await r.json())["snapshot"]
                em = discord.Embed(color=discord.Color.blue())
                em.set_image(url=website)
                await ctx.reply(embed=em, mention_author=False)

    @commands.command()
    async def websearch(self, ctx, *, query):
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
        em = discord.Embed(title="Web Search Results", description=f"FreeDiscord found **{len(allresults)}** results.")
        try:
            em.add_field(name="URLs Returned", value="\n".join(allresults))
        except Exception:
            em.add_field(name="Error", value="Too many urls fetched (dev is working on a fix)")
        await ctx.reply(embed=em, mention_author=False)

    @commands.command()
    async def animeinfo(self, ctx, query):
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
            await ctx.send(embed=em)

    @commands.command()
    async def catpic(self, ctx):
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

    @commands.command()
    async def findanime(self, ctx, link=None):
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
            await ctx.send(embed=em)

def setup(bot):
    bot.add_cog(Fun(bot))

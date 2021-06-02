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
from bs4 import BeautifulSoup
from discord.ext import commands
import concurrent.futures, os, importlib, sys, shutil

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
        await ctx.send(embed = em)

    
    @commands.command(description='For when you wanna settle the score some other way')
    async def choose(self, ctx, *choices: str):
        """Chooses between multiple choices.""" # removed unnecessary lines of code
        if "@everyone" in choices or "@here" in choices:
            em = discord.Embed(title = "Nice try, sadly that won't work here.", color = discord.Color.red())
            return await ctx.send(embed = em)
        em = discord.Embed(title = random.choice(choices), color = discord.Color.blue())
        await ctx.send(embed = em) 
    
    @commands.command(description='#emotes')
    async def emote(self, ctx, emote : discord.Emoji = None):
        """emote command"""
        if emote == None:
            em = discord.Embed(title="No emote given", description = f"Please use `{config.prefix}emote <emote>`.", color = discord.Color.red())
            await ctx.send(embed=em)
            return
        else:
            try:
                em = discord.Embed(timestamp=emote.created_at, color = discord.Color.blue())
                em.set_author(name=emote.name, icon_url=emote.url)
                em.set_thumbnail(url=emote.url)
                em.set_footer(text="Created on")
                em.add_field(name="ID", value=emote.id)
                em.add_field(name="Usage", value=f"`{emote}`")
                em.add_field(name="URL", value=f"[click here]({emote.url})") # masked links instead of actually sending the full link
                await ctx.send(embed=em)
                return
            except Exception:
                em = discord.Embed(title="That emote probably is not in the server that the bot is in.")
                await ctx.send(embed=em)
                return
        '''
        else:
            try:
                emote = discord.utils(self.bot.get_all_emojis())
                emote = discord.utils.get(self.bot.Emoji, name=emote)
            except Exception as e:
                await ctx.send(str(e))
                return
        '''

    @commands.command()
    async def f(self, ctx, *, message2):
        em = discord.Embed(title = f"F in the chat to: **{message2}**", color=discord.Color.blue())
        msg = await ctx.send(embed = em)
        await msg.add_reaction('🇫')
        def check(reaction, user):
            return msg == reaction.message
        usersreacted = []
        usersreacted.append(self.bot.user.name)
        while True:
            try:
                reaction, user = await self.bot.wait_for('reaction_add', check=check, timeout=30)
            except asyncio.TimeoutError:
                new_msg = await ctx.fetch_message(msg.id)
                number = len([x for x in await new_msg.reactions[0].users().flatten() if not x.bot])
                return await ctx.send(f"A total of {number} people paid their respects to **{message2}**.")
            else:
                if str(reaction.emoji) == "🇫":
                    if user.name in usersreacted:
                        continue
                    await ctx.send(f"**{user.name}** has paid their respects.")
                    usersreacted.append(user.name)

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
            await ctx.send(embed=em)
        except OSError:
            em = discord.Embed(title="Error", description="No cache folder could be found.", color=discord.Color.red())
            await ctx.send(embed=em)


    @commands.command()
    async def clearcache(self, ctx, clear = None):
        try:
            clear = clear.replace(" ", "+")
        except:
            pass
        if clear == None:
            shutil.rmtree("./cache")
            em = discord.Embed(title="Image Cache Directory Cleared", description="The `./cache` directory has been cleared. Images will take a few seconds longer to fetch as they recache.", color=discord.Color.green())
            await ctx.send(embed=em)
        else:
            if os.path.isfile(f'cache/{clear}.py'):
                os.remove(f"./cache/{clear}.py")
                em = discord.Embed(title="Image Cache Directory Cleared", description=f"The `./cache/{clear}.py` file has been deleted. Images will take a few seconds longer to fetch as they recache.", color=discord.Color.green())
                await ctx.send(embed=em)
            else:
                em = discord.Embed(title="No cache file found.", description=f"There was no cache file found at `./cogs/{clear}.py`.", color=discord.Color.red())
                await ctx.send(embed=em)
                
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
                if post['over_18'] == True and ctx.channel.nsfw is False:
                    return await ctx.send("Failed to get a post from that subreddit, try again in an NSFW channel.")
                title = str(post['title'])
        embed=discord.Embed(title=f'{title}', colour=0xaf85ff, url=f"https://reddit.com/{post['permalink']}")
        embed.set_footer(text=f"{post['upvote_ratio'] * 100:,}% Upvotes | Posted to r/{post['subreddit']}")
        embed.set_image(url=post['url'])
        await ctx.send(embed=embed)
        
    @reddit.error
    async def on_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            seconds = round(error.retry_after, 2)
            return await ctx.send("You are being rated-limited, please try again in {seconds} seconds!")
    

def setup(bot):
    bot.add_cog(Fun(bot))

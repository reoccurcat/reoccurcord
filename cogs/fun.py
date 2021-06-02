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
from bs4 import BeautifulSoup
from discord.ext import commands

##############################################

"""
requests and urllib are blocking. Do not use these libraries within your asynchronous code. 
(http://discordpy.readthedocs.io/en/latest/faq.html#what-does-blocking-mean)

discord.py uses aiohttp, so it should already be installed.
"""

def getdata(url):  # switch from requests module to aiohttp (see above for reason)
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            r = await response.text()  
    return r

class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def add(self, ctx, *integers = None): # creates a list of input (I haven't typecasted to (int) due to multitude of reasons)
        """Adds multiple numbers together."""
        if not integers:
            return await ctx.send("Provide at least two or more numbers!")
        if len(integers) == 1:
            return await ctx.send("Provide at least two or more numbers!")
        
        new_list = [] # initializing new list
        for number in integers: # iterating over the original list of numbers
        try:
           new_number = float(number) # conver the output to integer
           new_list.append([new_number, str(number)]) # append the converted string along with the string as a list
        except (TypeError, ValueError):
           pass # if a string is passed, pass it
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

    @commands.command()
    async def image(self, ctx, *, query):
        newquery = query.replace(" ", "+")
        #await ctx.send(newquery)
        images = []
        htmldata = getdata(f"https://searx.prvcy.eu/search?q={str(newquery)}&categories=images")
        #print(f"https://www.bing.com/images/search?q={str(newquery)}")
        soup = BeautifulSoup(htmldata, 'html.parser') 
        for item in soup.find_all('img'):
            if "data:image" not in str(item):
                if "/sa/" not in str(item):
                    if "/rp/" not in str(item):
                        try:
                            replace1 = item['src'].replace("%3A", ":")
                            replace2 = replace1.replace("%2F", "/")
                            replace3 = replace2.replace("%3F", "/")
                            replace4 = replace3.replace("%3D", "/")
                            replace5 = replace4.replace("%26", "?")
                            if "gstatic" in replace5:
                                replace6 = replace5.replace("images/", "images?")
                                replace7 = replace6.replace("q/", "q=")
                                lefttext = replace7.split("?usqp/")[0]
                                replace8 = lefttext.replace("?usqp/", "")
                                righttext = replace8.split("/image_proxy?url=")[1]
                                print(righttext)
                                images.append(righttext)
                            else:
                                righttext = replace5.split("/image_proxy?url=")[1]
                                print(righttext)
                                images.append(righttext)
                        except:
                            pass
        #for url in images:
        #    if "&c=" in url:
        #        right_text = url.split("&c=")[1]
        #        newtext = f"&c={right_text}"
        #        print(f"Right text is {newtext}")
        #        sep = '?w'
        #        stripped = url.split(sep, 1)[0]
        #        stripped += newtext
        #        newimages = []
                #newimages.append(stripped)
        #        print(stripped)
        #        newimages.append(stripped) 
                #if stripped != f"https://tse1.mm.bing.net/th":
                #    if stripped != f"https://tse2.mm.bing.net/th":
                #        if stripped != f"https://tse3.mm.bing.net/th":
                #            if stripped != f"https://tse4.mm.bing.net/th":
                #                print(stripped)
                #                newimages.append(stripped)                           
        printimage = random.choice(images)
        await ctx.send(str(printimage))


        
def setup(bot):
    bot.add_cog(Fun(bot))

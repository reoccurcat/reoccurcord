# Copyright (C) 2021 reoccurcat
# This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
# You should have received a copy of the GNU General Public License along with this program.  If not, see <http://www.gnu.org/licenses/>.

import discord
from discord import embeds
from discord.ext import commands
import psutil
import config
import bot
import random
import requests
from bs4 import BeautifulSoup 

def getdata(url): 
    r = requests.get(url) 
    return r.text

class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def add(self, ctx, left: int, right: int):
        """Adds two numbers together."""
        em = discord.Embed(title = left + right, color = discord.Color.blue())
        await ctx.send(embed = em)

    
    @commands.command(description='For when you wanna settle the score some other way')
    async def choose(self, ctx, *choices: str):
        """Chooses between multiple choices."""
        if "@everyone" in choices:
            em = discord.Embed(title = "Nice try, sadly that won't work here.", color = discord.Color.red())
            await ctx.send(embed = em)
        else:
            if "@here" in choices:
                em = discord.Embed(title = "Nice try, sadly that won't work here.", color = discord.Color.red())
                await ctx.send(embed = em)
            else:
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
                em.add_field(name="URL", value=f"<{emote.url}>")
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

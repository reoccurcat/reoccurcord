# Copyright (C) 2021 reoccurcat
# This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
# You should have received a copy of the GNU General Public License along with this program.  If not, see <http://www.gnu.org/licenses/>.

import os
import config
import discord
import aiohttp
import datetime
import requests
import globalconfig
from discord.ext import commands

intents = discord.Intents.default()
intents.members = True

description = ""

bot = commands.Bot(command_prefix=config.prefix, description=description, intents=intents)
bot.remove_command('help')

@bot.event
async def on_ready():
    # What gets printed in the terminal when the bot is succesfully logged in
    print('\n')
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    # Changes bot status to the default status when the bot starts up
    await bot.change_presence(activity=discord.Game(name='v' + globalconfig.version + " | " + config.prefix + "help"))
    try:
        async with aiohttp.ClientSession() as session:
            webhook = discord.Webhook.from_url(config.infowebhook, adapter=discord.AsyncWebhookAdapter(session))
            e = discord.Embed(title="Bot Back Online!", description="This FreeDiscord instance is back online.", color=discord.Color.green())
            await webhook.send(embed=e)
    except AttributeError:
        user = bot.get_user(int(config.ownerID))
        await user.send("The bot is back online.")

os.environ["JISHAKU_NO_DM_TRACEBACK"] = "True"
os.environ["JISHAKU_NO_UNDERSCORE"] = "True"
os.environ["JISHAKU_HIDE"] = "True"
os.environ["JISHAKU_RETAIN"] = "True"
bot.load_extension("jishaku")
#loading cog files (instead of loading one by one, using a for loop to load cogs)
for filename in os.listdir('./cogs'):
     if filename.endswith(".py"):
            bot.load_extension(f'cogs.{filename[:-3]}')

@bot.event
async def on_message(msg):
    if str(msg.author.id) in config.blacklist:
        for command in globalconfig.commands:
            newcontent = msg.content.split()[0]
            if newcontent.__contains__(config.prefix + str(command)):
                em = discord.Embed(title = "User Blacklisted", description = f"You are blacklisted from using the bot. Please contact <@!{config.ownerID}> for more information.")
                await msg.channel.send(embed = em, delete_after=5.0)
                return
    #try:
    #    for word in config.bad_words:
    #        if word in msg.content.lower():
    #            try:
    #                async with aiohttp.ClientSession() as session:
    #                    user = msg.author
    #                    webhook = discord.Webhook.from_url(config.adminwebhook, adapter=discord.AsyncWebhookAdapter(session))
    #                    e = discord.Embed(title="User Used Blacklisted Word!", color=discord.Color.red())
    #                    e.set_author(name=str(user), icon_url=user.avatar_url)
    #                    e.add_field(name="Word Blocked", value=f"||{msg.content}||")
    #                    #e.add_field(name="Message Blocked Time", value=str(datetime.now()))
    #                    await webhook.send(embed=e)
    #            except:
    #                pass
    #            await msg.delete()
    #            await msg.channel.send("Please don't use that word", delete_after=5.0)
    #        else:
    #            await bot.process_commands(msg)
    else:
        await bot.process_commands(msg)

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        em = discord.Embed(title = "Error", description = "You do not have permission to do that.", color = discord.Color.red())
        em.add_field(name = "Detailed Error", value = "`" + str(error) + "`")
        await ctx.send(embed = em)
    elif isinstance(error, commands.MissingRequiredArgument):
        em = discord.Embed(title = "Error", description = "Your command is missing an argument.", color = discord.Color.red())
        em.add_field(name = "Detailed Error", value = "`" + str(error) + "`")
        await ctx.send(embed = em)
    elif isinstance(error, commands.CommandNotFound):
        em = discord.Embed(title = "Error", description = "Command not found", color = discord.Color.red())
        em.add_field(name = "Detailed Error", value = "`" + str(error) + "`")
        await ctx.send(embed = em)
    else:
        em = discord.Embed(title = "An internal error occurred.", color = discord.Color.red())
        em.add_field(name = "Detailed Error", value = "`" + str(error) + "`")
        await ctx.send(embed = em)

bot.run(config.bot_token)

# Copyright (C) 2021-present reoccurcat
# This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
# You should have received a copy of the GNU General Public License along with this program.  If not, see <http://www.gnu.org/licenses/>.

import os
from sys import prefix
import config
import discord
import aiohttp
import globalconfig
import time
import asyncio
import random
from discord.ext import commands

intents = discord.Intents.default()
intents.members = True

description = ""

bot = commands.Bot(command_prefix=config.prefix, description=description, intents=intents)

statusloop = False

bot.commandsran = []
bot.errors = []

#bot.remove_command('help')

class MyNewHelp(commands.MinimalHelpCommand):
    def get_command_signature(self, command):
        return '%s%s %s' % (self.clean_prefix, command.qualified_name, command.signature)
    async def send_pages(self):
        destination = self.get_destination()
        for page in self.paginator.pages:
            emby = discord.Embed(description=page, color=discord.Color.blue())
            await destination.send(embed=emby)
    async def send_bot_help(self, mapping):
        embed = discord.Embed(title="Help", color=discord.Color.blue())
        cognames = []
        commandlist = []
        num = 0
        for cog, commands in mapping.items():
            filtered = await self.filter_commands(commands, sort=True)
            command_signatures = [self.get_command_signature(c) for c in filtered]  
            if command_signatures:
                num += 1   
                cog_name = getattr(cog, "qualified_name", "No Category")
                if cog_name != "No Category":
                    cognames.append(f'**Page {num}:**\t{cog_name}')
                    commandlist.append("\n".join(command_signatures))
                    embed.add_field(name=cog_name, value="\n".join(command_signatures))
        channel = self.get_destination()
        em = discord.Embed(title="Command List", description=f"This is the command list of {bot.user.name}'s commands. Click the numbers to go to different pages, or click the house to come back here.\n"+'\n'.join(cognames), color=discord.Color.blue())
        em.set_author(name=f"{bot.user.name}", icon_url="https://rc.reoccur.tech/assets/icon.gif")
        msg = await channel.send(embed=em)
        oldpage = 0
        emojilist = [ "🏠", "1️⃣", "2️⃣", "3️⃣", "⏹️"]
        for emoji in emojilist:
            await msg.add_reaction(f"{emoji}")
        def check(reaction, user):
            return user == self.context.author and str(reaction.emoji) in emojilist
        while True:
            try:
                reaction, user = await bot.wait_for("reaction_add", timeout=60, check=check)
                # waiting for a reaction to be added - times out after x seconds, 60 in this
                if str(reaction.emoji) == "1️⃣":
                    page = 1
                    em = discord.Embed(title=f"Command List Page {page}\n{cognames[page-1]}", description=f"{commandlist[page-1]}", color=discord.Color.blue())
                    em.set_author(name=f"{bot.user.name}", icon_url="https://rc.reoccur.tech/assets/icon.gif")
                    await msg.edit(embed=em)
                    await msg.remove_reaction(reaction, user)
                    oldpage = 1
                elif str(reaction.emoji) == "2️⃣":
                    page = 2
                    em = discord.Embed(title=f"Command List Page {page}\n{cognames[page-1]}", description=f"{commandlist[page-1]}", color=discord.Color.blue())
                    em.set_author(name=f"{bot.user.name}", icon_url="https://rc.reoccur.tech/assets/icon.gif")
                    await msg.edit(embed=em)
                    await msg.remove_reaction(reaction, user) 
                    oldpage = 2
                elif str(reaction.emoji) == "3️⃣":
                    page = 3
                    em = discord.Embed(title=f"Command List Page {page}\n{cognames[page-1]}", description=f"{commandlist[page-1]}", color=discord.Color.blue())
                    em.set_author(name=f"{bot.user.name}", icon_url="https://rc.reoccur.tech/assets/icon.gif")
                    await msg.edit(embed=em)
                    await msg.remove_reaction(reaction, user)
                    oldpage = 3
                elif str(reaction.emoji) == "4️⃣":
                    page = 4
                    em = discord.Embed(title=f"Command List Page {page}\n{cognames[page-1]}", description=f"{commandlist[page-1]}", color=discord.Color.blue())
                    em.set_author(name=f"{bot.user.name}", icon_url="https://rc.reoccur.tech/assets/icon.gif")
                    await msg.edit(embed=em)
                    await msg.remove_reaction(reaction, user)
                    oldpage = 4
                elif str(reaction.emoji) == "🏠":
                    page = 5
                    em = discord.Embed(title="Command List", description=f"This is the command list of {bot.user.name}'s commands. Click the numbers to go to different pages, or click the house to come back here.\n"+'\n'.join(cognames), color=discord.Color.blue())
                    em.set_author(name=f"{bot.user.name}", icon_url="https://rc.reoccur.tech/assets/icon.gif")
                    await msg.edit(embed=em)
                    await msg.remove_reaction(reaction, user)
                    oldpage = 5
                elif str(reaction.emoji) == "⏹️":
                    for emoji in emojilist:
                        await msg.clear_reaction(emoji)
                    break
            except asyncio.TimeoutError:
                for emoji in emojilist:
                    await msg.clear_reaction(emoji)
                break
                # ending the loop if user doesn't react after x seconds
            except IndexError:
                await msg.remove_reaction(reaction, user)
                em = discord.Embed(title="Error", description="Oops! You may not have permission to see this command group!", color=discord.Color.red())
                em.set_author(name=f"{bot.user.name}", icon_url="https://rc.reoccur.tech/assets/icon.gif")
                await msg.edit(embed=em)
                await asyncio.sleep(5) 
                if oldpage == 0:
                    em = discord.Embed(title="Command List", description=f"This is the command list of {self.self.bot.user.name}'s commands. Click the numbers to go to different pages, or click the house to come back here.\n"+'\n'.join(cognames), color=discord.Color.blue())
                    em.set_author(name=f"{bot.user.name}", icon_url="https://rc.reoccur.tech/assets/icon.gif")
                    await msg.edit(embed=em)
                else:
                    try:
                        page = oldpage
                        em = discord.Embed(title=f"Command List Page {page}\n{cognames[page-1]}", description=f"{commandlist[page-1]}", color=discord.Color.blue())
                        em.set_author(name=f"{bot.user.name}", icon_url="https://rc.reoccur.tech/assets/icon.gif")
                        await msg.edit(embed=em)
                    except Exception as e:
                        raise e
                    await msg.edit(embed=em)
                    continue
    async def send_error_message(self, error):
        embed = discord.Embed(title="Error", value=error, color=discord.Color.red())
        channel = self.get_destination()
        await channel.send(embed=embed)
    async def send_command_help(self, command):
        embed = discord.Embed(title=self.get_command_signature(command), color=discord.Color.blue())
        embed.add_field(name="Help", value=command.help)
        alias = command.aliases
        if alias:
            embed.add_field(name="Aliases", value=", ".join(alias), inline=False)
        channel = self.get_destination()
        await channel.send(embed=embed)

bot.help_command = MyNewHelp()

async def resetcommands():
    while True:
        mostusedcommands = []
        time.sleep(21600)

async def status_task():
    while True:
        statusloop = True
        await bot.change_presence(status=discord.Status.idle, activity=discord.Game(f"in {len(bot.guilds)} servers with {len(bot.users)} users"))
        await asyncio.sleep(20)
        await bot.change_presence(status=discord.Status.idle, activity=discord.Activity(type=discord.ActivityType.watching, name=f"for {config.prefix}help | v{str(globalconfig.version)}"))
        await asyncio.sleep(20)

@bot.event
async def on_ready():
    # What gets printed in the terminal when the bot is succesfully logged in
    print('\n')
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    # Changes bot status to the default status when the bot starts up
    #await bot.change_presence(activity=discord.Game(name='v' + globalconfig.version + " | " + config.prefix + "help"))
    try:
        async with aiohttp.ClientSession() as session:
            webhook = discord.Webhook.from_url(config.infowebhook, adapter=discord.AsyncWebhookAdapter(session))
            e = discord.Embed(title="Bot Back Online!", description="This reoccurcord instance is back online.", color=discord.Color.green())
            await webhook.send(embed=e)
    except AttributeError:
        user = bot.get_user(int(config.ownerID))
        await user.send("The bot is back online.")
    if statusloop is False:
        bot.loop.create_task(status_task())
    #await resetcommands()

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
    try:
        newcontent = msg.content.split()[0]
    except:
        newcontent = msg.content
    for command in bot.commands:
        if newcontent.__contains__(config.prefix + str(command)):
            if str(msg.author.id) in config.blacklist:
                em = discord.Embed(title = "User Blacklisted", description = f"You are blacklisted from using the bot. Please contact <@!{config.ownerID}> for more information.")
                await msg.channel.send(embed = em, delete_after=5.0)
                return
            elif newcontent != f"{config.prefix}mostusedcmds":  
                bot.commandsran.append(str(command))
                break
    await bot.process_commands(msg)

@bot.event
async def on_guild_join(guild):
    em = discord.Embed(title="Thanks for adding me!", description=f"Hi! I'm {bot.user.name}! I'm a multipurpose bot that can do a lot for you.", color=discord.Color.blue())
    em.add_field(name="What can you do?", value=f"I have many commands, which you can take a look at using `{config.prefix}help`!")
    em.add_field(name="What are your most popular commands?", value="My most popular commands are the `image`, `findanime`, and `analyzeimage` commands. Try them out!")
    em.set_footer(text="This bot is mainly developed by reoccurcat#0001 and various contributers on GitHub.")
    em.set_author(name=bot.user.name, icon_url="https://rc.reoccur.tech/assets/assets/icon.gif")
    for channel in guild.text_channels:
        if channel.name.__contains__("general"):
            if channel.permissions_for(guild.me).send_messages:
                await channel.send(embed=em)
                return
        elif channel.name.__contains__("bot"):
            if channel.permissions_for(guild.me).send_messages:
                await channel.send(embed=em)
                return
        elif channel.name.__contains__("system"):
            if channel.permissions_for(guild.me).send_messages:
                await channel.send(embed=em)
                return
    channel = guild.system_channel
    if channel.permissions_for(guild.me).send_messages:
        await channel.send(embed=em)

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        em = discord.Embed(title = "Error", description = "You do not have permission to do that.", color = discord.Color.red())
        em.add_field(name = "Detailed Error", value = "`" + str(error) + "`")
        await ctx.reply(embed=em, mention_author=False, delete_after=5)
    elif isinstance(error, commands.MissingRequiredArgument):
        em = discord.Embed(title = "Error", description = "Your command is missing an argument.", color = discord.Color.red())
        em.add_field(name = "Detailed Error", value = "`" + str(error) + "`")
        await ctx.reply(embed=em, mention_author=False, delete_after=5)
    elif isinstance(error, commands.CommandNotFound):
        return
    elif isinstance(error, commands.CommandOnCooldown):
        em = discord.Embed(title = "Cooldown Error", color = discord.Color.red())
        em.add_field(name = "Error Details", value = f'This command is on cooldown, you can use it in {round(error.retry_after, 2)} seconds.')
        await ctx.reply(embed=em, mention_author=False, delete_after=5)
    else:
        em = discord.Embed(title = "An internal error occurred.", color = discord.Color.red())
        em.add_field(name = "Detailed Error", value = "`" + str(error) + "`")
        await ctx.reply(embed=em, mention_author=False, delete_after=5)
    randnum = random.randint(1, 9999)
    dictionary = {}
    dictionary["command"] = str(ctx.message.content.split()[0])
    dictionary["error"] = str(error)
    bot.errors.append(dictionary)
    del dictionary

bot.run(config.bot_token)

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
        for cog, commands in mapping.items():
           filtered = await self.filter_commands(commands, sort=True)
           command_signatures = [self.get_command_signature(c) for c in filtered]
           if command_signatures:
                cog_name = getattr(cog, "qualified_name", "No Category")
                embed.add_field(name=cog_name, value="\n".join(command_signatures))
        channel = self.get_destination()
        await channel.send(embed=embed)
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
    elif isinstance(error, commands.CommandOnCooldown):
        em = discord.Embed(title = "Cooldown Error", color = discord.Color.red())
        em.add_field(name = "Error Details", value = f'This command is on cooldown, you can use it in {round(error.retry_after, 2)} seconds.')
        await ctx.send(embed=em)
    else:
        em = discord.Embed(title = "An internal error occurred.", color = discord.Color.red())
        em.add_field(name = "Detailed Error", value = "`" + str(error) + "`")
        await ctx.send(embed = em)

bot.run(config.bot_token)

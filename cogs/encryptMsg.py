# Copyright (C) 2021 reoccurcat
# This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
# You should have received a copy of the GNU General Public License along with this program.  If not, see <http://www.gnu.org/licenses/>.

import discord
import time
import config
from discord.ext import commands
from cryptography.fernet import Fernet

rounds_error = "No rounds given, syntax: command + rounds + message."

class Caesarcrypt(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(description="Twisted your message with caesarcrypt. @bot rounds(numbers) message")
    async def twisted_msg(self, ctx):
        """Encrypt a message."""
        message = ctx.message.content.split(" ")
        message = message.remove(message[0])
        message = bytes("".join(message), "utf-8")

        key = Fernet.generate_key()
        encrypted = Fernet(key).encrypt(message)

        await ctx.send(embed=discord.Embed(title="Encrypted message", description=f"{encrypted}\n\nYour decryption key is {str(key)}"))


    @commands.command(description="Untwisted the message with caesarcrypt. @bot rounds(numbers) message")
    async def untwisted_msg(self, ctx):
        """Decrypt a message."""
        message = ctx.message.content.split(" ")
        message = message.remove(message[0])
        key = bytes(message[0], "utf-8")
        message = message.remove(message[0])

        decrypted = Fernet(key).decrypt(bytes("".join(message), "utf-8"))

        await ctx.send(embed=discord.Embed(title="Decrypted message", description={decrypted}))

def setup(bot):
    bot.add_cog(Caesarcrypt(bot))


# if config.bot_lockdown_status == "no_lockdown":
#    ...
# elif config.bot_lockdown_status == "lockdown_activated":
#    em = discord.Embed(title = "This bot is locked down", description = "<@!" + config.ownerID + "> has locked down this bot globally.")
#    await ctx.send(embed = em)

# Copyright (C) 2021-present reoccurcat
# This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
# You should have received a copy of the GNU General Public License along with this program.  If not, see <http://www.gnu.org/licenses/>.

import discord
from discord.ext import commands
#import time
#import config

rounds_error = "No rounds given, syntax: command + rounds + message."

class Caesarcrypt(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(description="Twisted your message with caesarcrypt. @bot rounds(numbers) message")
    async def twisted_msg(self, ctx, rounds = None, *, message: str):
        """Encrypt a message."""
        await ctx.message.delete()
        if rounds is None:
            em = discord.Embed(title = "Wrong syntax.", description = rounds_error, color = discord.Color.red())
            return await ctx.send(embed = em)
        try:
            rounds = int(rounds)
        except Exception:
            em = discord.Embed(title = "Wrong syntax.", description = rounds_error, color = discord.Color.red())
            return await ctx.send(embed = em)
        encrypt = ""
        message = str(message)
        for char in message:
            if not char.isalpha():
                encrypt = encrypt + char
            elif char.isupper():
                # for uppercase Z
                encrypt = encrypt + chr((ord(char) + rounds - 65) % 26 + 65)
            else:
                # for lowercase z
                encrypt = encrypt + chr((ord(char) + rounds - 97) % 26 + 97)
        em = discord.Embed(title = 'Your encrypted message is: {}'.format(encrypt), color = discord.Color.blue())
        await ctx.send(embed = em)



    @commands.command(description="Untwisted the message with caesarcrypt. @bot rounds(numbers) message")
    async def untwisted_msg(self, ctx, rounds: int, *, message: str):
        """Decrypt a message."""
        await ctx.message.delete()
        if rounds is None:
            em = discord.Embed(title = "Wrong syntax.", description = rounds_error, color = discord.Color.red())
            return await ctx.send(embed = em)
        try:
            rounds = int(rounds)
        except Exception:
            em = discord.Embed(title = "Wrong syntax.", description = rounds_error, color = discord.Color.red())
            return await ctx.send(embed = em)
        decrypt = ""
        message = str(message)
        for char in message:
            if not char.isalpha():
                decrypt = decrypt + char
            elif char.isupper():
                # for uppercase Z
                decrypt = decrypt + chr((ord(char) - rounds - 65) % 26 + 65)
            else:
                # for lowercase z
                decrypt = decrypt + chr((ord(char) - rounds - 97) % 26 + 97)

        em = discord.Embed(title = 'Your decrypted message is: {}'.format(decrypt), color = discord.Color.blue())
        await ctx.send(embed = em)



def setup(bot):
    bot.add_cog(Caesarcrypt(bot))


# if config.bot_lockdown_status == "no_lockdown":
#    ...
# elif config.bot_lockdown_status == "lockdown_activated":
#    em = discord.Embed(title = "This bot is locked down", description = "<@!" + config.ownerID + "> has locked down this bot globally.")
#    await ctx.send(embed = em)

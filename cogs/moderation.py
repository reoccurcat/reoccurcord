# Copyright (C) 2021-present reoccurcat
# This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
# You should have received a copy of the GNU General Public License along with this program.  If not, see <http://www.gnu.org/licenses/>.

import discord
import os
import random
import asyncio
import string
from discord.ext import commands

##immune_roles variable
#def check_immune(roles):
#    roles = ''.join(filter(str.isalpha, str(roles)))
#    roles = roles.replace('Roleidname', ' ')
#    roles = roles.split()
#    if any(role in roles for role in config.immune_roles) == True:
#        return True
#    else:
#        return False

def timeconvertion(time):# Time convertion
    convertion = {"s": 1, "m": 60, "h": 3600, "d": 86400}
    letters_inside = ''.join(filter(str.isalpha, time))
    lettercount = len(letters_inside)
    to_convert = ''.join(filter(str.isdigit, time))
    if time[-1].isalpha() is True and time[0].isdigit() and lettercount == 1 and letters_inside in convertion and time.isalnum() is True:
        timeconverted = int(to_convert) * convertion[time[-1]]
        return int(timeconverted)
    return False

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    @commands.cooldown(1,10,commands.BucketType.user)
    async def purge(self, ctx, amount=10):
        """Purges messages, the default amount is 10"""
        if amount >= 100:
            await ctx.reply("This bot can only purge up to 99 messages.")
        await ctx.channel.purge(limit=amount+1)

    @commands.command()
    @commands.cooldown(1,10,commands.BucketType.user)
    async def dmpurge(self, ctx, amount=10):
        """Purges messages in dms, the default amount is 10"""
        if amount >= 100:
            await ctx.reply("This bot can only purge up to 99 messages.")
        if isinstance(ctx.channel, discord.channel.DMChannel):
            await ctx.channel.purge(limit=amount+1)
        else:
            await ctx.send("You cannot purge messages in a server using this command.")


    @commands.command()
    @commands.has_permissions(kick_members=True)
    @commands.cooldown(1,10,commands.BucketType.user)
    async def kick(self, ctx, user: discord.Member, *reason):
        """Kicks a member"""
        args = " ".join(reason[:])
        if not reason:
            await user.kick()
            em = discord.Embed(title = f"**{user}** has been kicked, reason: **none**.", color = discord.Color.blue())
            await ctx.reply(embed = em, mention_author=False)
        else:
            await user.kick()
            em = discord.Embed(title = f"**{user}** has been kicked, reason: **{args}**.", color = discord.Color.blue())
            await ctx.reply(embed = em, mention_author=False)


    @commands.command()
    @commands.has_permissions(ban_members=True)
    @commands.cooldown(1,10,commands.BucketType.user)
    async def ban(self, ctx, user: discord.Member, *reason):
        """Bans a member"""
        args = " ".join(reason[:])
        if not reason:
            await user.ban()
            em = discord.Embed(title = f"**{user}** has been banned, reason: **none**.", color = discord.Color.blue())
            await ctx.reply(embed = em, mention_author=False)
        else:
            await user.ban()
            em = discord.Embed(title = f"**{user}** has been banned, reason: **{args}**.", color = discord.Color.blue())
            await ctx.reply(embed = em, mention_author=False)


    @commands.command() # Takes 1s 1m 1h 1d
    @commands.has_permissions(manage_messages=True)
    @commands.cooldown(1,10,commands.BucketType.user)
    async def mute(self, ctx, user: discord.Member, mutetime):
        #BTW need to import time&asyncio module to work.
        """Mutes a member"""
        if timeconvertion(mutetime) is not False:
            role = discord.utils.get(user.guild.roles, name="muted")
            await user.add_roles(role)
            em = discord.Embed(title = "User has been muted for " + "`{}`".format(str(mutetime)) + ".", color = discord.Color.blue())
            await ctx.reply(embed = em, mention_author=False)
            await asyncio.sleep(timeconvertion(mutetime))
            await user.remove_roles(role)
        elif timeconvertion(mutetime) is False:
            em = discord.Embed(title = "The time format doesn't seem right.")
            await ctx.reply(embed = em, mention_author=False)


    @commands.command()
    @commands.has_permissions(ban_members=True)
    @commands.cooldown(1,10,commands.BucketType.user)
    async def softban(self, ctx, user: discord.Member, *reason):
        """Softbans a member, which bans and unbans them, removing the messages they sent in the last 7 days"""
        args = " ".join(reason[:])
        await ctx.guild.ban(user)
        await ctx.guild.unban(user)
        if not reason:
            em = discord.Embed(title = f"**{user}** has been softbanned, reason: **none**.", color = discord.Color.blue())
            await ctx.reply(embed = em, mention_author=False)
        else:
            em = discord.Embed(title = f"**{user}** has been softbanned, reason: **{args}**.", color = discord.Color.blue())
            await ctx.reply(embed = em, mention_author=False)


    @commands.command()
    @commands.has_permissions(ban_members=True)
    @commands.cooldown(1,10,commands.BucketType.user)
    async def unban(self, ctx, userid: int):
        """Unbans a member"""
        userToUnban = await self.bot.fetch_user(id)
        await ctx.guild.unban(userToUnban)
        em = discord.Embed(title = "Successfully unbanned `" + userToUnban.name + "`.", color = discord.Color.green())
        await ctx.reply(embed = em, mention_author=False)


    @commands.command()
    @commands.has_permissions(manage_messages=True)
    @commands.cooldown(1,10,commands.BucketType.user)
    async def unmute(self, ctx, user: discord.Member):
        """Unmutes a member"""
        role = discord.utils.get(user.guild.roles, name="muted")
        await user.remove_roles(role)
        em = discord.Embed(title = "Successfully unmuted `" + user.name + "`", color = discord.Color.green())
        await ctx.reply(embed = em, mention_author=False)


    @commands.command()
    @commands.has_permissions(manage_messages=True)
    @commands.cooldown(1,10,commands.BucketType.user)
    async def warn(self, ctx, user : discord.Member, *reason):
        """Warns a member"""
        args = " ".join(reason[:])
        if not os.path.exists('warns'):
            os.makedirs('warns')
        try:
            if os.stat("warns/" + str(user.id) + "_" + str(ctx.message.guild.id) + ".py").st_size > 0:
                await ctx.reply("Successfully warned that member.", mention_author=False)
                writeReasonTemplate = str(args)
                warns = open("warns/" + str(user.id) + "_" + str(ctx.message.guild.id) + ".py", 'a')
                warns.write("\n")
                warns.write(writeReasonTemplate)
                warns.close()

            elif os.stat("warns/" + str(user.id) + "_" + str(ctx.message.guild.id) + ".py").st_size == 0:
                await ctx.reply("Successfully warned that member.", mention_author=False)
                writeReasonTemplate = f"str(args)"
                warns = open("warns/" + str(user.id) + "_" + str(ctx.message.guild.id) + ".py", 'a')
                warns.write(writeReasonTemplate)
                warns.close()
        except OSError:
            await ctx.reply("Successfully warned that member.", mention_author=False)
            writeReasonTemplate = str(args)
            warns = open("warns/" + str(user.id) + "_" + str(ctx.message.guild.id) + ".py", 'a')
            warns.write(writeReasonTemplate)
            warns.close()


    @commands.command()
    @commands.has_permissions(manage_messages=True)
    @commands.cooldown(1,10,commands.BucketType.user)
    async def warns(self, ctx, user : discord.Member):
        """Warns a member"""
        if not os.path.exists('warns'):
            os.makedirs('warns')
        try:
            if os.stat("warns/" + str(user.id) + "_" + str(ctx.message.guild.id) + ".py").st_size > 0:
                with open("warns/" + str(user.id) + "_" + str(ctx.message.guild.id) + ".py") as f:
                    lines = f.readlines()
                    lines_clean = "".join(lines[:])
                    if not lines_clean:
                        em = discord.Embed(title = "Warns for " + str(user), description = "This user has no warnings.", color = discord.Color.blue())
                    else:
                        em = discord.Embed(title = "Warns for " + str(user), description = lines_clean, color = discord.Color.blue())
                        await ctx.reply(embed = em, mention_author=False)
            elif os.stat("warns/" + str(user.id) + "_" + str(ctx.message.guild.id) + ".py").st_size == 0:
                em = discord.Embed(title = "Warns for " + str(user), description = "This user has no warnings.", color = discord.Color.blue())
                await ctx.reply(embed = em, mention_author=False)
        except OSError:
                em = discord.Embed(title = "Warns for " + str(user), description = "This user has no warnings.", color = discord.Color.blue())
                await ctx.reply(embed = em, mention_author=False)


    @commands.command()
    @commands.has_permissions(manage_messages=True)
    @commands.cooldown(1,10,commands.BucketType.user)
    async def delwarn(self, ctx, user : discord.Member, *, reason):
        """Deletes a warning"""
        if not os.path.exists('warns'):
            os.makedirs('warns')
        fn = "warns/" + str(user.id) + "_" + str(ctx.message.guild.id) + ".py"
        f = open(fn)
        output = []
        word=str(reason)
        for line in f:
            if not line.startswith(word):
                output.append(line)
        f.close()
        f = open(fn, 'w')
        f.writelines(output)
        f.close()
        await ctx.reply("Successfully removed that warning.", delete_after=10.0, mention_author=False)

    
    @commands.command(pass_context=True)
    @commands.has_permissions(manage_nicknames=True)
    @commands.cooldown(1,10,commands.BucketType.user)
    async def modnick(self, ctx, *, user: discord.Member):
        """Moderates a nickname for a member, which sets it to 'ModdedNick' and a series of random letters and numbers"""
        source = string.ascii_letters + string.digits
        result_str = ''.join((random.choice(source) for i in range(8)))
        newnickname = f"ModdedNick{result_str}"
        await user.edit(nick=newnickname)
        await ctx.message.delete()
        await ctx.reply(f'Nickname was moderated for {user.mention} ({user.name}#{user.discriminator}).', delete_after=5.0, mention_author=False)


    @commands.command(pass_context=True)
    @commands.has_permissions(manage_nicknames=True)
    @commands.cooldown(1,10,commands.BucketType.user)
    async def changenick(self, ctx, user: discord.Member, nick):
        """Changes a nickname for a member"""
        await user.edit(nick=nick)
        await ctx.message.delete()
        await ctx.reply(f'Nickname was changed for {user.mention} ({user.name}#{user.discriminator}).', delete_after=5.0, mention_author=False)

def setup(bot):
    bot.add_cog(Moderation(bot))

# Copyright (C) 2021 reoccurcat
# This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
# You should have received a copy of the GNU General Public License along with this program.  If not, see <http://www.gnu.org/licenses/>.

import discord
from discord.ext import commands
import config
import datetime
import time
start_time = time.time()
class Utils(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ping(self, ctx):
        '''
        Get the latency of the bot.
        '''
        em = discord.Embed(title = "Pong! `"f"{round(self.bot.latency*1000)} ms`.", color = discord.Color.blue())
        await ctx.send(embed = em)


    @commands.command()
    async def avatar(self, ctx, *, user: discord.Member = None):
        """Get a link to somebody's avatar."""
        if user is None:
            user = ctx.author # removed unnecessary else statement
        icon_webp = f'[GIF]({user.avatar_url})' if user.is_avatar_animated() else f'[WEBP]({user.avatar_url})'
        icon_png = user.avatar_url_as(format='png')
        icon_jpg = user.avatar_url_as(format='jpg')
        embed = discord.Embed(title=f"{user.name}'s Avatar", description=f'[PNG]({icon_png}) | [JPG]({icon_jpg}) | {icon_webp}', color= discord.Color.blue())
        embed.set_image(url=user.avatar_url)
        await ctx.send(embed=embed) #send it in an embed with different types of formats of the image

    @commands.command()
    async def userinfo(self, ctx, user: discord.Member = None):
        """Gives information about a user."""
        if isinstance(ctx.channel, discord.DMChannel):
            return
        if user is None:
            user = ctx.author
        if user.display_name == user.name:
            usernickname = "None"
        else:
            usernickname = user.display_name
            
        date_format = config.date_format
        embed = discord.Embed(color = discord.Color.blue())
        embed.set_author(name=str(user), icon_url=user.avatar_url)
        embed.set_thumbnail(url=user.avatar_url)
        embed.add_field(name="ID", value=user.id)
        embed.add_field(name="Nickname", value=usernickname)
        embed.add_field(name="Joined", value=user.joined_at.strftime(date_format), inline=False)
        members = sorted(ctx.guild.members, key=lambda m: m.joined_at)
        embed.add_field(name="Registered", value=user.created_at.strftime(date_format), inline=True)
        perm_string = ', '.join([str(p[0]).replace("_", " ").title() for p in user.guild_permissions if p[1]])
        embed.add_field(name="Guild permissions", value=perm_string, inline=False)
        return await ctx.send(embed=embed)
        


    @commands.command()
    async def joined(self, ctx, member: discord.Member = None):
        """Says when a member joined."""
        if not member:
            member = ctx.author
        em = discord.Embed(title = '{0.name} joined in {0.joined_at}'.format(member), color = discord.Color.blue())
        await ctx.send(embed = em)



    @commands.command()
    async def serverinfo(self, ctx):
        """Gives some information about the server."""
        role_count = len(ctx.guild.roles)
        name = str(ctx.guild.name)
        description = "Description: " + str(ctx.guild.description)
        owner = str(ctx.guild.owner)
        id = str(ctx.guild.id)
        region = str(ctx.guild.region)
        memberCount = str(ctx.guild.member_count)
        icon = str(ctx.guild.icon_url)
        embed = discord.Embed(
            description=description,
            color=discord.Color.blue()
            )
        embed.set_thumbnail(url=icon)
        embed.set_author(name=name, icon_url=icon)
        embed.add_field(name="Owner", value=owner, inline=True)
        embed.add_field(name="Server ID", value=id, inline=True)
        embed.add_field(name="Server Created", value=ctx.guild.created_at.__format__(config.date_format))
        embed.add_field(name="Region", value=region, inline=True)
        embed.add_field(name="Number of Members", value=memberCount, inline=True)
        embed.add_field(name="Number of Roles", value=str(role_count), inline=True)

        await ctx.send(embed=embed)


    @commands.command()
    async def quickpoll(self, ctx, *, poll): # umm why not just use (*, poll) instead of (*poll)
        await ctx.message.delete()
        em = discord.Embed(title = f'{args}')
        msg = await ctx.send(embed = em)
        await msg.add_reaction('👍')
        await msg.add_reaction('👎')


    @commands.command(pass_context=True)
    async def uptime(self, ctx):
        current_time = time.time()
        difference = int(round(current_time - start_time))
        text = str(datetime.timedelta(seconds=difference))
        embed = discord.Embed(name="Uptime", value=text)
        try:
            await ctx.send(embed=embed)
        except discord.HTTPException:
            await ctx.send("Current uptime: " + text)

def setup(bot):
    bot.add_cog(Utils(bot))

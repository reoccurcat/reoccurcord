# Copyright (C) 2021 reoccurcat
# This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
# You should have received a copy of the GNU General Public License along with this program.  If not, see <http://www.gnu.org/licenses/>.

import discord
from discord.ext import commands
import config
import globalconfig
import importlib
import subprocess
import os

class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def reloadcog(self, ctx, *args):
        """Reloads a cog"""
        if str(ctx.message.author.id) == config.ownerID:
            args = "cogs." + " ".join(args[:])
            self.bot.unload_extension(args)
            self.bot.load_extension(args)
            em = discord.Embed(title = "Cog Reloaded", description = "`" + args + "` has been reloaded.", color = discord.Color.green())
            await ctx.send(embed = em)
        else:
            em = discord.Embed(title = "This command is for the bot owner only.", color = discord.Color.red())
            await ctx.send(embed = em)

    @commands.command()
    async def unloadcog(self, ctx, *args):
        """Unloads a cog"""
        if str(ctx.message.author.id) == config.ownerID:
            args = "cogs." + " ".join(args[:])
            self.bot.unload_extension(args)
            em = discord.Embed(title = "Cog Unloaded", description = "`" + args + "` has been unloaded.", color = discord.Color.green())
            await ctx.send(embed = em)
        else:
            em = discord.Embed(title = "This command is for the bot owner only.", color = discord.Color.red())
            await ctx.send(embed = em)

    @commands.command()
    async def loadcog(self, ctx, *args):
        """Loads a cog"""
        if str(ctx.message.author.id) == config.ownerID:
            args = "cogs." + " ".join(args[:])
            self.bot.load_extension(args)
            em = discord.Embed(title = "Cog Loaded", description = "`" + args + "` has been loaded.", color = discord.Color.green())
            await ctx.send(embed = em)
        else:
            em = discord.Embed(title = "This command is for the bot owner only.", color = discord.Color.red())
            await ctx.send(embed = em)

    @commands.command()
    async def restartbot(self, ctx):
        """Restarts the bot"""
        if str(ctx.message.author.id) == config.ownerID:
            first_embed = discord.Embed(title = "Restarting bot...", color = discord.Color.blue())
            msg = await ctx.send(embed=first_embed)
            dir_path = os.getcwd()
            subprocess.Popen(['python3', dir_path + '/bot.py'])
            new_embed = discord.Embed(title = "Restarted bot!", color = discord.Color.green())
            await msg.edit(embed=new_embed)
            await ctx.bot.close()
        else:
            em = discord.Embed(title = "This command is for the bot owner only.", color = discord.Color.red())
            await ctx.send(embed = em)

    @commands.command()
    async def shutdownbot(self, ctx):
        """Shuts down the bot"""
        if str(ctx.message.author.id) == config.ownerID:
            first_embed = discord.Embed(title = "Shutting down bot...", color = discord.Color.blue())
            msg = await ctx.send(embed=first_embed)
            new_embed = discord.Embed(title = "Shut down bot!", description = "Check your console, as it may still be running a subprocess. If it is, press `ctrl + c` on your keyboard to end the process.", color = discord.Color.green())
            await msg.edit(embed=new_embed)
            await ctx.bot.close()
        else:
            em = discord.Embed(title = "This command is for the bot owner only.", color = discord.Color.red())
            await ctx.send(embed = em)
        

    @commands.command()
    async def servers(self, ctx):
        if str(ctx.message.author.id) == config.ownerID:
            servers = list(self.bot.guilds)
            embed = discord.Embed(title = f"Connected on {str(len(servers))} servers:", color = discord.Color.blue())
            embed.add_field(name = "Servers", value = '\n'.join(guild.name for guild in self.bot.guilds))
            embed.add_field(name = "Server IDs", value = '\n'.join(str(guild.id) for guild in self.bot.guilds))
            #embed.add_field(name = "Server Invites", value = '\n'.join(for guild in self.bot.guilds: server = self.bot.get_guild(int(guild.id)); for channel in server.channels: invite = await channel.create_invite() if channel.name == "general"))
            await ctx.send(embed = embed)
            #await ctx.send(f"Connected on {str(len(servers))} servers:")
            #await ctx.send('\n'.join(guild.name for guild in self.bot.guilds))
        else:
            em = discord.Embed(title = "This command is for the bot owner only.", color = discord.Color.red())
            await ctx.send(embed = em)

    @commands.command()
    async def getinvite(self, ctx, serverID, channelName = None):
        if str(ctx.message.author.id) == config.ownerID:
            if channelName != None:
                channelQuery = channelName
            elif channelName == None:
                channelQuery = "general"
            server = self.bot.get_guild(int(serverID))
            #await ctx.send(server)
            embed = discord.Embed(title = f"Generated invite for '{server.name}'", color = discord.Color.blue())
            #channel = discord.utils.get(server.channels, name='general')
            #await ctx.send(channel)
            for channel in server.channels:
                if channel.name.__contains__(channelQuery) == True:
                    #await ctx.send(channel.id)
                    embed.add_field(name = "Channel Name", value = channel.name)
                    embed.add_field(name = "Channel ID", value = channel.id)
                    invite = await channel.create_invite()
                    embed.add_field(name = "Channel Invite", value = invite)
                    await ctx.send(embed = embed)
                    break
                #invite = channel.create_invite()
                #await ctx.send(invite)
            #guildID = ctx
            #server = discord.utils.get(str(guildID))
            #channel = discord.utils.get(server.channels, name='General')
            #invite = channel.create_invite()
            #await ctx.send(invite)
        else:
            em = discord.Embed(title = "This command is for the bot owner only.", color = discord.Color.red())
            await ctx.send(embed = em)

    @commands.command()
    async def getchannels(self, ctx, serverID):
        if str(ctx.message.author.id) == config.ownerID:
            server = self.bot.get_guild(int(serverID))
            #await ctx.send(server)
            #channel = discord.utils.get(server.channels, name='general')
            #await ctx.send(channel)
            embed = discord.Embed(title = f"List of channels for the server '{server.name}'", color = discord.Color.blue())
            for channel in server.channels:
                #channelsList.append(channel.name)
                embed.add_field(name = channel.name, value = channel.type)
            #channelslist = list(server.channels)
            #embed.add_field(name = "Servers", value = '\n'.join(str(channelslist)))
            await ctx.send(embed = embed)
            #for channel in server.channels:
                #await ctx.send(channel)
                #invite = channel.create_invite()
                #await ctx.send(invite)
        else:
            em = discord.Embed(title = "This command is for the bot owner only.", color = discord.Color.red())
            await ctx.send(embed = em)

    @commands.command()
    async def leaveserver(self, ctx, serverID):
        if str(ctx.message.author.id) == config.ownerID:
            server = self.bot.get_guild(int(serverID))
            await server.leave()
            embed = discord.Embed(title = f"Left the server '{server.name}'.", color = discord.Color.green())
            await ctx.send(embed = embed)
        else:
            em = discord.Embed(title = "This command is for the bot owner only.", color = discord.Color.red())
            await ctx.send(embed = em)

    #@commands.command()
    #async def blacklist(self, ctx, option, userID):
        #if str(ctx.message.author.id) == config.ownerID:
        #    if bool(ctx.guild) == True:
        #        await ctx.message.delete()
        #    if str(userID).isdigit() == True:
        #        if str(option) == "remove":
        #            oldlist = config.blacklist
        #            oldlist.remove(str(userID))
        #            importlib.reload(config)
        #            em = discord.Embed(title = "Success", description = f"Successfully removed <@!{str(userID)}> from the blacklist.")
        #            await ctx.send(embed = em, delete_after=5.0)
        #        elif str(option) == "add":
        #            importlib.reload(config)
        #            with open('config.py', 'r') as file1:
        #                filedata = file1.read()
        #            oldlist = config.blacklist
        #            print(oldlist)
        #            oldlist.append(str(userID))
        #            with open('tempconfig.py', 'w') as file:
        #                file.write(str(oldlist))
        #            with open('tempconfig.py', 'r') as file2:
        #                filedata1 = file2.read()
        #            print(str(config.blacklist))
        #            print(str(filedata1))
        #            filedata2 = filedata.replace(str(config.blacklist), str(filedata1))
        #            with open('tempconfig2.py', 'w') as file3:
        #                file3.write(filedata2)
        #        elif str(option) == "list":
        #            em = discord.Embed(title = "Blacklisted Users")
        #            em.add_field(name = "User IDs", value = '\n'.join(list(config.blacklist)))
        #            #em.add_field(name = "User Mentions", value = "<@!" + *config.blacklist, sep = "\n") + ">")
        #            await ctx.send(embed = em, delete_after=10.0)
        #        else:
        #            em = discord.Embed(title = "Error", description = f"`{str(option)}` doesn't seem to be a valid option. The valid options are `add` and `remove`.")
        #            await ctx.send(embed = em, delete_after=5.0)
        #    else:
        #        em = discord.Embed(title = "Error", description = f"`{str(userID)}` doesn't look like a User ID.")
        #        await ctx.send(embed = em, delete_after=5.0)
        #else:
        #    em = discord.Embed(title = "This command is for the bot owner only.", delete_after=5.0)
        #    await ctx.send(embed = em)

def setup(bot):
    bot.add_cog(Admin(bot))

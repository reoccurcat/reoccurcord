# Copyright (C) 2021-present reoccurcat
# This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
# You should have received a copy of the GNU General Public License along with this program.  If not, see <http://www.gnu.org/licenses/>.

import discord
import config
import datetime
import time
import os
import sys
import asyncio
import psutil
import requests
import aiohttp
import json
import importlib
import subprocess
import globalconfig
import shutil
from discord.ext import commands
from shutil import copyfile
from git import Repo

sys.path.append(os.path.realpath('.'))
start_time = time.time()

apikey = config.virustotal_api
iconurl = "https://rc.reoccur.tech/assets/vt_logo.png"

async def getdata(url):  # switch from requests module to aiohttp (see above for reason)
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            r = await response.text()  
    return r

def vt_json_parsing(detections):
    try:
        detections = str(detections).split("last_analysis_stats")
        detections = str(detections[1]).split('"')
    except Exception:
        return -1
    for m in detections:
        if 'malicious' in str(m) and any(d.isdigit() for d in m):
            detections = m
            detections = "".join(filter(str.isdigit, m))
            break
    return detections

class Utils(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ping(self, ctx):
        '''
        Get the latency of the bot.
        '''
        em = discord.Embed(title = "Pong! `"f"{round(self.bot.latency*1000)} ms`.", color = discord.Color.blue())
        await ctx.reply(embed = em, mention_author=False)


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
        await ctx.reply(embed=embed, mention_author=False) #send it in an embed with different types of formats of the image

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
        return await ctx.reply(embed=embed, mention_author=False)
        


    @commands.command()
    async def joined(self, ctx, member: discord.Member = None):
        """Says when a member joined."""
        if not member:
            member = ctx.author
        em = discord.Embed(title = '{0.name} joined in {0.joined_at}'.format(member), color = discord.Color.blue())
        await ctx.reply(embed = em, mention_author=False)



    @commands.command()
    async def serverinfo(self, ctx):
        """Gives some information about the server."""
        role_count = len(ctx.guild.roles)
        name = str(ctx.guild.name)
        description = "Description: " + str(ctx.guild.description)
        owner = str(ctx.guild.owner)
        guildid = str(ctx.guild.id)
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
        embed.add_field(name="Server ID", value=guildid, inline=True)
        embed.add_field(name="Server Created", value=ctx.guild.created_at.__format__(config.date_format))
        embed.add_field(name="Region", value=region, inline=True)
        embed.add_field(name="Number of Members", value=memberCount, inline=True)
        embed.add_field(name="Number of Roles", value=str(role_count), inline=True)

        await ctx.reply(embed=embed, mention_author=False)


    @commands.command()
    @commands.cooldown(1,30,commands.BucketType.user)
    async def quickpoll(self, ctx, *, poll): # umm why not just use (*, poll) instead of (*poll)
        await ctx.message.delete()
        em = discord.Embed(title = f'{poll}')
        msg = await ctx.send(embed = em)
        await msg.add_reaction('👍')
        await msg.add_reaction('👎')


    @commands.command(pass_context=True)
    @commands.cooldown(1,10,commands.BucketType.user)
    async def uptime(self, ctx):
        """Gets the uptime of the bot"""
        current_time = time.time()
        difference = int(round(current_time - start_time))
        text = str(datetime.timedelta(seconds=difference))
        embed = discord.Embed(name="Uptime", value=text)
        try:
            await ctx.reply(embed=embed, mention_author=False)
        except discord.HTTPException:
            await ctx.reply("Current uptime: " + text, mention_author=False)

    @commands.command()
    @commands.cooldown(1,30,commands.BucketType.user)
    async def botstatus(self, ctx, *args):
        """Sets the status of the bot. Owner only. Use 'botstatus' to reset"""
        args = " ".join(args[:])
        if str(ctx.message.author.id) == config.ownerID:
            if args == '':
                await self.bot.change_presence(activity=discord.Game(name=''))

                em = discord.Embed(title = "Bot status successfully reset!", color = discord.Color.green())
                await ctx.reply(embed = em, mention_author=False)
            else:
                await self.bot.change_presence(activity=discord.Game(name=args))

                em = discord.Embed(title = "Bot status successfully changed to `" + args + "`!", color = discord.Color.green())
                await ctx.reply(embed = em, mention_author=False)
        else:
            em = discord.Embed(title = "This command is for the bot owner only.", color = discord.Color.red())
            await ctx.reply(embed = em, mention_author=False)

    @commands.command()
    @commands.cooldown(1,10,commands.BucketType.user)
    async def about(self, ctx):
        '''Shows information about the bot instance'''
        em = discord.Embed(title = "About this instance", color = discord.Color.blue())
        em.add_field(name = "Instance name", value=f"{self.bot.user.name}#{self.bot.user.discriminator} ({self.bot.user.id})")
        em.add_field(name = "Website", value = "[Reoccur Tech](https://rc.reoccur.tech)")
        em.add_field(name = "Project URL", value = "[Github Link](https://github.com/reoccurcat/reoccurcord/)")
        em.add_field(name = "Support server", value = "[Discord Server](https://discord.gg/BNhVjFyB3S)")
        em.add_field(name = "Bot invite link", value = "[Invite Link](https://rc.reoccur.tech/invite)")
        em.add_field(name = "Terms of Service", value = "[ToS](https://rc.reoccur.tech/tos)")
        em.add_field(name = "Privacy Policy", value = "[Privacy](https://rc.reoccur.tech/privacy)")
        serverNumber = len(self.bot.guilds) # self.bot.guilds is a list object itself
        em.add_field(name = "Bot Server Count", value = serverNumber)
        cpuUsage = psutil.cpu_percent()
        em.add_field(name="Host CPU Usage", value=f"{cpuUsage}%")
        memUsage = psutil.virtual_memory().percent
        em.add_field(name="Host Memory Usage", value=f"{memUsage}%")
        em.add_field(name = "Ping", value = "`"f"{round(self.bot.latency*1000)} ms`")
        em.add_field(name="Prefix", value=f"`{config.prefix}`")
        em.add_field(name="Bot Owner", value=f"<@!{config.ownerID}>")
        current_time = time.time()
        difference = int(round(current_time - start_time))
        text = str(datetime.timedelta(seconds=difference))
        em.add_field(name="Uptime", value=text)
        em.set_thumbnail(url="https://rc.reoccur.tech/assets/icon.gif")
        await ctx.reply(embed = em, mention_author=False)

    @commands.command()
    @commands.cooldown(1,30,commands.BucketType.user)
    async def scanhash(self, ctx, inputhash: str):
        """Scans a hash using VirusTotal"""
        await ctx.message.delete()
        header = {'x-apikey': '{}'.format(apikey)}
        vturl = "https://www.virustotal.com/api/v3/files/{}".format(inputhash)
        response = requests.get(vturl, headers = header).json()
        response = str(response).split(",")
        parsed = vt_json_parsing(response)
        if parsed == -1:
            em = discord.Embed(title = "Something went wrong, could be the hash not in the VirusTotal database.", color = discord.Color.red())
            await ctx.reply(embed = em, mention_author=False)
            return
        generated_link = "https://www.virustotal.com/gui/file/{}/detection".format(inputhash)
        if int(parsed) == 0 :
            em = discord.Embed(title = "Detections: {}".format(parsed), color = discord.Color.green())
        elif int(parsed) >= 1 :
            em = discord.Embed(title = "Detections: {}".format(parsed), color = discord.Color.red())
        em.set_author(name="VirusTotal", icon_url=iconurl)
        em.add_field(name="Link:", value=generated_link)
        await ctx.reply(embed = em, mention_author=False)
        return


    @commands.command()
    @commands.cooldown(1,30,commands.BucketType.user)
    async def scanurl(self, ctx, url: str):
        """Scans a URL using VirusTotal"""
        #Need to import base64 module to work
        await ctx.message.delete()
        header = {'x-apikey': '{}'.format(apikey)}
        data = {'url': url}
        vturl = "https://www.virustotal.com/api/v3/urls"
        response = requests.post(vturl, data = data, headers = header).json()
        response = str(response).split(",")
        keyword = "'id': '"
        for i in response:
            if keyword in str(i):
                response = i.replace(keyword, "").replace("}", "").replace("'", "").replace(" ", "").split("-")
                try:
                    result_id = str(response[1])
                except Exception:
                    em = discord.Embed(title = "Something went wrong. Could be that you did not add the http/https prefix at the beginning of the webpage.", color = discord.Color.red())
                    em.set_author(name="VirusTotal", icon_url=iconurl)
                    await ctx.reply(embed = em, mention_author=False)
                    return
                break
        try:
            vturl = "https://www.virustotal.com/api/v3/urls/{}".format(result_id)
        except Exception:
            em = discord.Embed(title = "Something went wrong.", color = discord.Color.red())
            em.set_author(name="VirusTotal", icon_url=iconurl)
            await ctx.reply(embed = em, mention_author=False)
            return
        em = discord.Embed(title = "Analyzing URL...", description = "Please wait for 15 seconds.", color = discord.Color.blue())
        em.set_author(name="VirusTotal", icon_url=iconurl)
        msg = await ctx.reply(embed = em, mention_author=False)
        await asyncio.sleep(15)
        response = requests.get(vturl, headers=header).json()
        response = str(response).split(",")
        parsed = vt_json_parsing(response)
        if parsed == -1:
            new_embed = discord.Embed(title = "Something went wrong. Could be that you did not add the http/https prefix at the beginning of the webpage.", color = discord.Color.red())
            #await ctx.reply(embed = em)
            await msg.edit(embed=new_embed)
        else:
            generated_link = "https://www.virustotal.com/gui/url/{}/detection".format(result_id)
            if int(parsed) >= 1:
                new_embed = discord.Embed(title = "Detections: {}".format(str(parsed)), color = discord.Color.red())
            else:
                new_embed = discord.Embed(title = "Detections: {}".format(str(parsed)), color = discord.Color.green())
            new_embed.set_author(name="VirusTotal", icon_url=iconurl)
            new_embed.add_field(name="Link:", value=generated_link)
            #await ctx.reply(embed = em)
            await msg.edit(embed=new_embed)

    @commands.command()
    async def onesecmail(self, ctx, action=None, arg1=None, arg2=None):
        """Generate and manage a temporary email address"""
        mailicon = "https://rc.reoccur.tech/assets/email.png"
        if action == "generate":
            url = "https://www.1secmail.com/api/v1/?action=genRandomMailbox"
            jsondata = await getdata(url)
            jsondata = json.loads(jsondata)
            for item in jsondata:
                jsondata2 = item
            em = discord.Embed(title="Email Creator", description=f"Your generated temporary email is `{jsondata2}`.", color=discord.Color.blue())
            em.set_footer(text=f"Try running '{config.prefix}onesecmail check (email)' to view your inbox!")
            em.set_author(name="Temp Mail Manager", icon_url=mailicon)
            await ctx.send(embed=em)
        elif action == "check":
            email = arg1.split("@")[0]
            domain = arg1.split("@")[1].replace("@", "")
            url = f"https://www.1secmail.com/api/v1/?action=getMessages&login={email}&domain={domain}"
            jsondata = await getdata(url)
            jsondata = json.loads(jsondata)
            if str(jsondata) == "[]":
                em = discord.Embed(title="Email Manager", description="You have no emails yet.", color=discord.Color.blue())
                em.set_author(name="Temp Mail Manager", icon_url=mailicon)
                await ctx.send(embed=em)
            else:
                #await ctx.send(str(jsondata))
                #await ctx.send(type(jsondata))
                emailnum = 1
                em = discord.Embed(title="Email Manager", color=discord.Color.blue())
                em.set_author(name="Temp Mail Manager", icon_url=mailicon)
                em.set_footer(text=f"Try running '{config.prefix}onesecmail read (email) (ID)' to read a message!")
                for email in list(jsondata):
                    #await ctx.send(email)
                    em.add_field(name=f"Email {str(emailnum)} Details", value=f"Sender: **"+email["from"]+"**\nSubject: **"+email["subject"]+"**\nDate: **"+email["date"]+"**\n ID: **"+str(email["id"])+"**")
                await ctx.send(embed=em)
        elif action == "read":
            email = arg1.split("@")[0]
            domain = arg1.split("@")[1].replace("@", "")
            print(arg2)
            url = f"https://www.1secmail.com/api/v1/?action=readMessage&login={email}&domain={domain}&id={str(arg2)}"
            jsondata = await getdata(url)
            print(jsondata)
            data = json.loads(jsondata)
            em = discord.Embed(title="Email Viewer", color=discord.Color.blue())
            em.set_author(name="Temp Mail Manager", icon_url=mailicon)
            em.add_field(name="Sender", value=data["from"])
            em.add_field(name="Subject", value=data["subject"])
            em.add_field(name="Body", value=data["textBody"], inline=False)
            em.add_field(name="Date", value=data["date"])
            em.add_field(name="ID", value=str(data["id"]))   
            await ctx.send(embed=em)     
        else:
            em = discord.Embed(title="Help", color=discord.Color.blue())
            em.set_author(name="Temp Mail Manager", icon_url=mailicon)
            em.add_field(name=f"`{config.prefix}onesecmail generate`", value="Generates a temporary email.")
            em.add_field(name=f"`{config.prefix}onesecmail check (email)`", value="Views your inbox.")
            em.add_field(name=f"`{config.prefix}onesecmail view (email) (id)`", value="Views a message.")          
            await ctx.send(embed=em)

    @commands.command()
    @commands.cooldown(1,10,commands.BucketType.user)
    async def admin(self, ctx, choice=None, arg1=None, arg2=None):
        """Bot owner only commands. Run without any arguments to see the help on it."""
        if str(ctx.message.author.id) == config.ownerID:
            if choice == "update":
                if sys.platform == "linux" or sys.platform == "linux2":
                        try:
                            os.mkdir('./tmp/freeupdate')
                        except FileNotFoundError:
                            os.rmdir('./tmp/freeupdate')
                            os.mkdir('./tmp/freeupdate')
                        HTTPS_REMOTE_URL = globalconfig.github_login_url
                        DEST_NAME = './tmp/freeupdate'
                        cloned_repo = Repo.clone_from(HTTPS_REMOTE_URL, DEST_NAME)
                        dir_path = os.getcwd()
                        shutil.rmtree(dir_path + "/cogs/")
                        path = dir_path
                        src = './tmp/freeupdate/cogs'
                        dest = dir_path + "/cogs"
                        destination = shutil.copytree(src, dest)
                        copyfile('./tmp/freeupdate/bot.py', dir_path + '/bot.py')
                        copyfile('./tmp/freeupdate/setup.py', dir_path + '/setup.py')
                        copyfile('./tmp/freeupdate/README.md', dir_path + '/README.md')
                        copyfile('./tmp/freeupdate/globalconfig.py', dir_path + '/globalconfig.py')
                        copyfile('./tmp/freeupdate/start.py', dir_path + '/start.py')
                        shutil.rmtree('./tmp/freeupdate')
                        print("Done! Restart the bot to apply the changes!")
                        em = discord.Embed(title = "Updated!", description = f"{self.bot.user.name} updated! No error reported. Check your console to confirm this.", color = discord.Color.green())
                        em.add_field(name = "Note", value = "The bot will now restart. If it doesn't, start it up manually. If it won't start, open an issue in reoccurcord's GitHub repository.")
                        await ctx.reply(embed=em, mention_author=False)
                        dir_path = os.getcwd()
                        subprocess.Popen(['python3', f'{dir_path}/bot.py'])
                        await ctx.bot.close()
                elif sys.platform == "win32":
                        em = discord.Embed(title = "`updatebot` is not yet available for Windows.", color = discord.Color.red())
                        await ctx.reply(embed=em, mention_author=False)
                elif sys.platform == "darwin":
                        em = discord.Embed(title = "`updatebot` is not yet available for macOS.", color = discord.Color.red())
                        await ctx.reply(embed=em, mention_author=False)
            elif choice == "reload":
                args = f"cogs.{arg1}"
                self.bot.unload_extension(args)
                self.bot.load_extension(args)
                em = discord.Embed(title = "Cog Reloaded", description = "`" + args + "` has been reloaded.", color = discord.Color.green())
                await ctx.reply(embed=em, mention_author=False)
            elif choice == "updatecheck":
                if sys.platform == "linux" or sys.platform == "linux2" or sys.platform == "darwin":
                    tmpdir = "./tmp"
                elif sys.platform == "win32":
                    tmpdir = "./Temp"
                with open('config.py') as f:
                    if not 'latest_version' in f.read():
                        with open('config.py', 'a') as writeFile :
                            writeFile.write("latest_version = 'unknown'")
                            writeFile.close()
                            importlib.reload(config)
                if not os.path.exists(tmpdir + '/updatecheck'):
                    os.makedirs(tmpdir + '/updatecheck')
                elif os.path.exists(tmpdir + '/updatecheck'):
                    if os.path.exists(tmpdir + '/updatecheck/.git/objects/pack'):
                        new_name = str("unlock")
                        os.rename(tmpdir + '/updatecheck/.git/objects/pack', new_name)
                        shutil.rmtree('unlock')
                    shutil.rmtree(tmpdir + '/updatecheck')
                #os.mkdir('/tmp/freeupdate')
                HTTPS_REMOTE_URL = globalconfig.github_login_url
                first_embed = discord.Embed(title = "Checking for updates...", description = f"{self.bot.user.name} is now checking for updates. Please be patient.", color = discord.Color.blue())
                # send a first message with an embed
                msg = await ctx.reply(embed=first_embed, mention_author=False)
                DEST_NAME = tmpdir + '/updatecheck'
                cloned_repo = Repo.clone_from(HTTPS_REMOTE_URL, DEST_NAME)
                dir_path = os.getcwd()
                copyfile(tmpdir + '/updatecheck/globalconfig.py', dir_path + '/updateconfig.py')
                try:
                    shutil.rmtree(tmpdir + '/updatecheck')
                except os.error:
                    embed = discord.Embed(title = "Error in removing `" + tmpdir + "/updatecheck` folder", description = 'The `' + tmpdir + '/updatecheck` folder was not able to be removed, probably due to a permissions issue.', color = discord.Color.red())
                    await ctx.reply(embed=embed, mention_author=False) 
                updateconfig = importlib.import_module("updateconfig")
                if updateconfig.version > globalconfig.version:
                    new_embed = discord.Embed(title = "Checking for updates...", description = "Checking for updates succeeded!", color = discord.Color.green())
                    new_embed.add_field(name = "Upgrade found!", value = "It is recommended to update to version " + updateconfig.version + " from version " + globalconfig.version + " for the latest bug fixes and feature improvements.")
                    new_embed.add_field(name = "How do I upgrade?", value = "Use `" + config.prefix + "help updatebot` for more details.")
                    await msg.edit(embed=new_embed)
                if updateconfig.version < globalconfig.version:
                    new_embed = discord.Embed(title = "Checking for updates...", description = "Checking for updates succeeded!", color = discord.Color.green())
                    new_embed.add_field(name = "Downgrade found!", value = "It is recommended to downgrade to version " + updateconfig.version + " from version " + globalconfig.version + " because something most likely broke in the latest release.")
                    new_embed.add_field(name = "How do I downgrade?", value = "Use `" + config.prefix + "help updatebot` for more details. (The update command also downgrades the bot.)")
                    await msg.edit(embed=new_embed)
                if updateconfig.version == globalconfig.version:
                    new_embed = discord.Embed(title = "Checking for updates...", description = "Checking for updates succeeded!", color = discord.Color.green())
                    new_embed.add_field(name = "No updates found!", value = "You are up to date! This bot is at version `" + globalconfig.version + "` and the latest bot files available are at version `" + updateconfig.version + "`.")
                    new_embed.add_field(name = "How do I upgrade?", value = "You don't need to take any action, as you are up to date already. However, you can use `" + config.prefix + "help updatebot` for more details about the upgrade/downgrade process.")
                    await msg.edit(embed=new_embed)
                with open('config.py', 'r') as file :
                    filedata = file.read()
                newdata = filedata.replace(config.latest_version, updateconfig.version)
                with open('config.py', 'w') as file:
                    file.write(newdata)
                file.close()
                importlib.reload(config)
                os.remove(dir_path + "/updateconfig.py")
            elif choice == "blacklist":
                if bool(ctx.guild) is True:
                    await ctx.message.delete()
                if str(arg2).isdigit() is True:
                    if str(arg1) == "remove":
                        oldlist = config.blacklist
                        oldlist.remove(str(arg2))
                        importlib.reload(config)
                        em = discord.Embed(title = "Success", description = f"Successfully removed <@!{str(arg2)}> from the blacklist.")
                        await ctx.reply(embed = em, mention_author=False, delete_after=5.0)
                    elif str(arg1) == "add":
                        importlib.reload(config)
                        with open('config.py', 'r') as file1:
                            filedata = file1.read()
                        oldlist = config.blacklist
                        print(oldlist)
                        oldlist.append(str(arg2))
                        with open('tempconfig.py', 'w') as file:
                            file.write(str(oldlist))
                        with open('tempconfig.py', 'r') as file2:
                            filedata1 = file2.read()
                        print(str(config.blacklist))
                        print(str(filedata1))
                        filedata2 = filedata.replace(str(config.blacklist), str(filedata1))
                        with open('tempconfig2.py', 'w') as file3:
                            file3.write(filedata2)
                    elif str(arg1) == "list":
                        em = discord.Embed(title = "Blacklisted Users")
                        em.add_field(name = "User IDs", value = '\n'.join(list(config.blacklist)))
                        #em.add_field(name = "User Mentions", value = "<@!" + *config.blacklist, sep = "\n") + ">")
                        await ctx.reply(embed = em, mention_author=False, delete_after=10.0)
                    else:
                        em = discord.Embed(title = "Error", description = f"`{str(arg1)}` doesn't seem to be a valid option. The valid options are `add` and `remove`.")
                        await ctx.reply(embed = em, mention_author=False, delete_after=5.0)
                else:
                    em = discord.Embed(title = "Error", description = f"`{str(arg2)}` doesn't look like a User ID.")
                    await ctx.reply(embed = em, mention_author=False, delete_after=5.0)
            elif choice == "leaveserver":
                if arg1 is None:
                    server = self.bot.get_guild(int(ctx.guild.id))
                else:
                    server = self.bot.get_guild(int(arg1))
                await server.leave()
                embed = discord.Embed(title = f"Left the server '{server.name}'.", color = discord.Color.green())
                await ctx.reply(embed=embed, mention_author=False)
            elif choice == "getchannels":
                server = self.bot.get_guild(int(arg1))
                embed = discord.Embed(title = f"List of channels for the server '{server.name}'", color = discord.Color.blue())
                for channel in server.channels:
                    embed.add_field(name = channel.name, value = channel.type)
                await ctx.reply(embed=embed, mention_author=False)
            elif choice == "getinvite":
                if arg2 is not None:
                    channelQuery = arg2
                elif arg2 is None:
                    channelQuery = "general"
                server = self.bot.get_guild(int(arg1))
                embed = discord.Embed(title = f"Generated invite for '{server.name}'", color = discord.Color.blue())
                for channel in server.channels:
                    if channel.name.__contains__(channelQuery):
                        searchchannel = channel
                        break
                    else:
                        searchchannel = False
                try:
                    if searchchannel is not False:
                        for i in await server.invites():
                            if str(i.channel) == searchchannel.name:
                                invite = str(i.url)
                                inviter = str(i.inviter)
                                channelname = i.channel.name
                                channelid = i.channel.id
                                break
                            else:
                                searchchannel = False
                    if searchchannel is False:
                        for i in await server.invites():
                            invite = str(i.url)
                            inviter = i.inviter
                            channelname = i.channel.name
                            channelid = i.channel.id
                            embed.set_footer(text="There were no invites for the channel you specified.\nThe bot used the first invite available.")
                            break
                except Exception:
                    em = discord.Embed(title="Warning", description="I don't seem to have permission to check invites.\nWould you like me to create a 1-time-use invite?", color=discord.Color.red())
                    emojilist = ["❌", "✅"]
                    def check(reaction, user):
                        return user == ctx.author and str(reaction.emoji) in emojilist
                    msg = await ctx.send(embed=em)
                    for emoji in emojilist:
                        await msg.add_reaction(f"{emoji}")
                    try:
                        reaction, user = await self.bot.wait_for("reaction_add", timeout=60, check=check)
                        if str(reaction.emoji) == "❌":
                            await msg.delete()
                            return
                        elif str(reaction.emoji) == "✅":
                            await msg.delete()
                            for channel in server.channels:
                                if channel.name.__contains__(channelQuery):
                                    invite = await channel.create_invite(max_age=600, max_uses=1, reason="Bot owner generated, this invite will expire after 10 minutes and has 1 use.")
                                    channelname = channel.name
                                    channelid = channel.id
                                    inviter = str(self.bot.user.name)
                                    embed.set_footer(text="This invite was generated by the bot.\nIt has 1 use and will expire in 10 minutes.")
                                    break
                    except asyncio.TimeoutError:
                        await msg.delete()
                        return    
                embed.add_field(name = "Channel Name", value = str(channelname))
                embed.add_field(name = "Channel ID", value = str(channelid))
                embed.add_field(name = "Channel Invite", value = invite)
                embed.add_field(name = "Inviter", value = str(inviter))
                await ctx.reply(embed=embed, mention_author=False)
            elif choice == "servers":
                servers = list(self.bot.guilds)
                embed = discord.Embed(title = f"Connected on {str(len(servers))} servers:", color = discord.Color.blue())
                embed.add_field(name = "Servers", value = '\n'.join(guild.name for guild in self.bot.guilds))
                embed.add_field(name = "Server IDs", value = '\n'.join(str(guild.id) for guild in self.bot.guilds))
                await ctx.reply(embed=embed, mention_author=False)
            elif choice == "shutdown":
                first_embed = discord.Embed(title = "Shutting down bot...", color = discord.Color.blue())
                msg = await ctx.reply(embed=first_embed, mention_author=False)
                new_embed = discord.Embed(title = "Shut down bot!", description = "Check your console, as it may still be running a subprocess. If it is, press `ctrl + c` on your keyboard to end the process.", color = discord.Color.green())
                await msg.edit(embed=new_embed)
                await ctx.bot.close()
            elif choice == "restart":
                first_embed = discord.Embed(title = "Restarting bot...", color = discord.Color.blue())
                msg = await ctx.reply(embed=first_embed, mention_author=False)
                dir_path = os.getcwd()
                subprocess.Popen(['python3', f'{dir_path}/bot.py'])
                new_embed = discord.Embed(title = "Restarted bot!", color = discord.Color.green())
                await msg.edit(embed=new_embed)
                await ctx.bot.close()
            elif choice == "load":
                args = f"cogs.{arg1}"
                self.bot.load_extension(args)
                em = discord.Embed(title = "Cog Loaded", description = "`" + args + "` has been loaded.", color = discord.Color.green())
                await ctx.reply(embed=em, mention_author=False)
            elif choice == "unload":
                args = f"cogs.{arg1}"
                self.bot.unload_extension(args)
                em = discord.Embed(title = "Cog Unloaded", description = "`" + args + "` has been unloaded.", color = discord.Color.green())
                await ctx.reply(embed=em, mention_author=False)
            elif choice == "stats":
                em = discord.Embed(title="Stats")
                try:
                    em.add_field(name="Total Executed Commands", value=f"{str(len(self.bot.commandsran))} commands")
                except Exception:
                    em.add_field(name="Total Executed Commands", value="No commands have been executed yet.")
                try:
                    newlist = self.bot.commandsran
                    test = []
                    dictionary = {}
                    def sortfunc(e):
                        return e['amount']
                    for item in newlist:
                        dictionary = {}
                        counted = newlist.count(item)
                        dictionary["command"] = item
                        dictionary["amount"] = int(counted)
                        if dictionary not in test:
                            test.append(dictionary)
                        del dictionary
                    test.sort(key=sortfunc, reverse=True) 
                    #print(test)
                    number = 0
                    commanduses = []
                    for item in test:
                        if number != 4:
                            try:
                                commanduses.append("**Name:** `"+str(item["command"])+"`; **Amount**: `"+str(item["amount"])+"`")
                                number = number+1
                            except Exception:
                                break
                    if commanduses != []:
                        em.add_field(name="Most Used Commands", value="\n".join(commanduses))
                    else:
                        em.add_field(name="Most Used Commands", value="No commands have been ran yet.")
                except Exception:
                    em.add_field(name="Most Used Commands", value="No commands have been ran yet.")
                try:
                    list1 = self.bot.errors
                    list1.reverse()
                    errorlist = []
                    for x in range(4):
                        try:
                            dictionary = list1[x]
                            errorlist.append("**-** `"+str(dictionary["command"])+"` at `"+str(dictionary["time"])+"`:\n```fix\n"+str(dictionary["error"])+"\n```")
                        except Exception:
                            break
                    if dictionary != {}:
                        em.add_field(name="Recent Errors", value="\n".join(errorlist), inline=False)
                    else:
                        em.add_field(name="Recent Errors", value="There have not been any errors since the bot started.")
                except Exception:
                    em.add_field(name="Recent Errors", value="There have not been any errors since the bot started.", inline=False)
                await ctx.send(embed=em)
            else:
                em = discord.Embed(title="Help", color=discord.Color.blue())
                em.set_author(name="Admin (Bot Owner Only) Commands")
                em.add_field(name=f"`{config.prefix}admin servers`", value="Shows the servers the bot is in")
                em.add_field(name=f"`{config.prefix}admin getinvite (serverid) [channelname]`", value="Generates an invite for a server the bot is in")
                em.add_field(name=f"`{config.prefix}admin getchannels (serverid)`", value="Gets a list of channels in a server")
                em.add_field(name=f"`{config.prefix}admin reload (cog)`", value="Reloads a cog")
                em.add_field(name=f"`{config.prefix}admin unload (cog)`", value="Unloads a cog")  
                em.add_field(name=f"`{config.prefix}admin load (cog)`", value="Loads a cog")
                em.add_field(name=f"`{config.prefix}admin blacklist (add, remove, list) (userid)`", value="Manages the bot blacklist")
                em.add_field(name=f"`{config.prefix}admin update`", value="Updates the bot (Linux only)")
                em.add_field(name=f"`{config.prefix}admin updatecheck`", value="Checks for updates to the bot") 
                em.add_field(name=f"`{config.prefix}admin shutdown`", value="Shuts down the bot")  
                em.add_field(name=f"`{config.prefix}admin restart`", value="Restarts the bot")    
                em.add_field(name=f"`{config.prefix}admin stats`", value="Shows bot stats")
                await ctx.send(embed=em)
        else:
            em = discord.Embed(title = "This command is for the bot owner only.", color = discord.Color.red())
            await ctx.reply(embed=em, mention_author=False)

    @commands.command()
    async def mostusedcmds(self, ctx, amount=3):
        em = discord.Embed(title="Most Used Commands", color=discord.Color.blue())
        newlist = self.bot.commandsran
        test = []
        dictionary = {}
        def sortfunc(e):
            return e['amount']
        for item in newlist:
            dictionary = {}
            counted = newlist.count(item)
            dictionary["command"] = item
            dictionary["amount"] = int(counted)
            if dictionary not in test:
                test.append(dictionary)
            del dictionary
        test.sort(key=sortfunc, reverse=True) 
        #print(test)
        number = 0
        for item in test:
            if number != amount:
                try:
                    em.add_field(name=str(item["command"]), value="Amount of times ran: "+str(item["amount"]))
                    number = number+1
                except:
                    break
        await ctx.send(embed=em)

    @commands.command()
    async def recenterrors(self, ctx, amount=3):
        list1 = self.bot.errors
        list1.reverse()
        em = discord.Embed(title="Recent Errors")
        for x in range(amount):
            try:
                dictionary = list1[x]
                em.add_field(name=str(dictionary["command"]), value=str(dictionary["error"]))
            except Exception:
                break
        await ctx.send(embed=em)

def setup(bot):
    bot.add_cog(Utils(bot))

# Copyright (C) 2021-present reoccurcat
# This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
# You should have received a copy of the GNU General Public License along with this program.  If not, see <http://www.gnu.org/licenses/>.

import discord
import os
import shutil
import sys
import subprocess
import config
import globalconfig
import importlib
from shutil import copyfile
from discord.ext import commands
from git import Repo
#from stat import S_IREAD, S_IRGRP, S_IROTH, S_IWUSR


class Update(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def updatecheck(self, ctx):
        """Attempts to check for updates using the GitHub repository"""
        if str(ctx.message.author.id) == config.ownerID:
            # username = os.getlogin()
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
            first_embed = discord.Embed(title = "Checking for updates...", description = "FreeDiscord is now checking for updates. Please be patient.", color = discord.Color.blue())
            # send a first message with an embed
            msg = await ctx.send(embed=first_embed)
            DEST_NAME = tmpdir + '/updatecheck'
            cloned_repo = Repo.clone_from(HTTPS_REMOTE_URL, DEST_NAME)
            dir_path = os.getcwd()
            copyfile(tmpdir + '/updatecheck/globalconfig.py', dir_path + '/updateconfig.py')
            try:
                shutil.rmtree(tmpdir + '/updatecheck')
            except os.error:
                embed = discord.Embed(title = "Error in removing `" + tmpdir + "/updatecheck` folder", description = 'The `' + tmpdir + '/updatecheck` folder was not able to be removed, probably due to a permissions issue.', color = discord.Color.red())
                await ctx.send(embed=embed) 
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

        else:
            em = discord.Embed(title = "This command is for the bot owner only.", color = discord.Color.red())
            await ctx.send(embed = em)

    @commands.command()
    async def updatebot(self, ctx):
        """Attempts to update the bot directly from the GitHub repository."""
        #platform = sys.platform
        if str(ctx.message.author.id) == config.ownerID:
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
                em = discord.Embed(title = "Updated!", description = "FreeDiscord updated! No error reported. Check your console to confirm this.", color = discord.Color.green())
                em.add_field(name = "Note", value = "The bot will now restart. If it doesn't, start it up manually. If it won't start, open an issue in FreeDiscord's GitHub repository.")
                await ctx.send(embed = em)
                dir_path = os.getcwd()
                subprocess.Popen(['python3', f'{dir_path}/bot.py'])
                await ctx.bot.close()
           elif sys.platform == "win32":
                em = discord.Embed(title = "`updatebot` is not yet available for Windows.", color = discord.Color.red())
                await ctx.send(embed = em)
           elif sys.platform == "darwin":
                em = discord.Embed(title = "`updatebot` is not yet available for macOS.", color = discord.Color.red())
                await ctx.send(embed = em)

        else:
            em = discord.Embed(title = "This command is for the bot owner only.", color = discord.Color.red())
            await ctx.send(embed = em)

    @commands.command()
    async def updatecogs(self, ctx):
        """Updates cogs, but not the bot."""
        if str(ctx.message.author.id) == config.ownerID:
            # username = os.getlogin()
            try:
                os.mkdir('./tmp/cogupdate')
            except OSError:
                os.rmdir('./tmp/cogupdate')
                os.mkdir('./tmp/cogupdate')
            HTTPS_REMOTE_URL = globalconfig.github_login_url
            DEST_NAME = './tmp/cogupdate'
            cloned_repo = Repo.clone_from(HTTPS_REMOTE_URL, DEST_NAME)
            dir_path = os.getcwd()
            shutil.rmtree(dir_path + "/cogs/")
            path = dir_path
            src = './tmp/cogupdate/cogs'
            dest = dir_path + "/cogs"
            destination = shutil.copytree(src, dest)
            shutil.rmtree('./tmp/cogupdate')
            print("Done! Restart the bot to apply the changes!")
            em = discord.Embed(title = "Updated!", description = "Cogs updated! No error reported. Check your console to confirm this.", color = discord.Color.green())
            em.add_field(name = "Note", value = "If you want to use the new cogs, either restart the bot using `" + config.prefix + "restartbot` which will load all the cogs on startup (recommended), or reload every cog manually using `" + config.prefix + "reloadcog {every cog name}.`")
            await ctx.send(embed = em)
        else:
            em = discord.Embed(title = "This command is for the bot owner only.", color = discord.Color.red())
            await ctx.send(embed = em)


def setup(bot):
    bot.add_cog(Update(bot))

# reoccurcord
## Welcome to the official GitHub page of the reoccurcord bot!

### To invite the bot, click [here](https://rc.reoccur.tech/invite). 
### For the ToS, click [here](https://rc.reoccur.tech/tos).
### For the Privacy Policy, click [here](https://rc.reoccur.tech/privacy).

reoccurcord is a Discord bot made formerly by the reoccurdevs team but taken over by the last dev that worked on it that you can edit and self host. If you fork this project, please don't make a new project acting like this project is dead. **It isn't.** If you want to fork it and make a new bot, that's fine, but please give us credit. :)
If you find an issue, or have a feature suggestion, please let us know by opening an issue [here](https://github.com/reoccurcat/reoccurcord/issues).

## Documentation

### Starting the bot
#### Make sure you have [Python 3](https://www.python.org/downloads/) installed (and put in path, if you're on Windows 10)!!!
1. Clone the repository: `git clone https://github.com/reoccurcat/reoccurcord.git` and go to step 2. An alternative is to download the ZIP file, unzip it, shift + right click in the `reoccurcord-main` folder, click on `Open Powershell window here`, and continue with step 3.
2. `cd` to the repository folder: `cd reoccurcord`.
3. Make sure all the dependencies are installed, Windows: `python -m pip install discord.py requests asyncio gitpython psutil datetime bs4 jishaku` (add `nudenet` and `tensorflow-cpu` if you want NSFW detection) Linux: `pip3 install discord.py requests asyncio gitpython psutil datetime bs4 jishaku` (add `nudenet` and `tensorflow-cpu` if you want NSFW detection). If there are any other errors with importing dependencies, install them as necessary.
4. Run `python3 setup.py` for a configuration creator. If you don't do this, the bot will not run.
5. Before starting, make sure the Server Members Intent is enabled in your bot settings in the Discord Developer Portal.
6. To make sure the `mute` and `unmute` commands work, please make a role called `muted` in your server. The bot will not (yet) do this for you. After you create the role, make sure to create overrides for the channels you don't want a muted user speaking in.
7. Run the main bot file: `python3 start.py` (or see the commands with `python3 start.py --help`).

### Features

There are many features of the bot. These features include:

- VirusTotal file scanning
- Message encryption
- Moderation
- Fun commands
- Utility commands
- Custom playing status that you can customize per instance
- Self updating feature
- Lots more commands, and more commands being added regularly!

You can find the support server here:

[![Join our Discord server!](https://invidget.switchblade.xyz/xzPRBF9bhd)](http://discord.gg/xzPRBF9bhd)

You can invite the main bot instance here:

[Main Bot Invite Link](https://rc.reoccur.tech/invite)

Like earlier said, if you have any feature requests or issues with the bot, open an issue [here](https://github.com/reoccurcat/reoccurcord/issues)!
Enjoy the bot! We hope you have as much fun with it as we had programming it! :)

Made with discord.py v9.

# Copyright (C) 2021-present reoccurcat
# This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
# You should have received a copy of the GNU General Public License along with this program.  If not, see <http://www.gnu.org/licenses/>.

import os

print("Welcome to the reoccurcord interactive setup script!")
def tokenWrite() :
    writeBotToken = input("Enter your bot token: ")
    verificationOne = input("Is this correct? (y/n): '" + writeBotToken + "'")
    if verificationOne == "y":
        print("Writing...")
        writeTokenTemplate = "bot_token = '" + writeBotToken + "'\n"
        config = open('config.py', 'a')
        config.write(writeTokenTemplate)
        config.close()
        print("Written!")
        print()
    elif verificationOne == "n":
        print("Please rerun the file and input the correct bot token.")
        exit()
    elif verificationOne != "n" or "y":
        print("Invalid response, please rerun the script.")
        exit()

def prefixWrite() :
    writePrefix = input("Enter the bot's prefix: ")
    verificationTwo = input("Is this correct? (y/n): '" + writePrefix + "'")
    if verificationTwo == "y":
        print("Writing...")
        config = open('config.py', 'a')
        writePrefixTemplate = "prefix = '" + writePrefix + "'\n"
        config.write(writePrefixTemplate)
        config.close()
        print("Written!\n")
        #print(writeTokenTemplate)
    elif verificationTwo == "n":
        print("Please rerun the file and input your preferred bot prefix.")
        exit()
    elif verificationTwo != "n" or "y":
        print("Invalid response, please rerun the script.")
        exit()

def ownerIDWrite() :
    ownerIDinput = input("Enter the bot owner's user ID: ")
    verificationThree = input("Is this correct? (y/n): '" + ownerIDinput + "'")
    if verificationThree == "y":
        print("Writing...")
        config = open('config.py', 'a')
        writePrefixTemplate = "ownerID = '" + ownerIDinput + "'\n"
        config.write(writePrefixTemplate)
        config.close()
        config = open('config.py', 'r')
    elif verificationThree == "n":
        print("Please rerun the file and input the bot owner's user ID")
        exit()
    elif verificationThree != "n" or "y":
        print("Invalid response, please rerun the script.")
        exit()

def vtapiWrite() :
    print("If you don't have a VirusTotal API key, or don't want this feature, just hit enter on this prompt and type 's' when it asks if what you inputted is correct.\n")
    vtapiToken = input("Enter your VirusTotal API key: ")
    verificationFour = input("Is this correct? (y/n/s): '" + vtapiToken + "'")
    if verificationFour == "y":
        print("Writing...")
        config = open('config.py', 'a')
        writePrefixTemplate = "virustotal_api = '" + vtapiToken + "'\n"
        config.write(writePrefixTemplate)
        config.close()
        print("Written!")
        print()
    elif verificationFour == "n":
        print("Please rerun the file and input your VirusTotal API key.")
        exit()
    elif verificationFour == "s":
        print("Writing...")
        config = open('config.py', 'a')
        writePrefixTemplate = "virustotal_api = ''\n"
        config.write(writePrefixTemplate)
        config.close()
        print("Written!")
        print()
        print("You have chosen not to input a VirusTotal API key. You may add one by editing the config.py file later.")
    elif verificationFour != "n" or "y" or "s":
        print("Invalid response, please rerun the script.")
        exit()

def badwordWrite() :
    print("Please put in bad words that you want to be filtered by the bot.\nIf you don't want this feature just hit enter on this prompt and type 's' when it asks if what you inputted is correct.\nThe format is ")
    print('["badword1", "badword2", "badword3"]')
    badwords = input("Enter the bad words (make sure to use the format): ")
    verificationFour = input("Is this correct? (y/n/s): '" + badwords + "'")
    if verificationFour == "y":
        print("Writing...")
        config = open('config.py', 'a')
        writePrefixTemplate = "bad_words = " + badwords + "\n"
        config.write(writePrefixTemplate)
        config.close()
        print("Written!")
        print()
    elif verificationFour == "n":
        print("Please rerun the file and input the bad words you want to be filtered.")
        exit()
    elif verificationFour == "s":
        print("Writing...")
        config = open('config.py', 'a')
        writePrefixTemplate = "bad_words = []\n"
        config.write(writePrefixTemplate)
        config.close()
        print("Written!")
        print()
        print("You have chosen not to input bad words. You may add them by editing the config.py file later.")
    elif verificationFour != "n" or "y" or "s":
        print("Invalid response, please rerun the script.")
        exit()

def blacklistWrite() :
    print("Please put in blacklisted users that can't use the bot.\nIf you don't want this feature just hit enter on this prompt and type 's' when it asks if what you inputted is correct.\nThe format is ")
    print('["blacklisteduser1", "blacklisteduser2", "blacklisteduser3"]')
    blacklist = input("Enter the bad words (make sure to use the format): ")
    verificationFour = input("Is this correct? (y/n/s): '" + blacklist + "'")
    if verificationFour == "y":
        print("Writing...")
        config = open('config.py', 'a')
        writePrefixTemplate = "blacklist = " + blacklist + "\n"
        config.write(writePrefixTemplate)
        config.close()
        print("Written!")
        print()
    elif verificationFour == "n":
        print("Please rerun the file and input the bad words you want to be filtered.")
        exit()
    elif verificationFour == "s":
        print("Writing...")
        config = open('config.py', 'a')
        writePrefixTemplate = "blacklist = []\n"
        config.write(writePrefixTemplate)
        config.close()
        print("Written!")
        print()
        print("You have chosen not to input bad words. You may add them by editing the config.py file later.")
    elif verificationFour != "n" or "y" or "s":
        print("Invalid response, please rerun the script.")
        exit()

def dateformatWrite() :
    print("Please choose the date format you want to use in the commands.")
    print("Choices: 1) day/month/year hour:minutes AM/PM 2) month/day/year hour:minutes AM/PM 3) day/month/year hour:minutes (24 hour) 4) month/day/year hour:minutes (24 hour)")
    writedateformat = input("Enter the number of your choice: ")
    verificationOne = input("Is this correct? (y/n): '" + writedateformat + "'")
    if verificationOne == "y":
        print("Writing...")
        if writedateformat == "1":
            writeDateFormatTemplate = "date_format = '%d/%m/%Y, %I:%M %p'\n"
        elif writedateformat == "2":
            writeDateFormatTemplate = "date_format = '%m/%d/%Y, %I:%M %p'\n"
        elif writedateformat == "3":
            writeDateFormatTemplate = "date_format = '%d/%m/%Y, %H:%M'\n"
        elif writedateformat == "4": 
            writeDateFormatTemplate = "date_format = '%m/%d/%Y, %H:%M'\n"
        else:
            print("Invalid response, please rerun the script.")
        config = open('config.py', 'a')
        config.write(writeDateFormatTemplate)
        config.close()
        print("Written!")
        print()
    elif verificationOne == "n":
        print("Please rerun the file and input the correct number.")
        exit()
    elif verificationOne != "n" or "y":
        print("Invalid response, please rerun the script.")
        exit()

def firstwebhookwrite() :
    print("Please put in the webhook URL for sending information messages to.\n")
    print("If you don't want this feature, just put 's' in when it asks if it is correct.")
    webhook = input("Enter the webhook URL:")
    verificationFour = input("Is this correct? (y/n/s): '" + webhook + "'")
    if verificationFour == "y":
        print("Writing...")
        config = open('config.py', 'a')
        writePrefixTemplate = "infowebhook = " + str(webhook) + "\n"
        config.write(writePrefixTemplate)
        config.close()
        print("Written!")
        print()
    elif verificationFour == "n":
        print("Please rerun the file and input the webhook to use for information.")
        exit()
    elif verificationFour == "s":
        print("Writing...")
        config = open('config.py', 'a')
        writePrefixTemplate = "infowebhook = ''\n"
        config.write(writePrefixTemplate)
        config.close()
        print("Written!")
        print()
        print("You have chosen not to input an info webhook. You may add them by editing the config.py file later.")
    elif verificationFour != "n" or "y" or "s":
        print("Invalid response, please rerun the script.")
        exit()

def firstwebhookwrite() :
    print("Please put in the webhook URL for sending admin messages to.\n")
    print("If you don't want this feature, just put 's' in when it asks if it is correct.")
    webhook = input("Enter the webhook URL:")
    verificationFour = input("Is this correct? (y/n/s): '" + webhook + "'")
    if verificationFour == "y":
        print("Writing...")
        config = open('config.py', 'a')
        writePrefixTemplate = "adminwebhook = " + str(webhook) + "\n"
        config.write(writePrefixTemplate)
        config.close()
        print("Written!")
        print()
    elif verificationFour == "n":
        print("Please rerun the file and input the webhook to use for information.")
        exit()
    elif verificationFour == "s":
        print("Writing...")
        config = open('config.py', 'a')
        writePrefixTemplate = "adminwebhook = ''\n"
        config.write(writePrefixTemplate)
        config.close()
        print("Written!")
        print()
        print("You have chosen not to input an info webhook. You may add them by editing the config.py file later.")
    elif verificationFour != "n" or "y" or "s":
        print("Invalid response, please rerun the script.")
        exit()

if os.path.exists("config.py"):
    if os.stat("config.py").st_size == 0:
        os.remove("config.py")
    else:
        prompt = input("Existing config.py found. Should I delete it? (y/n)")
        if prompt == "y":
            print("Deleting existing config file...")
            os.remove("config.py")
            print("Deleted! Continuing with normal script now...")
            print()
        elif prompt == "n":
            print("Exiting...")
            exit()
        elif prompt != "n" or "y":
            print("Invalid response, please rerun the script.")
            exit()

tokenWrite()
prefixWrite()
ownerIDWrite()
vtapiWrite()
badwordWrite()
dateformatWrite()
blacklistWrite()
firstwebhookwrite()

config = open('config.py', 'a')
config.write("latest_version = 'unknown'")
config.close()
print("Your configuration file should be written now!")
print("To start your bot, run 'python3 start.py'")
print("Have a nice day! :)")
exit()
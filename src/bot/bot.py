"""Minimalist discord.py bot acting as an interface for the dbots-api."""
import aiohttp
from os import getenv

try:  # in case discord.py or simplejson isn't installed
    import discord
    from discord.ext import commands
    import simplejson as json  # to manage databases
except ModuleNotFoundError:  # install the discord modules
    import subprocess
    import sys as system

    subprocess.check_call([system.executable, '-m', 'pip', 'install', "discord.py"])
    subprocess.check_call([system.executable, '-m', 'pip', 'install', "simplejson"])
    import discord
    from discord.ext import commands
    import simplejson as json

decoder = json.JSONDecoder()

prefix = "e!"
api_path = "https://the-eggbot-27.herokuapp.com/"

intents = discord.Intents.all()
bot = discord.Client(intents=intents)

command = json.load(open('bot/commands.json', 'r'), "utf-8")
# imgs = json.load(open('images.json', 'r'), "utf-8")


@bot.event
async def on_ready():
    print('We have logged in as ' + bot.user.name + "#" + bot.user.discriminator)
    await bot.change_presence(activity=discord.Game(name='{p}help'.format(p=prefix)))


@bot.event
async def on_message(message):
    if message.author.bot:
        return  # don't let bots ddos
    messes = message.content.split()[0]
    mess = messes[0].lower()
    if "\\" in mess or "/" in mess:
        return  # avoid url escape attempts
    if mess.startswith(prefix):
        mess = mess[2:]
    uri = f"{api_path}?message={mess}"  # base thing like egg
    if mess in command:
        uri = f"{api_path}{command[mess]}{' '.join(messes[1:])}"
    try:
        print((str((await request(uri)), "utf-8")))
        await message.channel.send(decoder.decode(str((await request(uri)), "utf-8"))["message"])
    except KeyError:  # replace with typeerror and pass for 1) nothing and send for 2) img
        pass


async def request(uri: str):
    async with aiohttp.request('get', uri) as res:
        if res.status == 200:
            return await res.read()
        else:
            raise FileNotFoundError


try:
    token = getenv('token')
    if not token:
        input('The "token" environment variable was not found!\n Press enter to exit.')
        exit(0)
    bot.run(token)
except (FileNotFoundError, NameError):
    input("The bot token was not found! Press enter to exit...")

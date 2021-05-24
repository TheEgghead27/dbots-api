"""Minimalist discord.py bot acting as an interface for the dbots-api."""
from io import BytesIO

import aiohttp
from os import getenv

try:  # in case discord.py or simplejson isn't installed
    import discord
    import simplejson as json  # to manage databases
except ModuleNotFoundError:  # install the discord modules
    import subprocess
    import sys as system

    subprocess.check_call([system.executable, '-m', 'pip', 'install', "discord.py"])
    subprocess.check_call([system.executable, '-m', 'pip', 'install', "simplejson"])
    import discord
    import simplejson as json

decoder = json.JSONDecoder()

prefix = "e!"
api_path = "https://egglamp.herokuapp.com/"

intents = discord.Intents.default()
bot = discord.Client(intents=intents)

commands = json.load(open('src/bot/commands.json', 'r'), "utf-8")
imgs = json.load(open('src/bot/images.json', 'r'), "utf-8")
helpEmbed = None


@bot.event
async def on_ready():
    print('We have logged in as ' + bot.user.name + "#" + bot.user.discriminator)

    global helpEmbed
    if not helpEmbed:
        helpEmbed = discord.Embed(title=f"{bot.user.name} commands")
        d = ""
        for i in commands:
            d += f"`{prefix}{i}`, "
        helpEmbed.add_field(name="Fun", value=d.rstrip(", "))
        d = ""
        for i in imgs:
            d += f"`{prefix}{i}`, "
        helpEmbed.add_field(name="Image Manip", value=d.rstrip(", "))
        helpEmbed.set_footer(text=f"Additional information can be found at {api_path}docs")

    await bot.change_presence(activity=discord.Game(name='{p}help'.format(p=prefix)))


@bot.event
async def on_message(message):
    if message.author.bot:
        return  # don't let bots ddos
    messes = message.content.split()
    mess = messes[0].lower()
    if "\\" in mess or "/" in mess:
        return  # avoid url escape attempts
    uri = f"{api_path}?message={mess}"  # base thing like egg
    if mess.startswith(prefix):
        mess = mess[2:]
        if mess in commands:
            uri = f"{api_path}{commands[mess]}{' '.join(messes[1:])}"
        elif mess in imgs:
            try:
                uri = f"{api_path}images/{imgs[mess][0]}?image_url={messes[1]}"
                if len(imgs[mess]) >= 2:
                    try:
                        for j in range(2, len(imgs[mess]) + 1):
                            uri += f"&{imgs[mess][j - 1]}={messes[j]}"
                    except IndexError:
                        try:
                            # noinspection PyUnboundLocalVariable
                            uri = f"{api_path}say?" \
                                  f"message={messes[0]}%20requires%20another%20argument,%20`{imgs[mess][j - 1]}`!"
                        except NameError:
                            print("what the fuck fuck fuck code broken")
                            return
            except IndexError:
                uri = f"{api_path}say?message={messes[0]}%20requires%20an%20image%20URL!"
        elif mess == "help":
            if helpEmbed:  # this is the only thing that needs on_ready to be ready which is when it sets helpEmbed
                await message.channel.send(embed=helpEmbed)

    data = (await request(uri))
    try:
        try:
            out = decoder.decode(str(data, "utf-8"))
            await message.channel.send(out["message"])
        except KeyError:
            # noinspection PyUnboundLocalVariable
            try:
                # noinspection PyUnboundLocalVariable
                if out["detail"] == "Not Found":
                    raise FileNotFoundError
            except (KeyError, NameError):
                pass

            await message.channel.send(f'```\nError: {out["detail"][0]["loc"][1]}\'s {out["detail"][0]["msg"]}\n```')
        except TypeError:
            pass
    except discord.errors.HTTPException:
        try:
            cookbook = decoder.decode(str(data, "utf-8"))["message"]
            await message.channel.send(cookbook[:1987])
            await message.channel.send(cookbook[1987:])
        except discord.errors.HTTPException:
            pass
        except TypeError:
            pass  # why i havent resorted to on_error yet is sheer laziness
    except KeyError:  # replace with typeerror and pass for 1) nothing and send for 2) img
        print(f"KeyError of {uri}")
        pass
    except UnicodeDecodeError:
        image = BytesIO(data)
        image.seek(0)
        await message.channel.send(file=discord.File(image, imgs[mess][0]))
    except FileNotFoundError:
        await message.channel.send("It appears that my brain has malfunctioned.")
        raise FileNotFoundError(uri + " broken pleas fix manager")


async def request(uri: str):
    # print(f"Getting {uri}")
    async with aiohttp.request('get', uri) as res:
        # if res.status == 200:
        return await res.read()
        # else:
        # raise FileNotFoundError


try:
    token = getenv('token')
    if not token:
        input('The "token" environment variable was not found!\n Press enter to exit.')
        exit(0)
    bot.run(token)
except (FileNotFoundError, NameError):
    input("The bot token was not found! Press enter to exit...")

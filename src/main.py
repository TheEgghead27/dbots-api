from fastapi import FastAPI
from random import choice, randint
import re as regex
import deeppyer
from pydantic import BaseModel
from typing import Union
from aiohttp import request
from io import BytesIO
from PIL import Image, ImageOps, ImageEnhance

from data import *


app = FastAPI()


@app.get("/")
async def autoreply(message: str):
    """Port of simple commands/responses in Eggbot and autoresponses from Catlamp"""
    command = message
    message = command.lower()
    # hahaha yandev go brrr
    for i in mmyes:
        if message.startswith(i):
            return {"message": i}
    if message.startswith(eggTrigger):
        return {"message": choice(eggs)}
    elif message.startswith(("simp", "sɪᴍᴘ")):
        return {"message": choice(simp)}
    elif message.startswith(('moyai', '🗿', ':moyai:', 'mooyai')):
        return {"message": '🗿'}

    elif "do not the sex" in message:
        return {"message": "do not the sex"}
    elif "do the sex" in message:
        return {"message": "do NOT the sex"}
    elif "psps" in message:
        # piss counter
        piss = 0
        for _ in regex.findall("ps", message):
            piss += 1

        # full piss counter
        capitals = 0
        for _ in regex.findall("PS", command):
            capitals += 2
        if capitals / 2 == piss:  # if it's all PS, let it w i d e
            # print('piss')
            piss = 3

        if piss >= 3:
            for _ in regex.findall(regex.compile("[P, S][p,s]|[p, s][P, S]"), message):
                capitals += 1

            if capitals >= 3:
                return {"message": ":lampstarenear:"}
        return {"message": ":lampstare:"}


@app.get("/about")
async def about():
    """Returns information about the API."""
    return {
            "Description": "FastAPI API with ports of the functionality some of my Discord bot projects had.",
            "Author": "TheEgghead27",
            'GitHub': 'https://github.com/TheEgghead27/dbots-api'
            }


# i dunno if this is even legal
# @app.get("/bee")
# async def return_bee():
#     return {"message": bee}


@app.get("/random-kiri")
async def random_kiri():
    """Displays an image of Eijiro Kirishima from My Hero Academia. You can specify the number of images you want
        to be sent. [request from Discord user Amane#6008]"""
    return {"message": choice(kirilist)}


@app.get("/egg-recipes")
async def return_egg_recipes():
    """Lists all the known egg recipes."""
    return {"message": cookbook}


@app.get("/rate-food")
async def rate_food():
    """Rates your food like a certain angry chef"""
    return {"message": choice(insults)}


@app.get("/say")
async def say(message: str):
    """Echos the specified message"""
    return {"message": message}


@app.get("/coin-flip")
async def flip_coin():
    """Flips a coin."""
    rand = randint(0, 1)
    side = randint(1, 20)
    if side == 20:
        return {"message": "The coin landed on... its side?"}
    elif rand == 0:
        return {"message": "The coin landed on heads."}
    elif rand == 1:
        return {"message": "The coin landed on tails."}


positive = ["It is certain.", "It is decidedly so.", "Without a doubt.", "Yes – definitely.",
            "You may rely on it.", "As I see it, yes.", "Most likely.", "Outlook good.", "Yes.",
            "Signs point to yes."]
unsure = ["Reply hazy, try again.", "Ask again later.", "Better not tell you now.", "Cannot predict now.",
          "Concentrate and ask again."]
negative = ["Don't count on it.", "My reply is no.", "My sources say no.", "Outlook not so good.",
            "Very doubtful."]


@app.get("8ball")
async def consult_8_ball(question: str):
    """
    Asks the Magic 8-Ball a question.
    Disclaimer: The Magic 8-ball is not sentient and it does not represent the opinions its creators.
    """
    option = randint(1, 3)
    response = ""
    if option == 1:
        response = "🟢 " + choice(positive)
    elif option == 2:
        response = "🟡 " + choice(unsure)
    elif option == 3:
        response = "🔴 " + choice(negative)
    return {"message": f"🎱 The 8-ball has spoken. 🎱\nQuestion: {question}\nAnswer: {response}"}


# begin image manip mess
matcher = regex.compile(
    r'^(?:http|ftp)s?://'  # http:// or https://
    r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
    # r'localhost|' #localhost...
    r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
    r'(?::\d+)?'  # optional port
    r'(?:/?|[/?]\S+)$', regex.IGNORECASE)

catLampTemplate = Image.open('images/catlamp-outlineonly.png', mode='r').convert('RGBA')
dioTemplate = Image.open('images/dio.png', mode='r').convert('RGBA')
flushedTemplate = Image.open('images/flushed.png', mode='r').convert('RGBA')
joyTemplate = Image.open('images/joy.png', mode='r').convert('RGBA')


async def getImage(image: str) -> Union[Image.Image, str]:
    if isinstance(image, str):
        if regex.match(matcher, image) and image.split("?")[0][-4:] in ('.png', '.jpg', 'jpeg', '.gif', 'webp'):
            async with request('get', image) as res:
                if res.status == 200:
                    image = await res.read()
                else:
                    return f'There was an issue getting the URL "{image}"!'
        else:
            return f'"{image}" is not a valid image URL!'
    try:
        image = Image.open(BytesIO(image))
    except Exception as e:
        image = str(e)
    return image


def packageImage(outImg: Image.Image, file_name: str = "image.png") -> dict:
    img = BytesIO()
    outImg.save(img, "png")
    img.seek(0)
    return {"image": img.read(), "file_name": file_name}


# define methods
@app.get("/images/deepfry")
async def deepfry(image_url: str):
    """Deepfries the attached image or your/the mentioned user's avatar."""
    image = await getImage(image_url)
    if isinstance(image, str):
        return {"detail": image}
    # noinspection PyTypeChecker
    deepImg = await deeppyer.deepfry(image, flares=False)
    deepImg = deepImg.convert('RGBA')  # i dunno, deepImg is an Image.py, but sendImage() wants Image
    return packageImage(deepImg, "deepfry.png")
# @app.get("/images/catlamp")
# async def make_catlamp(image: str):
#     image = getImage(image)


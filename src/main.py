from fastapi import FastAPI
from pydantic import BaseModel
from random import choice, randint
from re import findall, compile as comp

from data import *


class Image(BaseModel):
    image: bytes


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
        for _ in findall("ps", message):
            piss += 1

        # full piss counter
        capitals = 0
        for _ in findall("PS", command):
            capitals += 2
        if capitals / 2 == piss:  # if it's all PS, let it w i d e
            # print('piss')
            piss = 3

        if piss >= 3:
            for _ in findall(comp("[P, S][p,s]|[p, s][P, S]"), message):
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

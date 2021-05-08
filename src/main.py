from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
from random import choice
from re import findall, compile as comp

from data import *


class Image(BaseModel):
    image: bytes
    output_name: Optional[str]


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
    return {"message": choice(kirilist)}


@app.get("/egg-recipes")
async def egg_recipes():
    return {"message": cookbook}


@app.get("/rate-food")
async def rate_food():
    return {"message": choice(insults)}


@app.get("/echo")
async def say(message: str):
    return {"message": message}

import math
import random
from fastapi import FastAPI, Response
import re as regex
from typing import Union
from aiohttp import request
from io import BytesIO
from PIL import Image, ImageOps, ImageEnhance

try:
    from data import *
except ModuleNotFoundError:
    from src.data import *


app = FastAPI(title="Eggbot + Catlamp API (Working Title)",
              description="FastAPI API with ports of the functionality some of my Discord bot projects had.")


def markdown(text: str):
    # 2/7 chance of being codeBlock or empty, then 50/50
    divisor = 0
    for i in spic:
        # I don't want the last list's full girth to be considered,
        # but since it would raise the randrange cap to intended levels, it stays like this with no edits
        divisor += len(i) + 1

    if random.randrange(1, divisor + 1) <= 2:  # codeBlock and empty have to stay by themselves
        markedDown = random.choice(spic[-1])
    else:
        # Thanks Blue
        # Repeat until length(tempList) = amount of desired markdowns:
        #     Random = random(0, length markdown list)
        #     If !tempList.contains(markdown[random] {
        # //add to list
        # }
        length = random.randrange(1, len(spic[:-1]) + 1)
        markedDown = ''
        temp = []
        while len(temp) < length:
            thing = random.choice(spic[:-1])
            if thing not in tuple(temp):
                temp.append(thing)
                markedDown += random.choice(thing)

    return markedDown + text + markedDown[::-1]


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
        return {"message": markdown(random.choice(eggs))}
    elif message.startswith(("simp", "sɪᴍᴘ")):
        return {"message": markdown(random.choice(simp))}
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
                return {"message": rand_stare(True)}
        return {"message": rand_stare(False)}
    return {"message": None}


def rand_stare(urgent: bool) -> str:
    print(lampstares)
    if urgent:
        return random.choice(lampstares[1])
    return random.choice(lampstares[0])


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
    return {"message": random.choice(kirilist)}


@app.get("/egg-recipes")
async def return_egg_recipes():
    """Lists all the known egg recipes."""
    return {"message": cookbook}


@app.get("/rate-food")
async def rate_food():
    """Rates your food like a certain angry chef"""
    return {"message": random.choice(insults)}


@app.get("/say")
async def say(message: str):
    """Echos the specified message"""
    return {"message": message}


@app.get("/coin-flip")
async def flip_coin():
    """Flips a coin."""
    rand = random.randint(0, 1)
    side = random.randint(1, 20)
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


@app.get("/8ball")
async def consult_8_ball(question: str):
    """
    Asks the Magic 8-Ball a question.
    Disclaimer: The Magic 8-ball is not sentient and it does not represent the opinions its creators.
    """
    if not question.strip():
        return {"message": "Please give the 8-ball a query."}

    option = random.randint(1, 3)
    response = ""
    if option == 1:
        response = "🟢 " + random.choice(positive)
    elif option == 2:
        response = "🟡 " + random.choice(unsure)
    elif option == 3:
        response = "🔴 " + random.choice(negative)
    return {"message": f"🎱 The 8-ball has spoken. 🎱\nQuestion: {question}\nAnswer: {response}"}


@app.get("/markdown")
async def mark_down(string: str):
    if not string.strip():
        return {"message": "Please provide a base string to mark down."}
    return {"message": markdown(string)}


# begin image manip mess
matcher = regex.compile(
    r'^(?:http|ftp)s?://'  # http:// or https://
    r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
    # r'localhost|' #localhost...
    r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
    r'(?::\d+)?'  # optional port
    r'(?:/?|[/?]\S+)$', regex.IGNORECASE)

try:
    catLampTemplate = Image.open('images/catlamp-outlineonly.png', mode='r').convert('RGBA')
    dioTemplate = Image.open('images/dio.png', mode='r').convert('RGBA')
    flushedTemplate = Image.open('images/flushed.png', mode='r').convert('RGBA')
    joyTemplate = Image.open('images/joy.png', mode='r').convert('RGBA')
except FileNotFoundError:
    catLampTemplate = Image.open('src/images/catlamp-outlineonly.png', mode='r').convert('RGBA')
    dioTemplate = Image.open('src/images/dio.png', mode='r').convert('RGBA')
    flushedTemplate = Image.open('src/images/flushed.png', mode='r').convert('RGBA')
    joyTemplate = Image.open('src/images/joy.png', mode='r').convert('RGBA')


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
    except Exception as ex:
        image = str(ex)
    return image


# stole off the site with best SEO, https://note.nkmk.me/en/python-pillow-square-circle-thumbnail/
def centerSquare(pil_img: Image.Image):
    """Adds padding on both sides to make an image square. (Centered)"""
    pil_img = pil_img.convert('RGBA')  # ensure transparency
    background_color = (0, 0, 0, 0)
    width, height = pil_img.size
    if width == height:
        return pil_img
    elif width > height:
        result = Image.new(pil_img.mode, (width, width), background_color)
        result.paste(pil_img, (0, (width - height) // 2))
        return result
    else:
        result = Image.new(pil_img.mode, (height, height), background_color)
        result.paste(pil_img, ((height - width) // 2, 0))
        return result


def simpSquare(pil_img: Image.Image):
    """Adds padding to the bottom or right of an image to make it square."""
    background_color = (0, 0, 0, 0)
    width, height = pil_img.size
    if width == height:
        return pil_img
    elif width > height:
        result = Image.new(pil_img.mode, (width, width), background_color)
        result.paste(pil_img, (0, 0))
        return result, 'Y'
    else:
        result = Image.new(pil_img.mode, (height, height), background_color)
        result.paste(pil_img, (0, 0))
        return result, 'X'


def hippityHoppityThisColorIsDisappearity(img: Image.Image, color: tuple = (0, 255, 0)):
    """Alias for replaceColor() with a result of transparent white"""
    return replaceColor(img, targetIn=color, colorOut=(255, 255, 255, 0))


# https://stackoverflow.com/questions/765736/using-pil-to-make-all-white-pixels-transparent
def replaceColor(image: Image.Image, targetIn: tuple, colorOut: tuple):
    img = image.convert("RGBA")
    Data = img.getdata()

    newData = []
    try:
        for item in Data:
            if item[0] == targetIn[0] and item[1] == targetIn[1] and item[2] == targetIn[2] and item[3] == targetIn[3]:
                newData.append(colorOut)
            else:
                newData.append(item)
    except IndexError:
        for item in Data:
            if item[0] == targetIn[0] and item[1] == targetIn[1] and item[2] == targetIn[2]:
                newData.append(colorOut)
            else:
                newData.append(item)

    img.putdata(newData)

    return img


def findMonoAlphaTarget(image: Image.Image):
    satisfied = False
    potentialTarget = (0, 255, 0, 255)  # start with green
    blacklist = []
    Fuck = 0

    while not satisfied:
        if Fuck == 10:
            random.seed()
            Fuck = 0

        if potentialTarget not in blacklist:
            if potentialTarget in image.getdata():
                blacklist.append(potentialTarget)
            else:
                satisfied = True
        else:
            Fuck += 1

        # randomize target
        potentialTarget = (random.randrange(0, 256), random.randrange(0, 256), random.randrange(0, 256), 255)

    return potentialTarget


def findDualAlphaTarget(image1: Image.Image, image2: Image.Image):
    satisfied = False
    potentialTarget = (0, 255, 0, 255)  # start with green
    blacklist = []
    Fuck = 0

    while not satisfied:
        if Fuck == 10:
            random.seed()
            Fuck = 0

        if potentialTarget not in blacklist:
            if potentialTarget in image1.getdata() or potentialTarget in image2.getdata():
                blacklist.append(potentialTarget)
            else:
                satisfied = True
        else:
            Fuck += 1

        # randomize target
        potentialTarget = (random.randrange(0, 256), random.randrange(0, 256), random.randrange(0, 256), 255)

    return potentialTarget


def sendImage(outImg: Image.Image) -> bytes:
    img = BytesIO()
    outImg.save(img, "png")
    img.seek(0)
    return img.read()


# define methods
try:
    import deeppyer

    @app.get("/images/deepfry.png")
    async def deepfry(image_url: str):
        """Deepfries the image in the image URL."""
        image = await getImage(image_url)
        if isinstance(image, str):
            return {"message": image}  # error
        # noinspection PyTypeChecker
        deepImg = await deeppyer.deepfry(image, flares=False)
        deepImg = deepImg.convert('RGBA')  # i dunno, deepImg is an Image.py, but sendImage() wants Image
        return Response(content=sendImage(deepImg), media_type="application/png")
except Exception as e:
    print(f"ERROR UH OH OOPSIE WOOPSIES\n{e}")
        

@app.get("/images/catlamp.png")
async def catLamp(image_url: str):
    """Generates a Catlamp of the image in the image URL."""
    image = await getImage(image_url)
    if isinstance(image, str):
        return {"message": image}  # error
    overlay = catLampTemplate.copy()

    # find a color not in either image so we can use it for transparency in the final product
    alpha = findDualAlphaTarget(image, overlay)

    # convert the images to be equal in size and mode for compatibility
    image = centerSquare(image)

    if image.size > overlay.size:
        image.thumbnail(overlay.size)
        # set alpha color outside of the lamp (replace green with the designated alpha color)
        overlay = replaceColor(overlay, (0, 255, 0, 255), alpha)

        # cut hole in template (remove the magenta pixels)
        overlay = hippityHoppityThisColorIsDisappearity(overlay, (255, 0, 255, 255))
    else:
        # cut hole in template (remove the magenta pixels)
        overlay = hippityHoppityThisColorIsDisappearity(overlay, (255, 0, 255, 255))

        overlay.thumbnail(image.size, Image.NEAREST)  # this son of the bitches is the problem

        # replace transparent green with alpha
        overlay = replaceColor(overlay, (0, 255, 0, 255), alpha)

    image = image.convert(mode=overlay.mode)

    # combine catLamp with image
    outImg = Image.alpha_composite(image, overlay)

    # make the outside actually transparent
    outImg = hippityHoppityThisColorIsDisappearity(outImg, alpha)

    return Response(content=sendImage(outImg), media_type="application/png")


@app.get("/images/dio.png")
async def dio(image_url: str):
    """You expected the image in the image URL, but it was I, Dio!"""
    image = await getImage(image_url)
    if isinstance(image, str):
        return {"message": image}  # error

    overlay = dioTemplate.copy()

    # convert the images to be equal in size and mode for compatibility
    image = centerSquare(image)

    # cut hole in template (remove the magenta pixels)
    overlay = hippityHoppityThisColorIsDisappearity(overlay, (255, 0, 255, 255))

    if image.size > overlay.size:
        image.thumbnail(overlay.size)
    else:
        overlay.thumbnail(image.size)  # this son of the bitches is the problem

    image = image.convert(mode=overlay.mode)

    # combine dio with image
    outImg = Image.alpha_composite(image, overlay)

    return Response(content=sendImage(outImg), media_type="application/png")


@app.get("/images/flushed.png")
async def flushed(image_url: str):
    """The image in the image URL: 😳"""
    image = await getImage(image_url)
    if isinstance(image, str):
        return {"message": image}  # error

    overlay = flushedTemplate.copy()

    # convert the images to be equal in size and mode for compatibility
    image = centerSquare(image)

    # cut hole in template (remove the magenta pixels)
    overlay = hippityHoppityThisColorIsDisappearity(overlay, (255, 0, 255, 255))

    if image.size > overlay.size:
        image.thumbnail(overlay.size)
    else:
        overlay.thumbnail(image.size)  # this son of the bitches is the problem

    image = image.convert(mode=overlay.mode)

    # combine flushy with image
    outImg = Image.alpha_composite(image, overlay)

    return Response(content=sendImage(outImg), media_type="application/png")


@app.get("/images/joy.png")
async def joy(image_url: str):
    """😂😂😂 This command makes the image in the image URL a joke. 😂😂😂"""
    image = await getImage(image_url)
    if isinstance(image, str):
        return {"message": image}  # error

    overlay = joyTemplate.copy()

    # convert the images to be equal in size and mode for compatibility
    image = centerSquare(image)

    # cut hole in template (remove the magenta pixels)
    overlay = hippityHoppityThisColorIsDisappearity(overlay, (255, 0, 255, 255))

    if image.size > overlay.size:
        image.thumbnail(overlay.size)
    else:
        overlay.thumbnail(image.size)  # this son of the bitches is the problem

    image = image.convert(mode=overlay.mode)

    # combine dio with image
    outImg = Image.alpha_composite(image, overlay)

    return Response(content=sendImage(outImg), media_type="application/png")


@app.get("/images/invert.png")
async def invert(image_url: str):
    """Inverts the image in the image URL."""
    image = await getImage(image_url)
    if isinstance(image, str):
        return {"message": image}  # error

    if image.mode == "RGBA":
        alpha = findMonoAlphaTarget(image)

        alphaTemp = Image.new('RGB', (1, 1), alpha)
        alphaTemp = ImageOps.invert(alphaTemp)

        alphaInvert = alphaTemp.getdata()[0]  # find inverted alpha color

        image = Image.alpha_composite(Image.new('RGBA', (image.width, image.height), alpha), image)
    else:
        alphaInvert = None

    image = image.convert('RGB')  # i dunno, ImageOps wants an RGB
    image = ImageOps.invert(image)

    if alphaInvert:
        image = hippityHoppityThisColorIsDisappearity(image, alphaInvert)

    return Response(content=sendImage(image), media_type="application/png")


@app.get("/images/grayscale.png")
async def sadden(image_url: str):
    """😔"""
    image = await getImage(image_url)
    if isinstance(image, str):
        return {"message": image}  # error

    image = image.convert('RGB')  # i dunno, ImageOps wants an RGB
    image = ImageOps.grayscale(image)

    return Response(content=sendImage(image), media_type="application/png")


@app.get("/images/saturate.png")
async def saturate(image_url: str):
    """Saturates the image in the image URL."""
    image = await getImage(image_url)
    if isinstance(image, str):
        return {"message": image}  # error

    image = image.convert('RGB')  # i dunno, ImageEnhance might want an RGB
    enhancer = ImageEnhance.Contrast(image)
    image = enhancer.enhance(2)
    enhancer = ImageEnhance.Color(image)
    image = enhancer.enhance(3)

    return Response(content=sendImage(image), media_type="application/png")


@app.get("/images/mirror.png")
async def mirror(image_url: str):
    """Creates a mirrored image of the image in the image URL."""
    image = await getImage(image_url)
    if isinstance(image, str):
        return {"message": image}  # error

    outImg = image.transpose(method=Image.FLIP_LEFT_RIGHT)  # processing here

    return Response(content=sendImage(outImg), media_type="application/png")


@app.get("/images/flip.png")
async def flip(image_url: str):
    """Creates an upside-down copy of the image in the image URL."""
    image = await getImage(image_url)
    if isinstance(image, str):
        return {"message": image}  # error

    outImg = image.transpose(method=Image.FLIP_TOP_BOTTOM)  # processing here
    outImg = outImg.transpose(method=Image.FLIP_LEFT_RIGHT)  # top bottom makes it also flip on the x

    return Response(content=sendImage(outImg), media_type="application/png")


@app.get("/images/rotate.png")
async def rotate(image_url: str, degrees: float):
    """Rotates the image in the image URL clockwise by the specified number of degrees.
    (Algorithms contributed by Blue#1287 (494615059474153483))"""
    image = await getImage(image_url)
    if isinstance(image, str):
        return {"message": image}  # error

    image = image.convert('RGBA')  # make it so transparency generates instead of black

    angleOffset = degrees % 90  # this is what we'll use instead of input
    if angleOffset == 0:
        if degrees % 180 == 90:  # plot twist, the angle was also 90
            angleOffset = 90

    diagonal = math.sqrt(image.width ** 2 + image.height ** 2)  # finding the length of the rectangle's diagonal

    # this very well might return radians instead of degrees so we gotta convert
    b = math.degrees(math.atan(image.width / image.height))

    # finding angle of the diagonal of the rectangle to the uhhhh global 90 degree line uhhhhh
    a = 90 - (angleOffset + b)

    rotatedWidth = diagonal * math.cos(math.radians(a))  # this requires radians and not degrees

    b = math.degrees(math.atan(image.height / image.width))

    # finding angle of the diagonal of the rectangle to the uhhhh global 90 degree line uhhhhh
    a = 90 - (angleOffset + b)

    rotatedHeight = diagonal * math.cos(math.radians(a))  # this requires radians and not degrees

    if rotatedWidth > rotatedHeight:
        biggest = math.floor(rotatedWidth)
    else:
        biggest = math.floor(rotatedHeight)
    result = Image.new(image.mode, (biggest, biggest), (0, 0, 0, 0))  # big image to prevent cutting off stuff
    # paste the image on in a centered position
    result.paste(image, ((result.width // 2) - (image.width // 2), (result.height // 2) - image.height // 2))

    outImg = result.rotate(angle=-degrees)  # for some cursed reason, rotate() defaults to counterclockwise

    # do some centering math stuff to find the coordinates of the actual content
    outImg = outImg.crop((round(outImg.width / 2 - rotatedWidth / 2),
                          round(outImg.height / 2 - rotatedHeight / 2),
                          round(outImg.width / 2 + rotatedWidth / 2),
                          round(outImg.height / 2 + rotatedHeight / 2)))

    return Response(content=sendImage(outImg), media_type="application/png")


@app.get("/images/custom_overlay.png")
async def custom_overlay(image_url: str, overlay_url: str):
    """
    Generates an image with a custom overlay on top of it.
    A magenta color of (255, 0, 255, 255) represents areas where the main image will show through the overlay,
    and a green color of (0, 255, 0, 255) represents transparency in the final output.
    Shades of these colors caused by anti-aliasing in the source template will not be replaced.
    Transparency in the overlay image has not been tested due to developer laziness.
    """
    image = await getImage(image_url)
    if isinstance(image, str):
        return {"message": image}  # error
    overlay = await getImage(overlay_url)
    if isinstance(image, str):
        return {"message": image}  # error

    # find a color not in either image so we can use it for transparency in the final product
    alpha = findDualAlphaTarget(image, overlay)

    # convert the images to be equal in size and mode for compatibility
    image = centerSquare(image)
    overlay = centerSquare(overlay)

    if image.size > overlay.size:
        image.thumbnail(overlay.size)
        # set alpha color outside of the lamp (replace green with the designated alpha color)
        overlay = replaceColor(overlay, (0, 255, 0, 255), alpha)

        # cut hole in template (remove the magenta pixels)
        overlay = hippityHoppityThisColorIsDisappearity(overlay, (255, 0, 255, 255))
    else:
        # cut hole in template (remove the magenta pixels)
        overlay = hippityHoppityThisColorIsDisappearity(overlay, (255, 0, 255, 255))

        overlay.thumbnail(image.size, Image.NEAREST)  # this son of the bitches is the problem

        # replace transparent green with alpha
        overlay = replaceColor(overlay, (0, 255, 0, 255), alpha)

    image = image.convert(mode=overlay.mode)

    # combine overlay with image
    outImg = Image.alpha_composite(image, overlay)

    # make the outside actually transparent
    outImg = hippityHoppityThisColorIsDisappearity(outImg, alpha)

    return Response(content=sendImage(outImg), media_type="application/png")


# general template because again
# @app.get("/images/image.png")
# async def name(image_url: str):
#     """document here"""
#     image = await getImage(image_url)
#     if isinstance(image, str):
#         return {"message": image}  # error
#
#     outImg = None  # processing here
#     outImg = outImg.convert('RGBA')
#
#     return Response(content=sendImage(outImg), media_type="application/png")

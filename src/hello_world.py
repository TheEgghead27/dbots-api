from fastapi import FastAPI
from pydantic import BaseModel
from enum import Enum
from typing import Optional


class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"


class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None


app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World!"}


@app.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id}


@app.get("/users/me")
async def read_user_me():
    return {"user_id": "the current user"}


# you want to put the ones with priority further up in the script
@app.get("/users/{user_id}")
async def read_user(user_id: str):
    return {"user_id": user_id}


@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    if model_name == ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}
    elif model_name.value == "lenet":
        return {"model_name": model_name, "message": "LeCNN all the images"}
    else:
        return {"model_name": model_name, "message": "Have some residuals"}


items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]


@app.get("/items_db/")
async def read_db_item(skip: int = 0, limit: int = 10):
    return items_db[skip: skip + limit]


@app.get("/items_db/{item_id}")  # required params just have no Optional[] tag or default value
async def read_db_item(item_id: str, q: Optional[str] = None, short: bool = False):  # bool converter is very generous
    item = {"item_id": item_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update({"description": "This is an amazing item that has a long description"})
    return item


@app.post("/items/")
async def create_item(item: Item):
    return item

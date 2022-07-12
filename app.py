import time
from os import getenv
from random import randrange

from dotenv import load_dotenv
from fastapi import FastAPI
from pydantic import BaseModel
from pymongo.mongo_client import MongoClient

# load .env file
load_dotenv()
USERNAME = getenv("USERNAME")
PASSWORD = getenv("PASSWORD")

# create structure for payload
class Query(BaseModel):
    id: str
    title: str
    category: str
    link: str


# create mongodb client
client = MongoClient(
    f"mongodb+srv://{USERNAME}:{PASSWORD}@clusteruno.vsijxwy.mongodb.net/?retryWrites=true&w=majority"
)
database = client.techenclave
collection = database.buy_sell_trade_temp

# CRUD methods
def get(category: str | None = None):
    if category is not None:
        data = collection.find({"category": category})
    else:
        data = collection.find().sort("time", -1).limit(10)
    data = data.sort("_id", -1).limit(10)
    data = [{item: data[item] for item in data if item != "time"} for data in data]
    return {"isError": False, "message": "Success", "status": 200, "item": data}


def delete(id: str):
    if collection.find_one({"_id": id}) is not None:
        item = collection.find_one({"_id": id})
        collection.delete_one({"_id": id})
        return {"isError": False, "message": "Success", "statusCode": 200, "item": item}
    else:
        return {
            "isError": True,
            "message": "Not Found",
            "statusCode": 404,
        }


def post(_item: Query):
    if collection.find_one({"_id": _item.id}) is not None:
        return {
            "isError": True,
            "message": "Already Exists",
            "statusCode": 400,
        }
    else:
        collection.insert_one(
            {
                "_id": _item.id,
                "title": _item.title,
                "category": _item.category,
                "link": _item.link,
                "time": time.time(),
            }
        )
    return {
        "isError": False,
        "message": "Success",
        "statusCode": 200,
        "item": _item,
    }


def update(_item: Query):
    if collection.find_one({"_id": _item.id}) is not None:
        collection.update_one(
            {"_id": _item.id},
            {
                "$set": {
                    "title": _item.title,
                    "category": _item.category,
                    "link": _item.link,
                }
            },
        )
        return {
            "isError": False,
            "message": "Success",
            "statusCode": 200,
            "item": _item,
        }


app = FastAPI()

# create endpoints
@app.get("/api/buySellTrade/")
def get_item():
    return get()


@app.delete("/api/buySellTrade/")
def delete_item(id: str):
    return delete(id)


@app.post("/api/buySellTrade/")
def add_item(item: Query):
    return post(item)


@app.put("/api/buySellTrade/")
def update_item(item: Query):
    return update(item)

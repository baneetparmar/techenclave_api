from pymongo.mongo_client import MongoClient
from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, url_for
from flask.wrappers import Response
from os import getenv
import json

# load .env file
load_dotenv()
USERNAME = getenv("USERNAME")
PASSWORD = getenv("PASSWORD")


class MongoAPI:
    def __init__(self):
        self.client = MongoClient(
            f"mongodb+srv://{USERNAME}:{PASSWORD}@clusteruno.vsijxwy.mongodb.net/?retryWrites=true&w=majority"
        )
        database = self.client.techenclave
        self.collection = database.buy_sell_trade

    def read(self):
        return [
            {item: data[item] for item in data if item != "_id"}
            for data in self.collection.find().limit(10)
        ]


# create flask app
app = Flask(__name__)


@app.route("/api/", methods=["GET"])
def get_method():

    return Response(
        response=json.dumps(MongoAPI().read()),
        status=200,
        mimetype="application/json",
    )


@app.route("/api/category/", defaults={"category": "all"})
@app.route("/api/category/<category>", methods=["GET"])
def get_category_method(category):
    return Response(
        response=json.dumps(MongoAPI().read()),
        status=200,
        mimetype="application/json",
    )


if __name__ == "__main__":
    app.run(debug=True)

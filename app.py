import flask
import pymongo
from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, url_for
from os import getenv

# load .env file
load_dotenv()
USERNAME = getenv("USERNAME")
PASSWORD = getenv("PASSWORD")

# create flask app
app = Flask(__name__)


@app.route("/")
def hello():
    return "Hello, World!"


if __name__ == "__main__":
    app.run(debug=True)

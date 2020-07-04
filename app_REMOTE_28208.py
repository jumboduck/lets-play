import os
from flask import Flask, render_template, url_for, redirect, request, flash, session
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

app = Flask(__name__)

@app.route("/")
def index():

    return render_template("public/index.html")


if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
    port=os.environ.get('PORT'),
    debug=True)

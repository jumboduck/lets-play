import os

from flask import Flask, render_template, redirect, request, url_for, session
from flask_pymongo import PyMongo
from bson.objectid import ObjectId


app = Flask(__name__)

""" To be added. """
# app.config['MONGO_DBNAME'] = ...
# app.config['MONGO_URI'] = ...
# app.secret_key = ...

@app.route('/')
def index():
    return render_template('index.html')


if __name__ =='__main__':
    app.run(
        host=os.environ.get('IP'),
        port=os.environ.get('PORT'),
        debug=True)

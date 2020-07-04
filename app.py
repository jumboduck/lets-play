import os
from datetime import datetime
from flask import Flask, redirect, render_template, request, session, url_for, flash
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "randomstring123"
app.config['DEBUG'] = False

if app.config['DEBUG'] == True:
    from config import dbconfig
    app.config["MONGO_DBNAME"] = ''
    app.config["MONGO_URI"] = dbconfig()
else:
    app.config['MONGO_DBNAME'] = os.getenv('MONGO_DBNAME')
    app.config['MONGO_URI'] = os.getenv('MONGO_URI')

mongo = PyMongo(app)


# Home page with login form

@app.route('/')
def index():
    return render_template('login.html', register=mongo.db.register.find_one())


"""Register form action  method must be post.  Insert  new user in database using form on login page, then redirect user to allrecipeslist page.
"""


@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        register = mongo.db.register
        reg_id = register.insert_one(request.form.to_dict())
        # print(register)
        object_id = reg_id.inserted_id
        return redirect(url_for('', register_id=object_id))
    return render_template('register.html')


"""
Login page action. Method must be post - find the given password and username and  if it matches then
redirect to allrecipeslist but ifnot redirect to register and if password only incorrect flash message to show that  password is incorrect
"""
@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        login_user = mongo.db.register.find_one(
            {'username': request.form['username']})
        form = request.form
        if login_user:
            if(form["password"] == login_user["password"]):  # if password correct
                session['username'] = login_user["username"]
                return redirect(url_for('', register_id=login_user["_id"]))
            else:  # and if password is not correct
                flash("Incorrect password")
        else:  # if user does not exist
            flash("User does not exist")
            return redirect(url_for('register'))
    return render_template('login.html')

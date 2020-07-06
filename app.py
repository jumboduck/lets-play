import os
from flask import Flask, redirect, render_template, request, url_for
from flask import session, flash
from flask_pymongo import PyMongo
# from bson.objectid import ObjectId
# Password and datetime look optional (Pasha)
# from werkzeug.security import generate_password_hash, check_password_hash
# from datetime import datetime


if os.path.exists('env.py'):
    import env


app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'letsplay'
app.config['MONGO_URI'] = os.environ.get('MONGO_URI')
app.secret_key = os.environ.get('SECRET')

"""
This piece of code is from some other place and at the moment it doesn't work.
That is why I kept it but commented it out. (Pasha)

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
"""

mongo = PyMongo(app)


# Home page with login form

@app.route('/')
def index():
    return render_template('public/index.html', session=session)
    # return render_template('
    # /public/login.html', register=mongo.db.register.find_one())


"""
Login page action. Method must be post.
Find the given password and username and  if it matches then
redirect to allrecipeslist but ifnot redirect to register and
if password only incorrect then
flash message to show that  password is incorrect
"""


@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        form = request.form
        login_user = mongo.db.users.find_one(
            {'username': request.form['username']})
        if login_user:
            if(form['password'] == login_user['password']):
                session['username'] = login_user['username']
                session['status'] = login_user['status']
                return redirect(url_for('home'))
                # return redirect(url_for(
                # '', register_id=login_user["_id"]))
            else:  # and if password is not correct
                flash("Incorrect password")
        else:  # if user does not exist
            flash("User does not exist")
            return redirect(url_for('register'))
    return render_template('/public/login.html', session=session)


@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('status', None)
    return redirect(url_for('index'))


@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        form = request.form
        # Get user's data from form.
        username = form['username']
        password = form['password']

        # If username is valid then redirect to sign in.
        users = mongo.db.users
        if users.count_documents({'username': username}) == 0:
            users.insert_one(
                {'username': username, 'password': password, 'status': 'user'})
            session['username'] = username
            session['status'] = 'user'
            return redirect(url_for('home'))
        else:
            flash("Not valid username or password. Try again, please.")

            """ This piece of code is from the old version.
            I kept it just in case we want to use it. /Pasha
            # reg_id = users.insert_one(request.form.to_dict())
            # object_id = reg_id.inserted_id
            # return redirect(url_for('', register_id=object_id))
            """
    return render_template('public/register.html', session=session)


@app.route('/home')
def home():
    return render_template('public/home.html', session=session)


@app.route('/activities_proposed')
def activities_proposed():
    return render_template('public/activities_proposed.html', session=session)


@app.route('/activities_done')
def activities_done():
    return render_template('public/activities_done.html', session=session)


@app.route('/games')
def games():
    return render_template('public/games.html', session=session)


"""
This piece of code is just to test a connect to MongoDB.
I commented it out but kept it for possible use in future. (Pasha)

@app.route('/')
def index():
    db_content = mongodb.db.users.find()
    print("db_content: ", db_content)
    n_of_users = mongodb.db.users.count_documents({})
    print("N of users: ", n_of_users)
    the_user = mongodb.db.users.find_one({"name": "Test User"})
    print("the_user: ", the_user)
    for key in the_user:
        print("key: ", key)
    return render_template('public/index.html', n_of_users=n_of_users)
"""


if __name__ == '__main__':
    app.run(
        host=os.environ.get('IP'),
        port=os.environ.get('PORT'),
        debug=True)

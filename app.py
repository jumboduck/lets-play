import os

from flask import Flask, render_template, redirect, request, url_for, session
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

if os.path.exists('env.py'):
    import env


app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'letsplay'
app.config['MONGO_URI'] = os.environ.get('MONGO_URI')
app.secret_key = os.environ.get('SECRET')

mongodb = PyMongo(app)


@app.route('/')
def index():
    db_content = mongodb.db.users.find()
    print("db_content: ", db_content)
    """
    # Failed attempt 1:
    n_of_users = mongodb.db.users.count_documents({})
    print("N of users: ", n_of_users)
    #Failed attempt 2:
    the_user = mongodb.db.users.find_one({"name": "Test User"})
    print("the_user: ", the_user)
    """
    return render_template('index.html')


if __name__ =='__main__':
    app.run(
        host=os.environ.get('IP'),
        port=os.environ.get('PORT'),
        debug=True)

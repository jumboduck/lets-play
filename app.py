import os
from flask import Flask, redirect, render_template, request, url_for
from flask import session, flash
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from passlib.hash import pbkdf2_sha256
import cloudinary
import cloudinary.uploader
import cloudinary.api
from datetime import datetime


if os.path.exists('env.py'):
    import env


app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'letsplay'
app.config['MONGO_URI'] = os.environ.get('MONGO_URI')
app.secret_key = os.environ.get('SECRET')
app.config['CLOUDINARY_URL'] = os.environ.get('CLOUDINARY_URL')

mongo = PyMongo(app)


# Home page with login form

@app.route('/')
def index():
    return render_template('public/index.html', session=session)


"""
Login page action. Method must be post.
Find the given password and username and  if it matches then
it logs the user in according to their account status of user or admin.
Flash messages will show incorrect username/password combination to add an
increased level of security to the user and not give clues to a potential hacker
of what was incorrect. / Andy
"""


@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        form = request.form
        login_user = mongo.db.users.find_one(
            {'username': request.form['username']})
        if login_user:
            if pbkdf2_sha256.verify(form["password"], login_user['password']):
                session['username'] = login_user['username']
                session['status'] = login_user['status']
                if session['status'] == 'admin':
                    return redirect(url_for('moderator'))
                else:
                    return redirect(url_for('home'))
            else:  # and if password is not correct
                flash("Incorrect username/password combination")
        else:  # if user does not exist
            flash("Incorrect username/password combination")
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
        password_confirm = form['confirm-password']

        # If username is valid then redirect to sign in.
        users = mongo.db.users
        if users.count_documents({'username': username}) == 0 and password == password_confirm:
            users.insert_one(
                {'username': username, 'password': pbkdf2_sha256.hash(password), 'status': 'user', 'accomplished': []})
            session['username'] = username
            session['status'] = 'user'
            return redirect(url_for('home'))
        else:
            flash("Not valid username or password. Try again, please.")

    return render_template('public/register.html', session=session)


@app.route('/home')
def home():
    return render_template('public/home.html', session=session)

"""
Display only activities that have not been accomplished by the user yet.
"""

@app.route('/activities')
def activities():
    activities = mongo.db.activities.find()
    user = mongo.db.users.find_one({'username': session['username']})
    available_activities = []
    for activity in activities:
        if not activity["_id"] in user["accomplished"]:
            available_activities.append(activity)
    return render_template('public/activities.html', session=session, activities=available_activities)


"""
When an activity is marked as completed, the 'accomplished' array in the user document of the
database is updated to include the id of the accomplished task.
If the form contains a field image, and it is not empty, the image is uploaded to cloudinary
and its information inserted in the "images" collection.
"""

@app.route('/complete/<activity_id>', methods = ["POST", "GET"])
def complete(activity_id):
    users = mongo.db.users
    images = mongo.db.images
    # Check if image input exists, and if a file has been selected
    if 'image' in request.files and request.files['image']:
        # Retrieve the image and send it to cloudinary
        image = request.files['image']
        uploaded_image = cloudinary.uploader.upload(image, width = 800, quality = 'auto')
        image_url = uploaded_image.get('secure_url')
        # Update "images" collection with new image
        images.insert({
            'image_url': image_url,
            'user': session['username'],
            'reactions': {'thumbsup': 0, 'heart': 0, 'laugh': 0, 'happy': 0},
            'timestamp': datetime.now(),
            'approved': False
        })
    # Update user document with accomplished activity
    users.update_one(
        {'username': session['username']},
        {'$push': {
            'accomplished': ObjectId(activity_id)
            }
        }
    )
    flash('Congratulations on completing this activity!')
    return redirect(url_for('activities'))


"""
Reset activities for logged in user
"""

@app.route('/reset_activities')
def reset_activities():
    users = mongo.db.users
    users.update({
        'username': session['username']
    },{
        '$set':{
            "accomplished": []
        }
    })
    flash("Well done, let's start again!")
    return redirect(url_for('activities'))


@app.route('/images', methods=["GET", "POST"])
def images():
    images = mongo.db.images.find({'approved': True}).sort([("_id", -1)])
    return render_template('public/images.html', images = images)


"""
if user_name not in images["liked_by"]:
        images.update(
            {'_id': ObjectId(image_id)},
            {
                "$inc": {"likes": 1},
                "$push" : {"liked_by": user_name}
        })
    else:
        images.update(
            {'_id': ObjectId(image_id)},
            {
                "$inc": {"likes": -1},
                "$pull" : {"liked_by": user_name}
        })
"""

@app.route('/update_reaction/<image_id>/<reaction>')
def update_reaction(image_id, reaction):
    images = mongo.db.images
    if session['username'] not in images[reaction + "_by"]:
        images.update_one(
            {'_id': ObjectId(image_id)},
            {
                '$inc': {"reactions." + reaction : 1},
                "$pull" : {reaction + "_by": session['username']}
            })
    else:
        images.update(
            {'_id': ObjectId(image_id)},
            {
                "$inc": {"reactions." + reaction : -1},
                "$pull" : {reaction + "_by": session['username']}
        })
    return redirect(url_for('images'))


# Admin Views


@app.route('/moderator')
def moderator():
    images = mongo.db.images.find({'approved': False})
    count_images = mongo.db.images.count_documents({'approved': False})
    return render_template(
        'admin/moderator.html', session=session, images=images, count=count_images)


@app.route('/approve/<image_id>')
def approve(image_id):
    mongo.db.images.update_one({'_id': ObjectId(image_id)}, {'$set': {'approved': True}})
    return redirect(url_for('moderator'))


@app.route('/reject/<image_id>')
def reject(image_id):
    mongo.db.images.delete_one({'_id': ObjectId(image_id)})
    return redirect(url_for('moderator'))


@app.route('/activity_manager', methods=["POST", "GET"])
def manage_activities():

    """
    The below is used within the Moderator Site to upload new activities 
    for the users so that they appear in the activities page.
    As the requirements field in the form is not required, it checks if it is blank
    and if it is, then it will not upload it to the DB. /Andy
    """

    if request.method == "POST":
        req = request.form
        new_task = {
            "name" : req["activity_name"],
            "description" : req["activity_description"],
            "has_photo" : req.getlist("activity_photo")
        }
                
        if req["activity_requirements"] != "":
            new_task["requirements"] = req["activity_requirements"]
        
        
        mongo.db.activities.insert_one(new_task)
        return redirect(request.referrer)

    return render_template('admin/activity_manager.html', session=session)

# Below handles any 404 errors when a user searches for a non-existant page. / Andy

@app.errorhandler(404)
def page_not_found(e):
    return render_template("public/404.html"), 404


if __name__ == '__main__':
    app.run(
        host=os.environ.get('IP'),
        port=os.environ.get('PORT'),
        debug=True)

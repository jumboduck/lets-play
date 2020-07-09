# [Lets-Play](https://letsplay-hackathon2020.herokuapp.com/login)

This project was put together during the July 2020 code institute hackathon.

We were originally a team of 6 people; 5 of us were at various stages in the code institute online course, 1 person had already finished the course. After 2 days that team was reduced to 4 people. The 6 people initially working on the project were: Andy Osborne, Simon Castagna, Leticia Leon, Pavel Zelenin, Deborah Thompson and Daryl. After the initial call and some initial research on our theme done by Daryl and Leticia, Andy, Simon, Pavel and Deborah continued to work on the project from Sunday 5th July 2020 to Thursday 9th July 2020.

Our brief was to provide an interactive site for children in lockdown. This was taken from a brief based on the theme below. The theme of the Hackathon was Thriving in the New Normal, and teams were asked to focus on coming up with solutions on how we can work, play and connect more effectively in a post-pandemic world. We focused on creating solutions for children aged 6 to 11 to interact with each other. Initially we decided to create a site where children could interact with each other through a range of suggested activities. Parents would create a login and password for the site and then work with their children on a list of activities. Children could complete these independently if they wished. At the end of the activity the parent could tick off the completed activity and upload it to the site. The upload would be supervised by the parent but would also be subject to moderation to ensure that only appropriate images and text were uploaded.

The app was deployed to heroku and can be accessed by clicking on the title above.

## UX

![Responsive Devices](/readme-files/responsive-screens.png)

Wireframes were created for the project each day. Initially we started with an ambitious design to include a quiz however we needed to downsize this as some of our team were unable to complete the hackathon and we wanted to focus on getting the design up and running as best as we could.

The site was made responsive with bootstrap for ease of use across all device sizes.

### User stories

User 1: Child aged 6 to 9 years old, bored at home, little online school work from school, parents trying to work at home and keep child entertained, looking up ideas for child to do and once an idea is found supervising the child. All very time consuming and distracting for parent at times.

User 2: Older child aged 10 to 11 years old. Fed up with work from school and working online in collaborative classrooms - sometimes logs into classroom then goes off and plays video games and so on. Feels that they are ok but parents feel that child's education is suffering. Parent would like to find something online that child can do that add to their education and sense of achievement.

User 3: Parent of child aged 6 to 11. Parent is fed up with kids being unoccupied,bored, doing little school work, etc so is looking for activities which engage and entertain them. Parent would also like a way to keep track of the activities their children are doing.

Wireframes were an integral part of the development process. We designed these at the start of the project but as time went by they needed
several revisions [wireframes](https://github.com/jumboduck/lets-play/blob/master/readme-files/letsplay-wireframes.pdf) to see the final versions of my wireframes.

## Features

The features which were implemented successfully are shown below:

1. Each user has a unique username and password.  
   Achieved through use of login page. The password is hashed and salted. Users are stored in a collection in the database- they are authenticated against this when they log in.

2. User logs in or registers on landing page then is directed to activities page. User is directed to activities page as soon as they are logged in.

3. User is then given list of generated activities to do which appears in their "Activities For You" page.

4. User can choose which activity to do and then do that activity. Some activities allow for the user to upload a picture of their project. User clicks on activity to get more details of activity and is then given instructions to do that activity, and hopefully goes away and does it.

5. Uploaded images go to moderator area where they are reviewed and if ok, approved to go onto the site. Users can upload images to moderator area. Security was added so that only moderator can access this area. See security notes section below.

6. Images uploaded by users are displayed on the images page. If a user is logged in, they have the ability to react to it by choosing between four reactions represented by emojis.

7. User doing activities can then do another activity from the list, ticking off the activities they have done so far and uploading images and description as described above. Further images and descriptions will be subject to moderation. User can choose from remaining list of activities displayed and repeat process.

8. Once user has come to the end of the activity list they can hit the reset button to restart the list of activities. User is able to reset activity list so they can revisit activities and maybe do these better.

9. In the moderator section, the moderator is able to upload further activities to the database which is then pushed out to the list of activities that each user has.

## Security features

From a user security standpoint, we implemented password hashing and salting so that no-one else can see or know a users password apart from the person who created. In addition to this, the flash messages will say "Incorrect username/password combination" to not help a "hacker" know which one is incorrect.

Additionally conditional logic was added to the moderator pages so that if the users status is not "admin" they cannot see the information on the page. Before this update, if anyone went to the URL for the moderator pages, they would be able to see it and interact with it.

## Development process of the project

1. We created a master repository for the project on GitHub. The repository contained a skeleton format for the project: static folder, templates folder, Procfile, readme and app.py files were included.

2. All members of the team forked the repo then cloned it locally. All members of the team were then able to create their own branches and issue pull requests for their code.

3. Next thing was to create a base template html file to control the overall look of the site.

4. In the app.py file all modules that were needed were imported and a secret key was set. Debug to True so that an error log would be produced for any errors encountered when running the project.

5. The Procfile and requirements.txt files were regularly updated.

6. An admin user was created for the moderator, noting this format as it would later be needed to put in the config.py file `mongodb://<dbuser>:<dbpassword>@XXXXXX.mlab.com:XXXXX/lets_play`

7. Activities were created and entered into the activities collection.

8. A cloudinary account was created to upload images to and its API url added to the env.py file

9. We connected the app.py file to the database. We entered the environment details in to the env.py file and then put this in gitignore. The Procfile and requirements.txt files were updated.

10. Lastly we checked that the entire app worked before doing a final push to heroku, making sure that the environment variables were correctly input into the heroku dashboard for the app and that debug was set to false so that the app was secure.

11. Finally we created a favicon for the app.

## Deployment

The following section describes the process we undertook to deploy this project to Heroku. Work done on pushing to heroku started by Simon, checked by Andy and Pasha.

-   We ensured that all required technologies were installed locally, as per the requirements.txt file.
-   We ensured that we had created a Procfile indicating that the app was based on python.
-   We used the bash terminal to log in to Heroku, using 'heroku login' command. Input Heroku login details.
-   We then created a new Heroku app, using `heroku apps:create appname` command from the terminal.
-   We pushed my project to Heroku, using `push -u heroku master` command from the terminal.
-   Then we created scale, using `heroku ps:scale web=1` command.
-   We then logged into Heroku and selected newly created app.
-   We then selected settings. Select 'Reveal Config'. I then added IP 0.0.0.0 and PORT 5000.
-   Then from the 'More' menu on the top right, we selected 'Restart all dynos'.
-   To view the app, in settings we selected the Domain URL, NOT Git URL to view your hosted application.
-   We checked that the app was now deployed via Heroku
-   The application on heroku was connected to Simon's repository on Github to ensure it would be updated with each of the team's merges

## Features which could be implemented in the future

1. Authenticated user login. Users identities could be checked using two factor authentication. This could be implemented in django or another python framework.

2. Statistics on user ratings for each activity. A ratings collection could be used for this. The ratings could be implemented using a number of technologies including crossfilter and matlab.

3. The ability for users to suggest new activities, which would have to be approved by the moderator.

4. The creation of a profile page for each user, along with badges won for completing activities.

## Technologies Used

[HTML](https://developer.mozilla.org/en-US/docs/Learn/HTML)
Hypertext markup language is used to create the structure of web pages. It consists of tags which tell the browser
how to set out text and images on the page. Hypertext is the method by which you move around on the web, markups are the tags
which set out the structure of the webpage, thus HTML is a language for web creation with its own structure and syntax. The data in the tags is read by the web browser enabling you to create any web page you like. In this project my templates are all written in HTML. The base template sets out the way in which
the website should look and information from this is used in each of the other templates.

[CSS](https://developer.mozilla.org/en-US/docs/Learn/CSS/Introduction_to_CSS) stands for Cascading Style sheets which is a type of style language which sets out how the webpage should be styled. It allows the user to style the webpage in a particular way, making the UX richer and more meaningful for the user.

[Flask](http://flask.pocoo.org/)
Flask is a microframework written in python. Flask is therefore the "glue" that holds an application together. Different types of file can co-exist in a flask application, with the base template holding the HTML base code for other templates. In addition flask provides security throught the wekzeug add in and the jinja templating language can also be used for markup on web pages.

[Jinja2](http://jinja.pocoo.org/docs/2.10/) is a templating language which is used for rendering data in html templates and is used for communication between the front end and back end of an app.

[jquery](https://jquery.com/) is used to simplify DOM manipulation. Jquery is a javascript library that is used to provide interactivity
on websites. The \$ sign signals to the browser that jquery is being used.

[python](https://www.python.org/)
We used Python version 3.7 to run our app. Python is a high level programming language used for apps in many frameworks such as
flask, pyramid and django. Python supports many programming paradigms and is object orientated and has a comprehensive set of libraries.
Python is managed by a non profit organsation the Python software foundation.

[mongodb](https://mlab.com/) was used mongodb for the database. Through pymongo (a module in python) we were able to connect my database to my flask app through the use of appropriate environment variables. Mongodb is a document database that provides the user with the facility to create, read, update and delete documents in a database. Mongodb documents are stored in collections in json or bson format and this makes it easy to work with in Python and other programming languages.

[Heroku](https://en.wikipedia.org/wiki/Heroku) is a cloud platform that allows a developer to build, deliver, scale and monitor apps. Heroku makes the experience of
deploying an app relatively straightforward.

[Chrome Developer Tools](https://developers.google.com/web/tools/chrome-devtools/) were used to work on my code. Chrome dev tools are a set of tools designed to give the developer tools
to amend code in a testing environment in order to enhance the UX and functionality experience. I was also able to test the responsiveness of my app using these tools.

[Cloudinary](https://cloudinary.com/) is an image hosting site with a very rich API, allowing to upload and transform images.

Alongside jQuery, AJAX was used for users to react to images and for these reactions to display without the page reloading entirely.

## Testing

Testing was carried out by human beings. Details of testing done by testers on a page by page basis is shown below.

### User Section Testing


### Admin Section Testing

We logged in as the admin/moderator for the website and tested that when a user uploads an image to the website that it appears in the list to be checked. In addition to this, we thoroughly tested that when an image has been approved that it appears in the images page and that when an image is rejected, it does not.

We tested the Activity Manager page to ensure that when we create a task that it gets pushed through to the current list of activities for the users. No bugs were found

## Interesting bugs or problems discovered during testing

## Credits

### Content

-   To speed up process of development, the theme [One Page Wonder](https://startbootstrap.com/previews/one-page-wonder/) by startbootstrap was used

-   All the photos used on the website were taken from [Pexels](https://www.pexels.com/), which is a stock image library.

- The logo was created using [Logomkr](https://logomakr.com/).

Media

Acknowledgements

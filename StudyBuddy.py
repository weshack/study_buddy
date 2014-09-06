from flask import Flask, url_for, redirect, session, render_template, request
from flask_login import (UserMixin, login_required, login_user, logout_user,
                         current_user)
from flask_googlelogin import GoogleLogin
import json
from jinja2 import Template
# from flask.ext.pymongo import PyMongo
from pymongo import MongoClient
import departmentArray

client = MongoClient()

db = client.sbdb
users = db.users


app = Flask(__name__, static_url_path='')

app.config.update(
    SECRET_KEY='Tieng3us3Xie5meiyae6iKKHVUIUDF',
    GOOGLE_LOGIN_CLIENT_ID='1002179078501-mdq5hvm940d0hbuhqltr0o1qhsr7sduc.apps.googleusercontent.com',
    GOOGLE_LOGIN_CLIENT_SECRET='O1kpQ8Is9s2pD3eOpxRfh-7x',
    GOOGLE_LOGIN_REDIRECT_URI='http://127.0.0.1:5000/oauth2callback'
)

googlelogin = GoogleLogin(app)

# DATABASE, TODO: Separate out.

# class User(db.Document):
#     name = db.StringField(max_length=255)
#     userID = db.StringField(max_length=255)


@app.route("/dbtest1")
def test1():
    test = db.users.insert({"name":"Aaron Plave","userID":"1234"})
    return "TEST"
    
@app.route("/dbtest2")
def test2():
    a = db.users.find_one()
    print a 
    b = a['name'] + " " + a['userID']
    return b

users = {}

@googlelogin.user_loader
def get_user(userid):
    return users.get(userid)

class User(UserMixin):
    def __init__(self, userinfo):
        self.id = userinfo['id']
        self.name = userinfo['name']

@app.route("/home")
@login_required
def root():
    return app.send_static_file('html/index.html')

# Make a search for a class, and return a json object.
@app.route('/find')
def search():
    search_keyword = request.args.get('search_keyword')
    
    # Query database with search_keyword

    # db.group_sessions.find
    search_results = [1,2,3] #StudySessions.objects(class_name=search_keyword)


    # Return template with object full of data
    return render_template('search_results.html', results=search_results)


@app.route('/')
def index():
    return render_template('login.html',login_link=googlelogin.login_url(approval_prompt='force',scopes=["email"]))


class User(UserMixin):
    def __init__(self,userinfo):
        self.id = userinfo['id']
        self.name = userinfo['name']
        print "\nUSERINFO:",userinfo,"\n"
        self.email = userinfo['email']

# Google OAuth
@app.route('/oauth2callback')
@googlelogin.oauth2callback
def login(token, userinfo, **params):
    user = users[userinfo['id']] = User(userinfo)
    # deny access to anyone without an @wesleyan.edu email address
    if not "@wesleyan.edu" in user.email:
        # redirect to same page, display error
        return render_template('login.html',results="meow, you have been denied.")
    login_user(user)
    session['token'] = json.dumps(token)
    return redirect(params.get('next', url_for('.login_redirect')))


@app.route('/login_redirect')
@login_required
def login_redirect():
    # if success, add user to db if not exists
    #check if user exists
    if not db.users.find_one({"userID": current_user.id}):
        print "FOUND THE USER", current_user.id
        db.users.insert({"name":current_user.name,"userID":current_user.id,"email":current_user.email})
    else:
        print "HAVE USER",current_user.id
    return redirect('/home')


@app.route('/logout')
def logout():
    logout_user()
    session.clear()
    return redirect('/')

@app.route('/checkin')
def checkin():
    return 'hello'

@app.route('/create')
def create():
    return render_template('create.html');

@app.route('/lucky')
def lucky():
    return 'feeling lucky picks random room'


@app.route('/new',methods=['POST'])
def new():
    # get the data from the request
    department = request.args.get('department')
    course = request.args.get('course')
    location = request.args.get('location')
    time = request.args.get('time')
    attendees = request.args.get('attendees')

    # validate data
    errors = []
    if not departmentArray.validDept(department):
        err1 = "DEPARTMENT DOES NOT EXIST", department
        errors.append(err1)
    if not len(course) == 3:
        err2 = "BAD COURSE NUMBER", course
        errors.append(err2)
    if len(location) > 255:
        err3 = "Location too long, please limit to 255 chars or less", location
        errs.append(err3)

    # convert/validate time
    time = 123456543

    #add more future validation here
    if errors:
        print "ERRORS:"
        for i in errors: print i
        return render_template('create.html',results=errors)

    # get user from session
    print session
    #user = session.get_user....?
    user = "Aaron Plave"

    # create group session object
    # group_session = {
        # "ownerID":
    # }

    # insert info into database 
    if not db.group_sessions.find_one({"userID": current_user.id}):
        print "FOUND THE USER", current_user.id
        db.users.insert({"name":current_user.name,"userID":current_user.id,"email":current_user.email})
    else:
        print "HAVE USER",current_user.id

    # TODO: confirm event created in DB
    return app.send_static_file('html/index.html')


if __name__ == "__main__":
	app.run(debug=True)

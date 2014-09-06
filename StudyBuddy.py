from flask import Flask, url_for, redirect, session, render_template, request
from flask_login import (UserMixin, login_required, login_user, logout_user,
                         current_user)
from flask_googlelogin import GoogleLogin
import json
from jinja2 import Template
# from flask.ext.pymongo import PyMongo
from pymongo import MongoClient
import departmentArray

##
# Constants for mongodb keys
##
DEPARTMENT_KEY = "department"
COURSE_NUMBER_KEY = "course_no"
LOCATION_KEY = "location"
TIME_KEY = "time"
ATTENDEES_KEY = "attendees"
COURSE_NOTES_KEY = "course_notes"
CONTACT_KEY = "contact"
DESCRIPTION_KEY = "description"
OWNER_KEY = "owner"
OWNER_ID_KEY = "owner_id"

client = MongoClient()

db = client.sbdb


app = Flask(__name__, static_url_path='')

app.config.update(
    SECRET_KEY='Tieng3us3Xie5meiyae6iKKHVUIUDF',
    GOOGLE_LOGIN_CLIENT_ID='1002179078501-mdq5hvm940d0hbuhqltr0o1qhsr7sduc.apps.googleusercontent.com',
    GOOGLE_LOGIN_CLIENT_SECRET='O1kpQ8Is9s2pD3eOpxRfh-7x',
    GOOGLE_LOGIN_REDIRECT_URI='http://127.0.0.1:5000/oauth2callback',
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
def root():
    return app.send_static_file('html/index.html')

def return_db_results(results,user,userID):
    return render_template('search_results',count=results.count(),results=list(results),user=user,userID=userID)

# Search for a class. Dept is fixed but number is free, must be 3 num code
@app.route('/find')
def search():
    user = "John Doe"
    userID = "12345"
    # IMPORTANT, make sure that the dept keyword is ALWAYS short form,
    # so on front end map the dept keyword (if long) to short form.
    dept_keyword = request.args.get('dept_keyword')

    # Verify dept is valid
    if not departmentArray.validDept(dept_keyword):
        err = "Invalid department, please enter a valid department."
        return render_template('search_results',error_message=err)
    
    course_keyword = request.args.get('course_keyword')

    # case where no course number is specified
    if not course_keyword:
        #just pull all the courses under that dept
        results0 = db.group_sessions.find({DEPARTMENT_KEY:dept_keyword}).sort(TIME_KEY)
        if results0.count() > 0:
            print "Got results0"
            return return_db_results(results0,user,userID)

    # TODO: verify course number is safe?
    # Query database with search_keyword. Dept number + 3 num code. If fails,
    results1 = db.group_sessions.find({DEPARTMENT_KEY:dept_keyword,COURSE_NUMBER_KEY:course_keyword}).sort(TIME_KEY)
    if results1.count() > 0:
        print "Got results1, yippee!"
        return return_db_results(results1,user,userID)

    # try same thing with the first two numbers (if there are 2-3 numbers) to get closest matches. If nothing,
    twoOrThree = False
    if len(course_keyword) == 2:
        short_course_keyword = course_keyword
        twoOrThree = True
    if len(course_keyword) == 3:
        short_course_keyword = course_keyword[0:1]
        twoOrThree = True
    if twoOrThree:
        results2 = db.group_sessions.find({DEPARTMENT_KEY:dept_keyword,COURSE_NUMBER_KEY:short_course_keyword}).sort(TIME_KEY)
        if results2.count() > 0:
            print "Got results2, yippee!"
            return return_db_results(results2,user,userID)
            
    # find all courses with that 3 number code. 

    # db.group_sessions.find
    search_results = [{CONTACT_KEY:"8607596671",LOCATION_KEY:"exley",COURSE_NUMBER_KEY:"303",TIME_KEY:"4:20pm",DESCRIPTION_KEY:"Assignment 2",ATTENDEES_KEY:[["Aaron","azroz"],["Denise","nishii"]],OWNER_KEY:"Hora",COURSE_NOTES_KEY:"class notes"}] #StudySessions.objects(class_name=search_keyword)
    count=5
    user="John Doe"
    userid="jd"
    boolean=False
    # Return template with object full of data
    return render_template('search_results.html', results=search_results, count=count,user=user,id=userid,boolean=boolean)


@app.route('/')
def index():
    return render_template('login.html', 
        login_link=googlelogin.login_url(approval_prompt='force',scopes=["email"]))



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
    if db.users.find_one({"userID": current_user.id}):
        print "HAVE USER",current_user.id
    else:
        print "FOUND THE USER", current_user.id
        db.users.insert({"name":current_user.name,"userID":current_user.id,"email":current_user.email})
    return redirect('/home')


@app.route('/logout')
def logout():
    logout_user()
    session.clear()
    return redirect('/')

#accessing the departmentArray information for autofilling department form
@app.route('/departments')
def departments():
    print "searching for departments.."
    return json.dumps(departmentArray.depts)

@app.route('/create')
def create():
    return render_template('create.html');

@app.route('/lucky')
def lucky():
    return 'feeling lucky picks random room'

@app.route('/new',methods=['POST'])
def new():
    # get the data from the request
    dept = request.form.get('department')
    course = request.form.get('course')
    location = request.form.get('location')
    time = request.form.get('time')
    attendees = request.form.get('attendees')

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
    ownerID = "123456"

    # create group session object
    group_session = {
        OWNER_ID_KEY : ownerID,
        DEPARTMENT_KEY : dept,
        COURSE_NUMBER_KEY : course,
        LOCATION_KEY : location,
        TIME_KEY : time,
        ATTENDEES_KEY : attendees
    }

    print "GROUP SESSION:",group_session
    # insert info into database 
    if db.group_sessions.find_one():
        errX = "Group already exists",group_session
        print errX
        # TODO: confirm event created in DB
        return render_template('create.html',results=errX)
    else:
        print "Unique group"
        db.group_sessions.insert(group_session)
        return app.send_static_file('html/index.html')

##
# Responds to a url of the form: 
#   /edit?department=<department>&course_no=<course_no>&location=<location>&time=<time>&attendees=<attendees>&course_notes=<course_notes>&group_id=<group_id>
#   
#   department : string
#   course_no : string
#   location : string
#   time : string
#   attendees : list of strings
#   course_notes : string
#   group_id : string
##
@app.route('/edit',methods=['POST'])
def edit():
    department = request.args.get('department')
    course_no = request.args.get('course_no')
    location = request.args.get('location')
    time = request.args.get('time')
    attendees = request.args.get('attendees')
    course_notes = request.args.get('course_notes')
    group_id = request.args.get('group_id')

    coll = db.group_sessions
    new_data = {DEPARTMENT_KEY    : department,
                COURSE_NUMBER_KEY : course_no,
                LOCATION_KEY      : location,
                TIME_KEY          : time,
                ATTENDEES_KEY     : attendees,
                COURSE_NOTES_KEY  : course_notes}

    # verify that user owns the group before updating database.
    coll.update({'_id' : group_id}, $set: new_data)

    # Show the updated results page.

@app.route('/delete',methods=['POST'])
def delete():
    # TODO: verify that user in session owns the group session to be deleted
    pass

@app.route('/join',methods=['POST'])
def join():
    # TODO: Verify user is not already in the group session
    # TODO: Add user to the group in the DB

    # Report success or failure so the UI can react
    pass

if __name__ == "__main__":
	app.run(debug=True)

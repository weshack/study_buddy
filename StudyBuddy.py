from flask import Flask, url_for, redirect, session, render_template, request
from flask_login import (UserMixin, login_required, login_user, logout_user,
                         current_user)
from flask_googlelogin import GoogleLogin
import json
from jinja2 import Template
# from flask.ext.pymongo import PyMongo
from pymongo import MongoClient
import departmentArray
import random
import time
from dateutil.parser import parse

##
# Constants for mongodb keys
##

DEPARTMENT_KEY = "department"
COURSE_NUMBER_KEY = "courseNumber"
LOCATION_KEY = "location"
TIME_KEY = "time"
COURSE_NOTES_KEY = "course_notes"
CONTACT_KEY = "contact"
DESCRIPTION_KEY = "description"
OWNER_NAME_KEY = "owner"
OWNER_ID_KEY = "owner_id"
ATTENDEES_KEY = "attendees"

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



# Search for a class. Dept is fixed but number is free, must be 3 num code
@app.route('/find')
def search():
    user = "John Doe"
    userID = "12345"

    # IMPORTANT, make sure that the dept keyword is ALWAYS short form,
    # so on front end map the dept keyword (if long) to short form.
    dept_keyword = request.args.get('search_keyword')
    if not dept_keyword:
        print "NO DEPT KEYWORD"
        grps = db.group_sessions.find()
        grps=cursortolst(grps)
        isAttendee=attendee(grps,user)

        return return_db_results(grps,user,userID,isAttendee)
    # Verify dept is valid
    
    skip_validation = True
    if not skip_validation:
        if not departmentArray.validDept(dept_keyword):
            err = "Invalid department, please enter a valid department."
            print err
            return render_template('search_results.html',results=[],error_message=err)
    

    course_keyword = request.args.get('course_no')

    print "DEPT KEYWORD:",dept_keyword
    print "COURSE KEYWORD:",course_keyword
    # case where no course number is specified
    if not course_keyword:
        #just pull all the courses under that dept
        results0 = db.group_sessions.find({DEPARTMENT_KEY:dept_keyword}).sort(TIME_KEY)
        results0=cursortolst(results0)
        print results0
        if len(results0) > 0:
            print "Got results0"
            isAttendee=attendee(results0,user)
            return return_db_results(results0,user,userID,isAttendee)

    # TODO: verify course number is safe?
    # Query database with search_keyword. Dept number + 3 num code. If fails,
    results1 = db.group_sessions.find({DEPARTMENT_KEY:dept_keyword,COURSE_NUMBER_KEY:course_keyword}).sort(TIME_KEY)
    results1=cursortolst(results1)
    if len(results1) > 0:
        print "Got results1, yippee!"
        isAttendee=attendee(results1,user)
        return return_db_results(results1,user,userID,isAttendee)

    # # try same thing with the first two numbers (if there are 2-3 numbers) to get closest matches. If nothing,
    # twoOrThree = False
    # if len(course_keyword) == 2:
    #     short_course_keyword = course_keyword
    #     twoOrThree = True
    # if len(course_keyword) == 3:
    #     short_course_keyword = course_keyword[0:2]
    #     twoOrThree = True
    # if twoOrThree:
    #     print "TWO OR THREE",short_course_keyword
    #     results2 = db.group_sessions.find({DEPARTMENT_KEY:dept_keyword,COURSE_NUMBER_KEY:short_course_keyword}).sort(TIME_KEY)
    #     if results2.count() > 0:
    #         print "Got results2, yippee!"
    #         return return_db_results(results2,user,userID)

    # else we have no results
    print "NO RESULTS"
    return render_template('search_results.html',results=[],count=0)


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

##
# Responds to route /lucky, returning a random group study session from database.
##
@app.route('/lucky')
def lucky():
    number_of_records = db.group_sessions.count()
    random_number = random.randint(0,number_of_records-1)
    group_session = db.group_sessions.find().limit(-1).skip(random_number).next()
    return 'picked random session with id: ' + str(group_session['_id'])

@app.route('/new',methods=['POST'])
def new():
    # get the data from the request
    dept = request.form.get('department')
    course = request.form.get('course')
    location = request.form.get('location')
    time = request.form.get('datetime')
    contact = request.form.get('contact')
    session_details = request.form.get('details')

    # validate data
    errors = []
    if not departmentArray.validDept(dept):
        err1 = "DEPARTMENT DOES NOT EXIST", dept
        errors.append(err1)
    if not len(course) == 3:
        err2 = "BAD COURSE NUMBER", course
        errors.append(err2)
    if len(location) > 255:
        err3 = "Location too long, please limit to 255 chars or less", location
        errs.append(err3)

    # convert/validate time
    #time = 123456543

    #add more future validation here
    if errors:
        print "ERRORS:"
        for i in errors: print i
        return render_template('create.html',results=errors)

    # get user from session
    print session
    #user = session.get_user....?
    ownerID = "123456"
    user='jon doe'
    # create group session object
    group_session = {
        OWNER_ID_KEY : ownerID,
        DEPARTMENT_KEY : dept,
        COURSE_NUMBER_KEY : course,
        LOCATION_KEY : location,
        TIME_KEY : time,
        CONTACT_KEY : contact,
        DESCRIPTION_KEY : session_details,
        ATTENDEES_KEY: [[ownerID,user]]
    }

    print "GROUP SESSION:",group_session
    # insert info into database 
    if db.group_sessions.find_one(group_session):
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
    coll.update({'_id' : group_id}, new_data)

    # Show the updated results page.


@app.route('/delete',methods=['POST'])
def delete():
    # TODO: verify that user in session owns the group session to be deleted
    pass

##
# Add the current user to the selected study session group.
# Responds to route of the form:
#   /join?group_id=<group_id>
#   
#   group_id : string
##
@app.route('/adduser',methods=['POST'])
def adduser():
    return "abc"

##
# Add the current user to the selected study session group.
# Responds to route of the form:
#   /join?group_id=<group_id>
#   
#   group_id : string
##
@app.route('/join',methods=['POST'])
def join():
    user = db.users.find_one({"userID": current_user.id})
    current_study_group = db.group_sessions.find_one({'_id': group_id})

    # Check that user is in the attendees of current_study_group
    # if user in usercurrent_study_group.attendees:
        # Show user that he/she is already in the group.

    coll = db.group_sessions
    new_attendees_list = coll.attendees.add(user)
    coll.update({'_id': current_study_group.id},
                {ATTENDEES_KEY : new_attendees_list})
    # Return that the database was updated and refresh the page with new attendees list.

def ISOToEpoch(timestring):
    return time.mktime(parse(timestring).timetuple())

def return_db_results(results,user,userID,isAttendee):
    return render_template('search_results.html',count=len(results),results=list(results),user=user,userID=userID,isAttendee=list(isAttendee))

def attendee(grps,userID):
    isAttendee=[]
    for grp_session in grps:
        for user in grp_session[ATTENDEES_KEY]:
            if userID==user[0]:
                isAttendee.append(True)
                break
            isAttendee.append(False)
    return isAttendee

def cursortolst(grps):
    return_list=[]
    for item in grps:
        return_list.append(item)
    return return_list


if __name__ == "__main__":
	app.run(debug=True)







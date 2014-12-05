from . import app, db, mongo_db

from flask import Flask, url_for, redirect, session, render_template, request, flash
from flask_login import (UserMixin, login_required, login_user, logout_user,
                         current_user)
from flask.ext.wtf import Form
from .forms import RegistrationForm, LoginForm
from flask_googlelogin import GoogleLogin
import json
from jinja2 import Template
# from flask.ext.pymongo import PyMongo
from pymongo import MongoClient
import departmentArray
import random
import time
from dateutil.parser import parse
from bson.json_util import dumps
from helpers import *
from datetime import datetime
from werkzeug.security import generate_password_hash
from mongokit import ObjectId

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
NAME="name"

@app.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm(request.form)
    if form.validate_on_submit():
        print "form validated"
        login_user(form.get_user(), remember=form.remember.data) # login_user(user, remember=True)
        flash("Logged in succesfully")
        return redirect(request.args.get("next") or url_for('home'))
    return render_template('login.html', form=form)

@app.route('/user', defaults={'user_id' : None})
@app.route('/user/<user_id>', methods=["GET", "POST"])
#@login_required
def user(user_id):
    if user_id is None:
        user = current_user
    else:
        user = mongo_db.users.User.find_one({'_id' : ObjectId(user_id)})

    if request.method == "POST":
        # /user/<user_id>?new_class=<class name>
        if 'new_class' in request.args:
            old_classes = user.classes
            old_classes.append(request.args.get('new_class'))
            user.classes = old_classes
            if user.save():
                return 'success!'
            else:
                return "didn't work"
    else:
        if user_id is None:
            return render_template('profile.html', user=current_user)      
        else:
            user = mongo_db.users.User.find_one({'_id' : ObjectId(user_id)})
            return render_template('profile.html', user=user)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm(request.form)
    if form.validate_on_submit():
        # Create user
        user_email = form.email.data
        password = form.password.data

        if mongo_db.users.User.find({'email' : user_email}).count() > 0:
            flash('An account with that email already exists!')
            form = RegistrationForm()
            return render_template('register.html', form=form)
        else:
            new_user = mongo_db.users.User()
            new_user.email = user_email
            new_user.password = generate_password_hash(password)
            new_user.save()

        # log user in
        login_user(new_user)
        return redirect(url_for('home'))
    if 'user_email' in session:
        return render_template('register.html', email=session['user_email'], form=form)
    else:
        return render_template('register.html', form=form)

@app.route("/")
def home():
    return render_template('index.html')

@app.route("/group/<group_id>")
def group(group_id):
    group = mongo_db.study_sessions.StudySession.find({'id' : ObjectId()})
    return render_template('group.html', group=group)

# Search for a class. Dept is fixed but number is free, must be 3 num code
# TODO: search doesn't work correctly, always returns everything from the database, no matter what we search for.
@app.route("/find")
def search():

    if 'new_find' in request.args: # request coming from /find page
        search_query = request.args.get('new_find').lower()
        dept_keyword, course_keyword = parse_new_find(search_query)
    else:
        course_keyword = request.args.get('course_no')
        dept_keyword = request.args.get('dept_keyword').lower()

    print "DEPT KEYWORD:",dept_keyword
    print "COURSE KEYWORD:",course_keyword

    search_results = None
    results_exist = True

    if course_keyword and dept_keyword:
        search_results = mongo_db.study_sessions.StudySession.find(
            {'course_no' : course_keyword, 'department' : dept_keyword})
        print search_results , "We are in if condition"
    elif dept_keyword and not course_keyword:
        print "only department entered"
        search_results = mongo_db.study_sessions.StudySession.find(
            {'department' : dept_keyword})
    elif not dept_keyword and not course_keyword:
        search_results = mongo_db.study_sessions.StudySession.find()
    else:
        flash('Enter something to search!')
        return render_template('index.html')

    # else we have no results
    if search_results.count() > 0:
        print "Text"
        for result in search_results:
            print result
    else:
        results_exist = False
    
    search_results.rewind()
    return render_template('search_results.html', results = search_results, 
        results_exist = results_exist)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/create')
def create():
    return render_template('create.html',username='dummy');
    #return render_template('create.html',username=session['username']);

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
    name=request.form.get('name')
    dept = request.form.get('department').lower()
    course = request.form.get('course')
    location = request.form.get('location')
    time =  datetime.strptime(request.form.get('datetime'), '%Y-%m-%dT%H:%M')
    contact = request.form.get('contact').lower()
    description = request.form.get('description')
    session_details = request.form.get('details')

    # validate data
    errors = []
    if not departmentArray.validDept(dept):
        err1 = "DEPARTMENT DOES NOT EXIST", dept
        errors.append(err1)
    # if not len(course) == 3:
    #     err2 = "BAD COURSE NUMBER", course
    #     errors.append(err2)
    # if len(location) > 255:
    #     err3 = "Location too long, please limit to 255 chars or less", location
    #     errs.append(err3)

    # convert/validate time
    #time = 123456543

    #add more future validation here
    if errors:
        print "ERRORS:"
        for i in errors: print i
        return render_template('create.html',username='dummy',results=errors)
        #return render_template('create.html',username=session['username'],results=errors)

    # get user from session
    user='dummy'
    ownerID = 'dummy'
    #user=session['username']
    #ownerID = session['userid']

    # create group session object
    new_session=mongo_db.study_sessions.StudySession()
    new_session.department=dept
    new_session.course_no=course
    new_session.time=time
    new_session.location=location
    new_session.description=description
    new_session.contact_info=contact
    new_session.details=session_details
    new_session.name=name
    new_session.save()
    print "GROUP SESSION:",group_session
    # insert info into dabase 
    if mongo_db.study_sessions.StudySession.find_one(new_session):
    #if db.group_sessions.find_one(group_session):
        errX = "Group already exists",group_session
        print errX
        # TODO: confirm event created in DB
        return render_template('create.html',username='dummy',results=errX)
        #return render_template('create.html',username=session['username'],results=errX)
    else:
        print "Unique group"
        db.group_sessions.insert(group_session)
        return render_template('index.html',username='dummy')
        #return render_template('index.html',username=session['username'])

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
@app.route('/join',methods=['POST'])
def join():
    user = db.users.find_one({"userID": session['userid']})
    group_id = request.args.get('group_id')
    db_results_list = cursortolst(db.group_sessions.find())

    insert_item = {}
    
    for item in db_results_list:
        print str(item['_id']) + " =? " + str(group_id)
        if str(group_id) == str(item['_id']):
            print "we have a match!"
            item[ATTENDEES_KEY].append([user['userID'], user['name']])
            insert_item = item
    # current_study_group = db.group_sessions.find_one({'_id': group_id})
    print insert_item
    # Check that user is in the attendees of current_study_group
    # if user in usercurrent_study_group.attendees:
        # Show user that he/she is already in the group.

    coll = db.group_sessions
    #new_attendees_list = current_study_group[ATTENDEES_KEY].add(user)
    coll.update({'_id': insert_item['_id']}, insert_item, True)
    print list(coll.find())
    # Return that the database was updated and refresh the page with new attendees list.
    return 'success'

def ISOToEpoch(timestring):
    return time.mktime(parse(timestring).timetuple())

def return_db_results(results,user,userID,isAttendee):
    return render_template('search_results.html',username=session['username'],count=len(results),results=list(results),user=user,userID=userID,isAttendee=list(isAttendee))

def attendee(grps,userID):
    print "user id is: " + userID
    isAttendee=[]
    for grp_session in grps:
        isAttendeeInGroup = False
        for user in grp_session[ATTENDEES_KEY]:
            if userID == user[0]:
                isAttendeeInGroup = True
                break
        isAttendee.append(isAttendeeInGroup)
    return isAttendee

def cursortolst(grps):
    return_list=[]
    for item in grps:
        return_list.append(item)
    return return_list


if __name__ == "__main__":
	app.run(debug=True)







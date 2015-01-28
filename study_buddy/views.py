from study_buddy import app, APP_ROOT
from init_db import mongo_db
from forms import RegistrationForm, LoginForm, GroupForm, EmailForm, PasswordForm, EditUserForm
from helpers import *

from flask import url_for, redirect, session, render_template, request, flash
from pymongo import ASCENDING, DESCENDING
from mongokit import ObjectId
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash
from uuid import uuid4
from json import loads

from flask.ext.login import login_required, login_user, logout_user, current_user
from flask.ext.wtf import Form


@app.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm(request.form)
    if form.validate_on_submit():
        print "form validated"
        login_user(form.get_user(), remember=form.remember.data) # login_user(user, remember=True)
        flash("Logged in succesfully")
        return redirect(request.args.get("next") or url_for('home'))
    return render_template('login.html', form=form)

@app.route('/user/<user_id>')
def user(user_id):
    user = mongo_db.users.User.find_one({'_id' : ObjectId(user_id)})
    return render_template('profile.html', user=current_user)

@app.route('/user/delete/<class_name>', methods=["POST"])
@login_required
def delete_class(class_name):
    if current_user.is_authenticated():
        mongo_db.users.update({'_id' : ObjectId(current_user._id)}, {'$pull' : {'classes' : class_name.lower()}})
    return redirect(url_for('edit_user', user_id=current_user._id))

@app.route('/user/add', methods=["POST"])
@login_required
def add_class():
    if current_user.is_authenticated():
        class_name = request.form['new_class'].lower()
        if mongo_db.users.find({'_id' : ObjectId(current_user._id), 
                                'classes' : {'$in' : [class_name]}}).count() <= 0:
            mongo_db.users.update({'_id' : ObjectId(current_user._id)}, {'$push' : {'classes' : class_name}})
        return redirect(url_for('edit_user', user_id=current_user._id))
    else:
        flash('You are not allowed to do this!')
        return redirect(url_for('home'))


@app.route('/edit/<user_id>', methods=["GET", "POST"])  
@login_required
def edit_user(user_id):
    user = mongo_db.users.User.find_one({'_id' : ObjectId(user_id)})  
    if request.method == "POST":
        user.name.first = request.form['first_name']
        user.name.last = request.form['last_name']
        user.save()
        return redirect(url_for('edit_user', user_id=user_id))
    return render_template('edit_user.html', user=user)



@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm(request.form)
    if form.validate_on_submit():
        # Create user
        new_user = mongo_db.users.User()
        new_user.email = form.email.data.lower()
        new_user.password = generate_password_hash(form.password.data)
        new_user.school = school_name_from_email(form.email.data.split('@')[1].strip())
        new_user.verified = False
        new_user.save()

        # log user in
        login_user(new_user)
        flash('Check your email for verification!')
        send_verification_email(new_user.email)
        return redirect(url_for('home'))
    if 'user_email' in session:
        return render_template('register.html', email=session['user_email'], form=form)
    else:
        return render_template('register.html', form=form)

@app.route('/verify/<token>')
def verify(token):
    try:
        email = ts.loads(token, salt="email-confirm-key", max_age=86400)
    except:
        abort(404)

    user = mongo_db.users.User.find_one({'email' : email})
    print "User:", user.email
    user.verified = True
    user.save()
    login_user(user)
    return redirect(url_for('login'))

@app.route('/reset', methods=["GET", "POST"])
def reset_password():
    form = EmailForm()
    if form.validate_on_submit():
        user = mongo_db.users.User.find_one({'email' : form.email.data})

        subject = "Succor password reset requested"
        token = ts.dumps(user.email, salt='recover-key')
        recover_url = url_for('reset_with_token', token=token, _external=True)
        body = render_template('email/recover.txt', url=recover_url)
        html = render_template('email/recover.html', url=recover_url)
        send_email(subject, app.config['ADMINS'][0], [user.email], body, html)

        flash('Check your email for password reset link')
        return redirect(url_for('home'))
    return render_template('reset.html', form=form)

@app.route('/reset/<token>', methods=["GET", "POST"])
def reset_with_token(token):
    try:
        email = ts.loads(token, salt="recover-key", max_age=86400)
    except:
        abort(404)

    form = PasswordForm()

    if form.validate_on_submit():
        user = mongo_db.users.User.find_one({'email' : email})
        user.password = generate_password_hash(form.password.data)
        user.save()

        return redirect(url_for('login'))
    return render_template('reset_with_token.html', form=form, token=token)

@app.route('/')
def home():
    if not request.cookies.get('succor-visited'):
        is_first_time = True
    if request.cookies.get('succor-visited'):
        request.set_cookie('succor-visited', value=True)
    return render_template('index.html', is_first_time=is_first_time)

@app.route("/group/<group_id>")
def group(group_id):
    group = mongo_db.study_sessions.StudySession.find_one({'_id' : ObjectId(group_id)})
    return render_template('group.html', group=group)

@app.route("/about")
def about():
    people_bios = open(APP_ROOT + '/people_bios.json').read()
    people_data = loads(people_bios)
    return render_template('about.html', people_data=people_data)

@app.route("/find")
def search():

    if 'new_find' in request.args: # request coming from /find page
        search_query = request.args.get('new_find').lower()
        dept_keyword, course_keyword = parse_new_find(search_query)
    else:
        course_keyword = request.args.get('course_no')
        dept_keyword = request.args.get('dept_keyword').lower()

    # Get location data.
    # longitude = float(request.args.get('geo_location').split(',')[1])
    # latitude = float(request.args.get('geo_location').split(',')[0])
    # location = [longitude, latitude]

    # Get current datetime.
    date_now = datetime.today() - timedelta(hours=1)

    # Build search query.
    upcoming_query_object = {'time' : {'$gte' : date_now}}
    old_query_object = {'time' : {'$lt' : date_now}}
    if dept_keyword:
        upcoming_query_object['department'] = dept_keyword
        old_query_object['department'] = dept_keyword
        
        if course_keyword:
            upcoming_query_object['course_no'] = course_keyword
            old_query_object['course_no'] = course_keyword
    
    if current_user.is_authenticated():
        upcoming_query_object['school'] = current_user.school
        old_query_object['school'] = current_user.school
    else:
        location_query = {
                            '$near' : {
                                '$geometry' : {
                                    'type' : 'Point',
                                    'coordinates' : location
                                },
                                '$maxDistance' : 5000
                            }   
                        }
        # upcoming_query_object['geo_location'] = location_query
        # old_query_object['geo_location'] = location_query

    print "upcoming query", upcoming_query_object
    print "old query", old_query_object

    # Make database query.
    upcoming_search_results = mongo_db.study_sessions.StudySession.find(upcoming_query_object)
    old_search_results = mongo_db.study_sessions.StudySession.find(old_query_object)
    
    upcoming_search_results.sort('time', ASCENDING)
    old_search_results.sort('time', DESCENDING)

    upcoming_search_results.rewind()
    return render_template('search_results.html', 
        upcoming_results = upcoming_search_results,
        old_results = old_search_results, 
        results_exist = (upcoming_search_results.count() > 0 or old_search_results.count() > 0))


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/create', methods=["POST","GET"])
def create():
    create_form = GroupForm(request.form)
    if create_form.validate_on_submit():
        new_session=mongo_db.study_sessions.StudySession()
        # Get and parse gelocation data from form.
        # location_data = create_form.geo_location.data.split(',')
        # lat = float(location_data[0])
        # lon = float(location_data[1])
        # new_session.geo_location={
        #     'type':'Point',
        #     'coordinates':[lon, lat]}
        # store department as lower case so search works
        new_session.department=create_form.department.data.lower() 
        new_session.course_no=str(create_form.course_no.data)
        new_session.time=create_form.datetime.data
        new_session.location=create_form.where.data
        new_session.description=create_form.assignment.data
        if current_user.is_authenticated():
            new_session.contact_info=current_user.email
            new_session.name=current_user.name.first + ' ' + current_user.name.first
            new_session.school=current_user.school
        else:
            new_session.contact_info=create_form.email.data
            new_session.name='Anonymous'

        new_session.details=create_form.details.data
        
        new_session.save()
        flash("Group Created!")
        return redirect(url_for('group', group_id=new_session._id))
    return render_template('create.html',username='dummy', form=create_form);
    #return render_template('create.html',username=session['username']);

@app.route('/all-nighter')
def allnighter():
    return render_template('index.html')
# ##
# # Responds to route /lucky, returning a random group study session from database.
# ##
# @app.route('/lucky')
# def lucky():
#     number_of_records = db.group_sessions.count()
#     random_number = random.randint(0,number_of_records-1)
#     group_session = db.group_sessions.find().limit(-1).skip(random_number).next()
#     return 'picked random session with id: ' + str(group_session['_id'])

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
# @app.route('/edit',methods=['POST'])
# def edit():
#     department = request.args.get('department')
#     course_no = request.args.get('course_no')
#     location = request.args.get('location')
#     time = request.args.get('time')
#     attendees = request.args.get('attendees')
#     course_notes = request.args.get('course_notes')
#     group_id = request.args.get('group_id')

#     coll = db.group_sessions
#     new_data = {DEPARTMENT_KEY    : department,
#                 COURSE_NUMBER_KEY : course_no,
#                 LOCATION_KEY      : location,
#                 TIME_KEY          : time,
#                 ATTENDEES_KEY     : attendees,
#                 COURSE_NOTES_KEY  : course_notes}

#     # verify that user owns the group before updating database.
#     coll.update({'_id' : group_id}, new_data)

#     # Show the updated results page.


# @app.route('/delete',methods=['POST'])
# def delete():
#     # TODO: verify that user in session owns the group session to be deleted
#     pass

##
# Add the current user to the selected study session group.
# Responds to route of the form:
#   /join?group_id=<group_id>
#   
#   group_id : string
##
# @app.route('/join',methods=['POST'])
# def join():
#     user = db.users.find_one({"userID": session['userid']})
#     group_id = request.args.get('group_id')
#     db_results_list = cursortolst(db.group_sessions.find())

#     insert_item = {}
    
#     for item in db_results_list:
#         print str(item['_id']) + " =? " + str(group_id)
#         if str(group_id) == str(item['_id']):
#             print "we have a match!"
#             item[ATTENDEES_KEY].append([user['userID'], user['name']])
#             insert_item = item
#     # current_study_group = db.group_sessions.find_one({'_id': group_id})
#     print insert_item
#     # Check that user is in the attendees of current_study_group
#     # if user in usercurrent_study_group.attendees:
#         # Show user that he/she is already in the group.

#     coll = db.group_sessions
#     #new_attendees_list = current_study_group[ATTENDEES_KEY].add(user)
#     coll.update({'_id': insert_item['_id']}, insert_item, True)
#     print list(coll.find())
#     # Return that the database was updated and refresh the page with new attendees list.
#     return 'success'









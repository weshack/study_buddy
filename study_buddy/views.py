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
from inflection import titleize

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
    return render_template('profile.html', user=user)

@app.route('/user/delete/<class_name>', methods=["POST"])
@login_required
def delete_class(class_name):
    if current_user.is_authenticated():
        mongo_db.users.update({'_id' : ObjectId(current_user._id)}, {'$pull' : {'classes' : class_name}})
    return redirect(url_for('edit_user', user_id=current_user._id))

@app.route('/user/add', methods=["POST"])
@login_required
def add_class():
    if current_user.is_authenticated():
        class_name = request.form['new_class'].lower()
        dept_keyword, course_keyword = parse_new_find(class_name)
        smart_class_name = smart_search(dept_keyword, current_user.school)
        mongo_db.users.update({'_id' : ObjectId(current_user._id)},
            {'$addToSet' : {
                'classes' : (smart_class_name + " " + course_keyword).strip()
            }})
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
        user.name.full = titleize(request.form['first_name'] + ' ' + request.form['last_name'])
        user.save()
        return redirect(url_for('edit_user', user_id=user_id))
    return render_template('edit_user.html', user=user)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm(request.form)
    print "creating form"
    if form.validate_on_submit():
        print "validated form"
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
        print form.errors
        print "form not validated or not post request"
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
        send_email(subject, app.config['FROM_EMAIL_ADDRESS'], [user.email], body, html)

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
    return render_template('index.html')

@app.route("/group/<group_id>")
def group(group_id):
    group = mongo_db.study_sessions.StudySession.find_one({'_id' : ObjectId(group_id)})
    participants = mongo_db.users.find({'_id' : { '$in' : group.participants }})
    return render_template('group.html', group=group, participants=participants)

@app.route("/group/join/<group_id>", methods=["POST"])
@login_required
def join_group(group_id):
    full_name = current_user.name.full or None
    mongo_db.study_sessions.update({'_id' : ObjectId(group_id)},
        {'$addToSet' : {
            'participants' : current_user._id
        }})
    return redirect(url_for('group', group_id=group_id))

@app.route("/group/leave/<group_id>", methods=["POST"])
@login_required
def leave_group(group_id):
    if current_user.is_authenticated():
        group = mongo_db.study_sessions.update({'_id' : ObjectId(group_id)},
            {'$pull' : {
                'participants' : current_user._id
            }})
    return redirect(url_for('group', group_id=group_id))

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
    
    if current_user.is_authenticated():
        smart_dept_keyword = smart_search(dept_keyword, current_user.school)
        upcoming_query_object['school'] = current_user.school
        old_query_object['school'] = current_user.school
    # else:
    #     location_query = {
    #                         '$near' : {
    #                             '$geometry' : {
    #                                 'type' : 'Point',
    #                                 'coordinates' : location
    #                             },
    #                             '$maxDistance' : 5000
    #                         }   
    #                     }
        # upcoming_query_object['geo_location'] = location_query
        # old_query_object['geo_location'] = location_query
    else:
        smart_dept_keyword = smart_search(dept_keyword, None)

    if dept_keyword:
        upcoming_query_object['department'] = smart_dept_keyword
        old_query_object['department'] = smart_dept_keyword
        
        if course_keyword:
            upcoming_query_object['course_no'] = course_keyword
            old_query_object['course_no'] = course_keyword

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
        print "form validated"
        new_session=mongo_db.study_sessions.StudySession()
        # Get and parse gelocation data from form.
        # location_data = create_form.geo_location.data.split(',')
        # lat = float(location_data[0])
        # lon = float(location_data[1])
        # new_session.geo_location={
        #     'type':'Point',
        #     'coordinates':[lon, lat]}
        # store department as lower case so search works 
        new_session.course_no=str(create_form.course_no.data)
        new_session.time=create_form.datetime.data
        new_session.location=create_form.where.data
        new_session.description=create_form.assignment.data
        if current_user.is_authenticated():
            new_session.contact_info=current_user.email
            new_session.name=current_user.name.first + ' ' + current_user.name.last
            new_session.school=current_user.school
            new_session.department=smart_search(create_form.department.data, 
                                                current_user.school)
        else:
            new_session.contact_info=create_form.email.data
            new_session.name='Anonymous'
            new_session.school=create_form.school.data
            new_session.department=smart_search(create_form.department.data,
                                                create_form.school.data)

        new_session.details=create_form.details.data
        
        new_session.save()
        flash("Group Created!")
        return redirect(url_for('group', group_id=new_session._id))
    return render_template('create.html',username='dummy', form=create_form);
    #return render_template('create.html',username=session['username']);

@app.route('/all-nighter')
def allnighter():
    return render_template('index.html')










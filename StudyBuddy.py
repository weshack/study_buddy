from flask import Flask, url_for, redirect, session, render_template, request
from flask_login import (UserMixin, login_required, login_user, logout_user,
                         current_user)
from flask_googlelogin import GoogleLogin
import json
from jinja2 import Template
# from flask.ext.pymongo import PyMongo
from pymongo import MongoClient
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
def root():
    return app.send_static_file('html/index.html')

# Make a search for a class
@app.route('/find')
def search():
    search_keyword = request.args.get('search_keyword')
    
    # Query database with search_keyword
    # db.group_sessions.find
    search_results = [1,2,3] #StudySessions.objects(class_name=search_keyword)

    # Return template with object full of data
    return render_template('search_results.html', results=search_results)


@app.route('/login')
def index():
    return render_template('login.html', 
        login_link=googlelogin.login_url(approval_prompt='force'))

    """
        <p><a href="%s">Login</p>
    """ % (googlelogin.login_url(approval_prompt='force',scopes=["email"]))

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
    login_user(user)
    session['token'] = json.dumps(token)
    return redirect(params.get('next', url_for('.login_redirect')))


@app.route('/login_redirect')
@login_required
def login_redirect():
    # deny access to anyone without an @wesleyan.edu email address
    deny = False
    if deny:
        return
        # redirect to same page, display error
        # return redirect(params.get('next', url_for('.profile')))
    # if success, add user to db if not exists
    print "CURRENT USER", current_user.email
    db.users.insert({"name":current_user.name,"userID":"1234"})
    return redirect('/home')

@app.route('/logout')
def logout():
    logout_user()
    session.clear()
    return """
        <p>Logged out</p>
        <p><a href="/">Return to /</a></p>
        """

@app.route('/checkin')
def checkin():
    return 'hello'

if __name__ == "__main__":
	app.run(debug=True)

from flask import Flask, url_for, redirect, session, render_template, request
from flask_login import (UserMixin, login_required, login_user, logout_user,
                         current_user)
from flask_googlelogin import GoogleLogin
import json
from jinja2 import Template

users = {}
app = Flask(__name__, static_url_path='')

app.config.update(
    SECRET_KEY='Miengous3Xie5meiyae6iu6mohsaiRae',
    GOOGLE_LOGIN_CLIENT_ID='1002179078501-mdq5hvm940d0hbuhqltr0o1qhsr7sduc.apps.googleusercontent.com',
    GOOGLE_LOGIN_CLIENT_SECRET='O1kpQ8Is9s2pD3eOpxRfh-7x',
    GOOGLE_LOGIN_REDIRECT_URI='http://127.0.0.1:5000/oauth2callback')
   
googlelogin = GoogleLogin(app)

@googlelogin.user_loader
def get_user(userid):
    return users.get(userid)


class User(UserMixin):
    def __init__(self, userinfo):
        self.id = userinfo['id']
        self.name = userinfo['name']

@app.route("/")
def root():
    return app.send_static_file('html/index.html')

# Make a search for a class, and return a json object.
@app.route('/find')
def search():
    search_keyword = request.args.get('search_keyword')
    
    # Query database with search_keyword
    search_results = [1,2,3] #StudySessions.objects(class_name=search_keyword)

    # Return template with object full of data
    return render_template('search_results.html', results=search_results)


@app.route('/login')
def index():
    return """
        <p><a href="%s">Login</p>
    """ % (googlelogin.login_url(approval_prompt='force'))


# Google OAuth
@app.route('/oauth2callback')
@googlelogin.oauth2callback
def login(token, userinfo, **params):
    user = users[userinfo['id']] = User(userinfo)
    login_user(user)
    session['token'] = json.dumps(token)
    print user
    return redirect(params.get('next', url_for('.profile')))


@app.route('/profile')
@login_required
def profile():
    return """
        <p>Hello, %s</p>
        <p>Token: %r</p>
        <p><a href="/logout">Logout</a></p>
        """ % (current_user.name, session.get('token'))

@app.route('/logout')
def logout():
    logout_user()
    session.clear()
    return """
        <p>Logged out</p>
        <p><a href="/">Return to /</a></p>
        """

if __name__ == "__main__":
	app.run(debug=True)

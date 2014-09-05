from flask import Flask, url_for, redirect, session
from flask_login import (UserMixin, login_required, login_user, logout_user,
                         current_user)
from flask_googlelogin import GoogleLogin
import json

users = {}

app = Flask(__name__)
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
        self.picture = userinfo.get('picture')

@app.route("/")
def hello():
  return "Hello world"

# Make a search for a class, and return a json object.
@app.route("/search/<keyword>")
def search(keyword):
	return "search page: " + keyword


@app.route('/login')
def index():
    return """
        <p><a href="%s">Login</p>
        <p><a href="%s">Login with extra params</p>
        <p><a href="%s">Login with extra scope</p>
    """ % (
        googlelogin.login_url(approval_prompt='force'),
        googlelogin.login_url(approval_prompt='force',
                              params=dict(extra='large-fries')),
        googlelogin.login_url(
            approval_prompt='force',
            scopes=['https://www.googleapis.com/auth/drive'],
            access_type='offline',
        ),
    )


# Google OAuth
@app.route('/oauth2callback')
@googlelogin.oauth2callback
def create_or_update_user(token, userinfo, **params):
    user = User.filter_by(google_id=userinfo['id']).first()
    if user:
        user.name = userinfo['name']
        user.avatar = userinfo['picture']
    else:
        user = User(google_id=userinfo['id'],
                    name=userinfo['name'],
                    avatar=userinfo['picture'])
    db.session.add(user)
    db.session.flush()
    login_user(user)
    return redirect(url_for('index'))


@app.route('/profile')
@login_required
def profile():
    return """
        <p>Hello, %s</p>
        <p><img src="%s" width="100" height="100"></p>
        <p>Token: %r</p>
        <p>Extra: %r</p>
        <p><a href="/logout">Logout</a></p>
        """ % (current_user.name, current_user.picture, session.get('token'),
               session.get('extra'))

@app.route('/oauth2callback')
@googlelogin.oauth2callback
def login(token, userinfo, **params):
    user = users[userinfo['id']] = User(userinfo)
    login_user(user)
    session['token'] = json.dumps(token)
    session['extra'] = params.get('extra')
    return redirect(params.get('next', url_for('.profile')))

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

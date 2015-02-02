from flask import Flask, render_template, request, session, abort

# from flask.ext.wtf.csrf import CsrfProtect
from flask.ext.assets import Environment, Bundle
from flask.ext.mail import Mail, Message

from itsdangerous import URLSafeTimedSerializer
from inflection import titleize

import os, binascii

app = Flask(__name__)

app.config.from_object('study_buddy.base_config')
app.config.from_object('study_buddy.local_config')

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

def output_time(result):
    format = "%a, %-d at %-I:%M %p"
    return result.strftime(format)	

def generate_csrf_token():
    if '_csrf_token' not in session:
    	print "Generating CSRF token..."
        session['_csrf_token'] = binascii.hexlify(os.urandom(24))
   	print "Session contains CSRF token:", session['_csrf_token']
    return session['_csrf_token']		

# assets = Environment(app)
# scss = Bundle('', filters='pyscss', output='all.css')
# assets.register('scss_all', scss)

# csrf = CsrfProtect()
# csrf.init_app(app)

ts = URLSafeTimedSerializer(app.config["SECRET_KEY"])

mail = Mail(app)

print "Running app..."
app.jinja_env.globals.update(output_time=output_time)
app.jinja_env.globals.update(titleize=titleize)
app.jinja_env.globals['csrf_token'] = generate_csrf_token

from study_buddy import views, models

@app.errorhandler(404)
def page_not_found(e):
	return render_template('404.html'), 404

@app.before_request
def csrf_protect():
    if request.method == "POST":
        token = session.pop('_csrf_token', None)
        print "CSRF Token from form", request.form.get("_csrf_token")
        print "CSRF Token from session:", token
        if not token or token != request.form.get('_csrf_token'):
            abort(403)


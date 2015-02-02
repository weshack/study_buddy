from flask import Flask, render_template, request, session, abort

from flask.ext.wtf.csrf import CsrfProtect
from flask.ext.assets import Environment, Bundle
from flask.ext.mail import Mail, Message

from itsdangerous import URLSafeTimedSerializer
from inflection import titleize

import os, binascii

app = Flask(__name__)

app.secret_key = os.urandom(24)

app.config.from_object('study_buddy.base_config')
app.config.from_object('study_buddy.local_config')

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

def output_time(result):
    format = "%a, %-d at %-I:%M %p"
    return result.strftime(format)			

# assets = Environment(app)
# scss = Bundle('', filters='pyscss', output='all.css')
# assets.register('scss_all', scss)

csrf = CsrfProtect()
csrf.init_app(app)

ts = URLSafeTimedSerializer(app.config["SECRET_KEY"])

mail = Mail(app)

print "Running app..."
app.jinja_env.globals.update(output_time=output_time)
app.jinja_env.globals.update(titleize=titleize)

from study_buddy import views, models

@app.errorhandler(404)
def page_not_found(e):
	return render_template('404.html'), 404

@csrf.error_handler
def csrf_error(reason):
    return render_template('csrf_error.html', reason=reason), 400


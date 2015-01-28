from flask import Flask, render_template

from flask.ext.wtf.csrf import CsrfProtect
from flask.ext.assets import Environment, Bundle
from flask.ext.mail import Mail, Message

from itsdangerous import URLSafeTimedSerializer
from inflection import titleize

import os

app = Flask(__name__)

app.config.from_object('study_buddy.base_config')
app.config.from_envvar('SUCCOR_CONFIG_FILE')

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

def output_time(result):
    format = "%a, %-d at %-I:%M %p"
    return result.strftime(format)

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

from study_buddy import views, models

@app.errorhandler(404)
def page_not_found(e):
	return render_template('404.html'), 404

from flask import Flask, render_template
from flask.ext.login import LoginManager
from flask.ext.wtf.csrf import CsrfProtect
from flask.ext.assets import Environment, Bundle

from mongokit import ObjectId, Connection
from json import loads

import os

from models import *

app = Flask(__name__)

app.config['SECURITY_POST_LOGIN'] = '/profile'

app.config.update(
    SECRET_KEY='Tieng3us3Xie5meiyae6iKKHVUIUDF'
)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

def output_time(result):
    format = "%a, %-d at %-I:%M %p"
    return result.strftime(format)

connection = Connection()
connection.register([StudySession, User])
mongo_db = connection.succor

# assets = Environment(app)
# scss = Bundle('', filters='pyscss', output='all.css')
# assets.register('scss_all', scss)

# login_manager = LoginManager()
# login_manager.init_app(app)
# login_manager.login_view = 'login'

# csrf = CsrfProtect()
# csrf.init_app(app)

people_bios = open(APP_ROOT + '/people_bios.json').read()
people_data = loads(people_bios)

print "Running app..."
app.jinja_env.globals.update(output_time=output_time)
from study_buddy import views, models

@app.errorhandler(404)
def page_not_found(e):
	return render_template('404.html'), 404

# @login_manager.user_loader
# def load_user(user_id):
# 	return mongo_db.users.User.find_one({'_id' : ObjectId(user_id)})
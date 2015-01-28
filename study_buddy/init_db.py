from study_buddy import app

from models import StudySession, User

from pymongo import GEOSPHERE
from mongokit import Connection, ObjectId

from flask.ext.login import LoginManager

connection = Connection(host=app.config['DB_HOST'], port=app.config['DB_PORT'])
connection.register([StudySession, User])
mongo_db = connection[app.config['DB_NAME']]
mongo_db.study_sessions.ensure_index([('geo_location', GEOSPHERE)])

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
	return mongo_db.users.User.find_one({'_id' : ObjectId(user_id)})


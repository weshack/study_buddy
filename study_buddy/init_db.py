from study_buddy import app

from models import StudySession, User

from pymongo import GEOSPHERE
from mongokit import Connection

connection = Connection(host=app.config['DB_HOST'], port=app.config['DB_PORT'])
connection.register([StudySession, User])
mongo_db = connection.succor
mongo_db.study_sessions.ensure_index([('geo_location', GEOSPHERE)])


from study_buddy import app

from flask.ext.login import UserMixin

from mongokit import Document, Connection

import datetime

class User(Document, UserMixin):
    __database__ = app.config['DB_NAME']
    __collection__ = 'users'

    structure = {
        'date_creation' : datetime.datetime,
        'email' : basestring,
        'password' : basestring,
        'school' : basestring,
        'verified' : bool,
        'name' : {
            'first' : basestring,
            'last' : basestring
        },
        'classes' : [basestring],
        'groups_joined' : [basestring]
    }

    default_values = {
        'date_creation' : datetime.datetime.utcnow
    }

    required_fields = ['email', 'password']

    use_dot_notation = True

    def get_id(self):
        return str(self._id)

class StudySession(Document):
    __database__ = app.config['DB_NAME']
    __collection__ = 'study_sessions'

    structure = {
        'date_creation': datetime.datetime,
        'department': basestring,
        'course_no': basestring,
        'time': datetime.datetime,
        'location': basestring,
        'description': basestring,
        'contact_info': basestring,
        'details': basestring,
        'name': basestring,
        'geo_location' : dict,
        'school' : basestring
        # _id : ObjectId - mongo gives this to you automatically
   }


    required_fields = ['department', 'course_no', 'time', 'location']

    default_values = {
        'date_creation': datetime.datetime.utcnow
    }

    use_dot_notation = True

class Slangs(Document):
    __database__ = 'succor'
    __collection__ = 'similar_names'

    structure = {
        'school' : basestring,
        'department_name': basestring,
        'names' : [basestring]
    }


    use_dot_notation = True

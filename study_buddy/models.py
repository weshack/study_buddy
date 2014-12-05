from flask.ext.login import UserMixin

from mongokit import Document

import datetime

class User(Document, UserMixin):
    __database__ = 'succor'
    __collection__ = 'users'

    structure = {
        'date_creation' : datetime.datetime,
        'email' : basestring,
        'password' : basestring,
        'name' : {
            'first' : basestring,
            'last' : basestring
        },
        'classes' : [basestring]
    }

    default_values = {
        'date_creation' : datetime.datetime.utcnow
    }

    required_fields = ['email', 'password']

    use_dot_notation = True

    def get_id(self):
        return str(self._id)

class StudySession(Document):
    __database__ = 'succor'
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
        'name': basestring
   }


    required_fields = ['department', 'course_no', 'time', 'location']

    default_values = {
        'date_creation': datetime.datetime.utcnow
    }

    use_dot_notation = True

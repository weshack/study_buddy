from flask.ext.wtf import Form
from wtforms import TextField, PasswordField, ValidationError, BooleanField, IntegerField, DateTimeField, validators
from study_buddy import mongo_db
from werkzeug.security import check_password_hash

class EmailForm(Form):
    email = TextField('Email', validators = [validators.Email(), validators.Required()])

class PasswordForm(Form):
    password = PasswordField('Password', validators = [validators.Required()])

class GroupForm(Form):
    name = TextField('Your Name', [
        validators.Required()
    ])
    email = TextField('Contact', [
        validators.Email()
    ])
    department = TextField('Department', [
        validators.Required()
    ])

    course_no = IntegerField('Course Number', [
        validators.Required(),
    ])
    datetime = DateTimeField('Date and time', format="%Y/%m/%d %H:%M")
    where = TextField('Where', [
        validators.Required()
    ])
    assignment = TextField('Assignment', [
        validators.Required()
    ])
    details = TextField('Details')
    all_nighter=BooleanField('All nighter')

    def validate_course_no(self, field):
        if not self.course_no.data < 1000 or len(str(self.course_no.data)) != 3:
            raise validators.ValidationError('Please enter a 3 digit course number')

    def validate_email(self, field):
        if '.edu' not in self.email.data:
            raise validators.ValidationError('Please use a .edu email')

class EditUserForm(Form):
    first_name = TextField('First Name')
    last_name = TextField('Last Name')
    course = TextField('Class')

class LoginForm(Form):
    email = TextField('Email', [
        validators.Required()
    ])

    password = PasswordField('Password')

    remember = BooleanField('Remember me')

    def validate_password(self, field):
        user = self.get_user()

        if user is None:
            raise validators.ValidationError('Email does not exist')

        if not check_password_hash(user.password, self.password.data):
            raise validators.ValidationError('Invalid password')

        if not user.verified:
            raise validators.ValidationError('Not verified yet')

    def get_user(self):
        return mongo_db.users.User.find_one({'email' : self.email.data})


class RegistrationForm(Form):
    email = TextField('Email', [
        validators.Required(),
        validators.length(min=6, max=50),
        validators.Email()
    ])

    def validate_email(self, field):
        if '.edu' not in self.email.data:
            raise validators.ValidationError('Please use a .edu email')

        if mongo_db.users.User.find({'email' : self.email.data}).count() > 0:
            raise validators.ValidationError('Account with that email already exists')

    password = PasswordField('Password', [
        validators.Required(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Confirm Password')
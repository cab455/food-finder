#flask_wtf's base is Python's wtforms library
#object-relational mapper
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, validators as val
from wtforms.fields.html5 import EmailField
from foodfinder.models.user import User
from foodfinder.extensions import db
#from wtforms.validators import InputRequired, Email, Length, Optional



class SignupForm(FlaskForm):
    name = StringField('name', validators=[val.InputRequired(), val.Length(min=2)])
    username = StringField('username', validators=[val.InputRequired(), val.Length(min=6, message="Username must be a minimum of 6 characters")])
    password = PasswordField('password', validators=[val.InputRequired(), val.Length(min=8, message="Password must a minimum of 8 characters")])
    email = EmailField('email', validators=[val.InputRequired(), val.Email()])

    def unique_username(form, field):
        user = db.session.execute(db.select(User).filter_by(username=form.username.data)).scalar()
        if user:
            raise val.ValidationError("That username already exists")

class LoginForm(FlaskForm):
    username = StringField('username', validators=[val.InputRequired(message="Please enter your username")])
    password = PasswordField('password', validators=[val.InputRequired(message="Please enter your password")])

    #WTForms automatically runs validation methods once defined
    def validate_username(form, field):
        user = db.session.execute(db.select(User).filter_by(username=form.username.data)).scalar()
        if not user:
            raise val.ValidationError("That username does not exist")
        elif not user.verify_password(form.password.data) and form.password.data:
            raise val.ValidationError('That password is incorrect')

class PasswordForm(FlaskForm):
    username = StringField('username', validators=[val.InputRequired(message="Please enter your username")])
    old_password = PasswordField('old password', validators=[val.InputRequired()])
    new_password = PasswordField('new password', validators=[val.InputRequired(), val.Length(min=8, message="Password must be a minimum of 8 characters"),
                                                              val.EqualTo('new_password_repeat', message="The passwords must match")])
    new_password_repeat = PasswordField('Re-enter new password', validators=[val.InputRequired(), val.Length(min=8, message="Password must be a minimum of 8 characters")])

    def validate_username(form, field):
        user = db.session.execute(db.select(User).filter_by(username=form.username.data)).scalar()
        if not user:
            raise val.ValidationError("That username does not exist")
        elif not user.verify_password(form.old_password.data) and form.old_password.data:
            raise val.ValidationError('Old password is incorrect')



class SearchForm(FlaskForm):
    protein = StringField('protein', validators=[val.Optional()])
    starches = StringField('starches', validators=[val.Optional()])
    nonstarches = StringField('nonstarches', validators=[val.Optional()])
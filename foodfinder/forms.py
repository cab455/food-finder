#flask_wtf's base is Python's wtforms library
#object-relational mapper
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, validators as val
from wtforms.fields.html5 import EmailField
from foodfinder.models.user import User
from foodfinder.extensions import db
#from wtforms.validators import InputRequired, Email, Length, Optional


class LoginForm(FlaskForm):
    username = StringField('username', validators=[val.InputRequired()])
    password = PasswordField('password', validators=[val.InputRequired()])

    #WTForms automatically runs validation methods once defined
    def validate_username(form, field):
        user = db.session.execute(db.select(User).filter_by(username=form.username.data)).scalar_one()
        if not user:
            raise val.ValidationError("That username does not exist")
        elif not user.verify_password(form.password.data):
            raise val.ValidationError('That password is incorrect')


class SignupForm(FlaskForm):
    name = StringField('name', validators=[val.InputRequired(), val.Length(min=2)])
    username = StringField('username', validators=[val.InputRequired(), val.Length(min=6)])
    password = PasswordField('password', validators=[val.InputRequired(), val.Length(min=8)])
    email = EmailField('email', validators=[val.InputRequired(), val.Email()])

    def unique_username(form, field):
        user = db.session.execute(db.select(User).filter_by(username=form.username.data)).scalar_one()
        if user:
            raise val.ValidationError("That username already exists")


class SearchForm(FlaskForm):
    protein = StringField('protein', validators=[val.Optional()])
    starches = StringField('starches', validators=[val.Optional()])
    nonstarches = StringField('nonstarches', validators=[val.Optional()])
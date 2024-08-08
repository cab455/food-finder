#flask_wtf's base is Python's wtforms library
#object-relational mapper
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, validators as val
from wtforms.fields.html5 import EmailField
#from wtforms.validators import InputRequired, Email, Length, Optional


class LoginForm(FlaskForm):
    username = StringField('username', validators=[val.InputRequired()])
    password = PasswordField('password', validators=[val.InputRequired()])


class SignupForm(FlaskForm):
    name = StringField('name', validators=[val.InputRequired(), val.Length(min=2)])
    username = StringField('username', validators=[val.InputRequired(), val.Length(min=8)])
    password = PasswordField('password', validators=[val.InputRequired(), val.Length(min=8)])
    email = EmailField('email', validators=[val.InputRequired(), val.Email()])
    

class SearchForm(FlaskForm):
    protein = StringField('protein', validators=[val.Optional()])
    starches = StringField('starches', validators=[val.Optional()])
    nonstarches = StringField('nonstarches', validators=[val.Optional()])
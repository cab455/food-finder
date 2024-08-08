from .__init__ import db

#Allows for user session mgmt (login/logout)
#API for user authentication
from flask_login import LoginManager, UserMixin, current_user, logout_user, login_required
import datetime as datetime
from werkzeug.security import generate_password_hash, check_password_hash

#creating association table for roles/users
roles_users = db.Table('roles_users', 
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('role_id', db.Integer, db.ForeignKey('role.id')))


class User(db.Model, UserMixin):
    __tablename = 'User'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    active = db.Column(db.Boolean)
    roles = db.relationship('Role', secondary=roles_users, backref=db.backref('users', lazy='dynamic'))
    #favorites = db.relationship('Favorite', backref='user', lazy=True)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_hash_password(self, hashed_password, password):
        return check_password_hash(hashed_password, password)

    #def is_authenticated(self):
    #    return False 
    
    #def is_anonymous(self):
    #    return True
    
    #def is_active(self):
    #    return False

    def __repr__(self):
        return '<User %r>' % self.username
    

#e.g., admin, regular user, etc
#many-to-many relationship between user and role
class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40))
    description = db.Column(db.String(255))


class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    recipe_name = db.Column(db.String(50), nullable=False)
    ingredients = db.Column(db.Text, nullable=False)
    url = db.Column(db.String(100), nullable=False)
    #favorites = db.relationship('Favorite', backref='recipe', lazy=True)
    #cook_date = db.Column(db.String(10), nullable=False)

    def __repr__(self):
        return '<Recipe %r>' % self.recipe_name

class Favorite(db.Model):
    __tablename__ = 'Favorite'
    id = db.Column(db.Integer, primary_key=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey(Recipe.id), primary_key=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id), primary_key=True, nullable=False)

    #def __repr__(self):
    #    return '<Favorite %r>' % self.id

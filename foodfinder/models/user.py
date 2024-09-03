from foodfinder.extensions import db
#Allows for user session mgmt (login/logout)
#API for user authentication
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from foodfinder.extensions import login_manager


#Model for User table in db
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    #active = db.Column(db.Boolean)
    #roles = db.relationship('Role', secondary=roles_users, backref=db.backref('users', lazy='dynamic'))
    #favorites = db.relationship('Favorite', backref='user', lazy=True)

    def __init__(self, name, username, password, email):
        self.name = name
        self.username = username
        self.password = self.set_password(password)
        self.email = email
        
    #Hashes user submitted password
    def set_password(self, password):
        return generate_password_hash(password)

    #Compares user inputted password with password stored in db
    def verify_password(self, input_password):
        return check_password_hash(self.password, input_password)

    def __repr__(self):
        return '<User %r>' % self.username
    
@login_manager.user_loader
def load_user(user_id):
    return db.get_or_404(User, user_id)
    
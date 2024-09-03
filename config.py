import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    #prevents cross-site request forgery
    #os.urandom(24).hex() to generate random secret key value
    SECRET_KEY = os.urandom(24).hex() #os.environ.get('SECRET_KEY')

    #need to add a salt for the hash_password
    SECURITY_PASSWORD_SALT = os.urandom(16).hex() #os.environ.get('SECURITY_PASSWORD_SALT')

    #configure and setup db location
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI')\
        or 'sqlite:///' + os.path.join(basedir, 'foodfinder.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
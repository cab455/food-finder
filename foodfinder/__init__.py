#Application with divisional splitting

import pandas as pd
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

#API for user authentication
#deprecated
#from flask_security import Security, SQLAlchemyUserDatastore, login_required, UserMixin, RoleMixin
#for hashing user passwords
#from flask_security.utils import hash_password, verify_password


#ModelClass.query.get() -> retrieve item using primary key
#get() vs get_or_404(): former returns None while latter returns 404 
#Not Found HTTP response
#name attribute: used for POST methods; e.g., request.form['name]
#id attribute: used for CSS/JS
#Flash-Security: authentication API good for dbs

#instantiating the db with the instantiated flask app
db = SQLAlchemy()

def create_app():
    #instantiate flask app object
    app = Flask(__name__, instance_relative_config=False)

    #configure and setup location of db
    app.config['SECRET_KEY'] = 'tisasecret' #prevents cross-site request forgery
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///foodfinder.db'
    #need to add a salt for the hash_password
    #app.config['SECURITY_PASSWORD_SALT'] = 'tissecretsalt'

    db.init_app(app)

    login_manager = LoginManager(app)
    login_manager.login_view = 'login_bp.login'
    login_manager.init_app(app)
    
    #import User class to use in load_user function
    from .models import User
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    #read the csv containing the recipes into a dataframe for future ref
    recipes = pd.read_csv('recipes.csv')
    recipes = recipes[['recipe_name', 'ingredients', 'url']].dropna()


    with app.app_context():
        #create db, populate with recipe data from imported csv
        db.create_all()
        recipes.to_sql(name='recipe', con=db.engine, if_exists='replace', index=True, index_label="ID")

        #import classes for views
        from .favs import favs
        from .home import home
        from .login import login
        from .recipes import recipes
        from .signup import signup

        #register blueprint for each view
        app.register_blueprint(favs.favs_bp)
        app.register_blueprint(home.home_bp)
        app.register_blueprint(login.login_bp)
        app.register_blueprint(recipes.recipes_bp)
        app.register_blueprint(signup.signup_bp)

        return app
    


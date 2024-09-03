#Application with divisional splitting

from flask import Flask
from config import Config
from foodfinder.extensions import db, login_manager

import pandas as pd
#from flask_login import LoginManager

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



#Flask application factory function
def create_app(config_class=Config):
    #instantiate flask app object
    app = Flask(__name__)
    #bcrypt = Bcrypt()
    #Import config values to configure app
    app.config.from_object(config_class)

    db.init_app(app)
    login_manager.init_app(app)
    
    #import User class to use in load_user function
    #from foodfinder.models.old import User
    #@login_manager.user_loader
    #def load_user(user_id):
    #    return db.session.execute(db.select(User).get(int(user_id))).scalar()
    
    #Create db tables and populate Recipes table with data from csv
    with app.app_context():
        #import module for db models before creating tables in db
        from foodfinder.models.recipe import Recipe, Favorite
        from foodfinder.models.user import User
        #create db, populate with recipe data from imported csv
        db.create_all()
        #read the csv containing the recipes into a dataframe for future ref
        recipes = pd.read_csv('recipes.csv')
        recipes = recipes[['recipe_name', 'ingredients', 'url']].dropna()
        recipes.to_sql(name='recipe', con=db.engine, if_exists='replace', index=True, index_label="ID")

    #import classes for blueprints
    from foodfinder.login import login_bp
    from foodfinder.signup import signup_bp
    from foodfinder.home import home_bp
    from foodfinder.recipes import recipes_bp
    from foodfinder.favs import favs_bp
        
    #register blueprints
    app.register_blueprint(login_bp)
    app.register_blueprint(signup_bp)
    app.register_blueprint(home_bp)
    app.register_blueprint(recipes_bp)
    app.register_blueprint(favs_bp)
        

    return app
    


from flask import Flask, render_template, url_for, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy
import pandas as pd
import datetime as datetime

#ModelClass.query.get() -> retrieve item using primary key
#get() vs get_or_404(): former returns None while latter returns 404 
#Not Found HTTP response
#name attribute: used for POST methods; e.g., request.form['name]
#id attribute: used for CSS/JS


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///foodfinder.db'
db = SQLAlchemy(app)

#read the csv containing the recipes into a dataframe for future ref
recipes = pd.read_csv('recipes.csv')
recipes = recipes[['recipe_name', 'ingredients', 'url']].dropna()


class User(db.Model):
    __tablename = 'User'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100))
    favorites = db.relationship('Favorite', backref='user', lazy=True)

    def __repr__(self):
        return '<User %r>' % self.username

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
    #    return '<Favorite %r>' % self.

with app.app_context():
    db.create_all()
    recipes.to_sql(name='recipe', con=db.engine, if_exists='replace', index=True, index_label="ID")

#Login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        msgs =[]
        un = request.form['username']
        pw = request.form['password']
        user_lookup = User.query.filter_by(username=un).first()
        if not user_lookup:
            msg = "The username does not exist. Please try again"
            msgs.append(msg)
            return render_template('login.html', msgs=msgs)
        else:
            if user_lookup.password != pw:
                msg = "The password is incorrect. Please try again."
                msgs.append(msg)
                return render_template('login.html', msgs=msgs)
            else:
                return redirect('/home')
    else:
        return render_template('login.html')


#Signup method/html
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        msgs = []
        nm = request.form['name']
        un = request.form['username']
        pw = request.form['password']
        em = request.form['email']
        temp_user = User.query.filter_by(email=em).first()
        if temp_user:
            msg = "A user with that email already exists. Please log in."
            msgs.append(msg)
            return render_template('signup.html', msgs=msgs)
        else:
            if len(pw) < 8:
                msg = "Password must be at least 8 characters"
                msgs.append(msg)
            temp_user = User.query.filter_by(username=un).first()
            if temp_user:
                msg = "Username is taken. Please choose a different one."
                msgs.append(msg)
            if len(msgs) == 0:
                msg = "You've successfully signed up! Login below."
                msgs.append(msg)
                new_user = User(name=nm, username=un, password=pw, email=em)
                try:
                    db.session.add(new_user)
                    db.session.commit()
                    return redirect('/login')
                except:
                    'There was an issue siging up that user'
            else:
                return render_template('signup.html', msgs=msgs)
    else:
        return render_template('signup.html')


#Accessing the url "http://127.0.0.1/" triggers the "home" function
#which renders the "home" view (method=GET)
@app.route('/home', methods=['GET'])
def home():
    return render_template('home.html')



#Submitting the form at the url "http://127.0.0.1/" triggers
#the "recipes" function, which renders the "recipes" view (method=POST)
@app.route('/recipes', methods=['POST'])
def recipes():
    if request.method == 'POST':
        protein = str(request.form['protein'])
        starch = str(request.form['starch'])
        nonstarch = str(request.form['non-starch'])
        if protein == "" and starch == "" and nonstarch == "":
            matches = Recipe.query.order_by(Recipe.recipe_name).all()
            recipe_matches = [r for r in matches]
        else:
            matches = Recipe.query.filter(Recipe.ingredients.contains(protein), Recipe.ingredients.contains(starch),
                                                  Recipe.ingredients.contains(nonstarch)).all()
            recipe_matches = [r for r in matches]
        return render_template('recipes.html', recipe_matches=recipe_matches)



#Accessing the url "http://127.0.0.1/favs" triggers the "favs"
#function which renders the "favs" view (method=GET)
#Submitting the "Add to favorites" form on the "recipes" view at the
#url "http://127.0.0.1/" triggers the "favs" function, which renders
#the "recipes" view (method=POST); uses the id of the recipe that was
#favorited to query the Recipes table for the recipe id, then uses that
#along with the user id to add a record to the Favorites table with the
#recipe id and user id as foreign keys
@app.route('/favs', methods=['POST', 'GET'])
def favs():
    #click on "Favorites" link on home page
    if request.method == 'GET':
        favorites = [] #Recipes.query.order_by(Recipes.recipe_name).all()
        return render_template("favs.html", favorites=favorites)
    #click on "Add to Favorites" button on recipes page
    elif request.method == 'POST':
        new_fav = []
        new_fav_id = int(request.form['row']) #Recipes.query.get(id).id
        temp = Recipe.query.get(new_fav_id)
        new_fav.append(temp)
        return render_template('favs.html', favorites=new_fav)






if __name__ == "__main__":
    #debug=True: to be able to make/see html changes in real time
    app.run(debug=True)
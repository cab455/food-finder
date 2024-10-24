from foodfinder.extensions import db
from .user import User

import pandas as pd
import csv


#class for Recipe table in db
class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    recipe_name = db.Column(db.String(50), nullable=False)
    ingredients = db.Column(db.Text, nullable=False)
    url = db.Column(db.String(100), nullable=False)
    favorites = db.relationship('Favorite', backref='recipe', lazy=True)
    #cook_date = db.Column(db.String(10), nullable=False)

    def __init__(self, name, items, url):
        self.recipe_name = name
        self.ingredients = items
        self.url = url

    def __repr__(self):
        return '<Recipe %r>' % self.recipe_name
    

#class for Favorites table in db
class Favorite(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    recipe_name = db.Column(db.String(50), nullable=False)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __init__(self, name, rec_id, us_id):
        self.recipe_name = name
        self.recipe_id = rec_id
        self.user_id = us_id

    def __repr__(self):
        return '<Favorite %r>' % self.recipe_name
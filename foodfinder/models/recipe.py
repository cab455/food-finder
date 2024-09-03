from foodfinder.extensions import db
from .user import User


#class for Recipe table in db
class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    recipe_name = db.Column(db.String(50), nullable=False)
    ingredients = db.Column(db.Text, nullable=False)
    url = db.Column(db.String(100), nullable=False)
    #favorites = db.relationship('Favorite', backref='recipe', lazy=True)
    #cook_date = db.Column(db.String(10), nullable=False)

    def __repr__(self):
        return '<Recipe %r>' % self.recipe_name
    

#class for Favorites table in db
class Favorite(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    recipe_name = db.Column(db.String(50), db.ForeignKey(Recipe.recipe_name), nullable=False)
    recipe_id = db.Column(db.Integer, db.ForeignKey(Recipe.id), primary_key=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id), primary_key=True, nullable=False)

    def __repr__(self):
        return '<Favorite %r>' % self.recipe_name
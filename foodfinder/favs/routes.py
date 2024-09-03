from flask import Blueprint, render_template, request
from flask_login import login_required

from foodfinder.favs import favs_bp
from foodfinder.models.recipe import Recipe

#Accessing the url "http://127.0.0.1/favs" triggers the "favs"
#function which renders the "favs" view (method=GET)
#Submitting the "Add to favorites" form on the "recipes" view at the
#url "http://127.0.0.1/" triggers the "favs" function, which renders
#the "recipes" view (method=POST); uses the id of the recipe that was
#favorited to query the Recipes table for the recipe id, then uses that
#along with the user id to add a record to the Favorites table with the
#recipe id and user id as foreign keys
@favs_bp.route('/favs', methods=['POST', 'GET'])
@login_required
def favs():
    #click on "Favorites" link on home page
    if request.method == 'GET':
        favorites = [] #Recipes.query.order_by(Recipes.recipe_name).all()
        return render_template("favs/index.html", favorites=favorites)
    #click on "Add to Favorites" button on recipes page
    elif request.method == 'POST':
        new_fav = []
        new_fav_id = int(request.form['row']) #Recipes.query.get(id).id
        temp = Recipe.query.get(new_fav_id)
        new_fav.append(temp)
        return render_template('favs/index.html', favorites=new_fav)
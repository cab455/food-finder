from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user

from foodfinder.favs import favs_bp
from foodfinder.models.user import User
from foodfinder.models.recipe import Recipe, Favorite
from foodfinder.extensions import db

#Accessing the url "http://127.0.0.1/favs" triggers the "favs"
#function which renders the "favs" view (method=GET)
#Submitting the "Add to favorites" form on the "recipes" view at the
#url "http://127.0.0.1/" triggers the "favs" function, which renders
#the "recipes" view (method=POST); uses the id of the recipe that was
#favorited to query the Recipes table for the recipe id, then uses that
#along with the user id to add a record to the Favorites table with the
#recipe id and user id as foreign keys
@favs_bp.route('/favs', methods=['GET', 'POST'])
@login_required
def favs():
    #click on "Favorites" link on home page
    if request.method == 'GET':
        favorites = Favorite.query.filter_by(user_id=current_user.id).order_by(Favorite.recipe_name).all()
        return render_template("favs/index.html", favorites=favorites)
    #click on "Add to Favorites" button on recipes page
    elif request.method == 'POST':
        new_fav_id = int(request.form['row']) 
        new_fav_obj = Recipe.query.filter(Recipe.id == new_fav_id).first() #db.session.execute(db.select(Recipe).filter_by(recipe_id=new_fav_id))
        fav = Favorite(new_fav_obj.recipe_name, new_fav_id, current_user.id)
        try:
            db.session.add(fav)
            db.session.commit()
            flash("Recipe successfully added to favorites")
            return redirect(url_for('favs_bp.favs'))
        except Exception as e:
            print(e)
            return render_template('favs/index.html', error=e)
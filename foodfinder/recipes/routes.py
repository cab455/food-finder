from flask import request, render_template, redirect
from flask_login import login_required, current_user
from flask import current_app as app

from foodfinder.recipes import recipes_bp
from foodfinder.models.recipe import Recipe, Favorite
from foodfinder.extensions import db

#Submitting the form at the url "http://127.0.0.1/" triggers
#the "recipes" function, which renders the "recipes" view (method=POST)
@recipes_bp.route('/recipes', methods=['POST'])
@login_required
def recipes():
    if request.method == 'POST':
        protein = str(request.form['protein'])
        starch = str(request.form['starches'])
        nonstarch = str(request.form['nonstarches'])
        recipe_matches = []
        if protein == "" and starch == "" and nonstarch == "":
            recipe_matches = Recipe.query.order_by(Recipe.recipe_name).all()
        else:
            recipe_matches = Recipe.query.filter(Recipe.ingredients.contains(protein), Recipe.ingredients.contains(starch),
                                                  Recipe.ingredients.contains(nonstarch)).all()
        recipe_in_favs = []
        marked_recipe_matches = []
        for r in recipe_matches:
            if Favorite.query.filter_by(recipe_id=r.id, user_id=current_user.id).all():
                recipe_in_favs.append(1)
            else:
                recipe_in_favs.append(0)
        marked_recipe_matches = list(zip(recipe_in_favs, recipe_matches))
        return render_template('recipes/index.html', recipe_matches=marked_recipe_matches)
from flask import request, render_template
from flask_login import login_required
from flask import current_app as app

from foodfinder.recipes import recipes_bp
from foodfinder.models.recipe import Recipe

#Submitting the form at the url "http://127.0.0.1/" triggers
#the "recipes" function, which renders the "recipes" view (method=POST)
@recipes_bp.route('/recipes', methods=['POST'])
@login_required
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
        return render_template('recipes/index.html', recipe_matches=recipe_matches)
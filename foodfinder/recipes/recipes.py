from flask import Blueprint, request
from flask_login import login_required
from flask import current_app as app

recipes_bp = Blueprint(
    'recipes_bp', __name__,
    template_folder='templates',
    static_folder='static'
)

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
        return render_template('recipes.html', recipe_matches=recipe_matches)
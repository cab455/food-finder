from flask import Blueprint

recipes_bp = Blueprint(
    'recipes_bp', __name__,
    template_folder='templates',
    static_folder='static'
)

from foodfinder.recipes import routes
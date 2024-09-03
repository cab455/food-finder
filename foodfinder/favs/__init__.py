from flask import Blueprint

favs_bp = Blueprint(
    'favs_bp', __name__,
    template_folder='templates',
    static_folder='static'
)

from foodfinder.favs import routes
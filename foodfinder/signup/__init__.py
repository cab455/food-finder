from flask import Blueprint

signup_bp = Blueprint(
    'signup_bp', __name__,
    template_folder='templates',
    static_folder='static'
)

from foodfinder.signup import routes
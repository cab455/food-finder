from flask import Blueprint

#Configure home Blueprint
#dunder name set to 'home_bp'
#template_folder and static_folder point to
#templates ant static folders in home directory,
#respectively
home_bp = Blueprint(
    'home_bp', __name__,
    template_folder='templates',
    static_folder='static'
)

from foodfinder.home import routes
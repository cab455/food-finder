from flask import Blueprint, render_template
from flask import current_app as app
from foodfinder.forms import SearchForm

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


#Accessing the url "http://127.0.0.1/" triggers the "home" function
#which renders the "home" view (method=GET)
@home_bp.route('/home', methods=['GET'])
#@login_required
def home():
    form = SearchForm()
    if form.validate_on_submit():
        print("Search")
    return render_template('home.html', form=form)

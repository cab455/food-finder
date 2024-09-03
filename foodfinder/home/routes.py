from flask import render_template
from flask import current_app as app
from foodfinder.forms import SearchForm
from flask_login import login_required

from foodfinder.home import home_bp


#Accessing the url "http://127.0.0.1/" triggers the "home" function
#which renders the "home" view (method=GET)
@home_bp.route('/home', methods=['GET'])
@login_required
def home():
    form = SearchForm()
    #if form.validate_on_submit():
    #    print("Search")
    return render_template('home/index.html', form=form)

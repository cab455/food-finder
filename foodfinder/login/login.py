from flask import Blueprint, render_template, request, redirect, url_for
from flask import current_app as app
from foodfinder.models import User

#Configure home Blueprint
#dunder name set to 'home_bp'
#template_folder and static_folder point to
#templates ant static folders in home directory,
#respectively
login_bp = Blueprint(
    'login_bp', __name__,
    template_folder='templates',
    static_folder='static'
)


#Login page
@login_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        #if current_user.is_authenticated:
        #    return redirect(url_for('home'))
        msgs =[]
        un = request.form['username']
        pw = request.form['password']
        user_lookup = User.query.filter_by(username=un).first()
        if not user_lookup:
            msg = "The username does not exist. Please try again"
            msgs.append(msg)
            return render_template('login.html', msgs=msgs)
        else:
            #if verify_password(pw, user_lookup.password):
            if user_lookup.password == pw:
                return redirect(url_for('home'))
            else:                
                msg = "The password is incorrect. Please try again."
                msgs.append(msg)
                return render_template('login.html', msgs=msgs)
    else:
        return render_template('login.html')
    
#logout route
@login_bp.route('/logout', methods=['GET'])
#@login_required
def logout():
    if request.method == 'GET':
        return redirect(url_for('login')) 
from flask import render_template, redirect, url_for, flash
#from flask import current_app as app
from flask_login import current_user, login_user, login_required, logout_user
from foodfinder.forms import LoginForm, PasswordForm
from foodfinder.extensions import db

from foodfinder.login import login_bp
from foodfinder.models.user import User


#Login route
@login_bp.route('/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        curr_user = db.session.execute(db.select(User).filter_by(username=form.username.data)).scalar_one()
        login_user(curr_user)
        return redirect(url_for('home_bp.home'))
    return render_template('login/index.html', form=form)

#Forgot password route
@login_bp.route('/forgotpassword', methods=['GET', 'POST'])
def forgotpassword():
    form = PasswordForm()
    if form.validate_on_submit():
        curr_user = db.session.execute(db.select(User).filter_by(username=form.username.data)).scalar_one()
        curr_user.password = curr_user.set_password(form.new_password.data)
        try:
            db.session.commit()
            flash("Password change was sucessful! Login below.")
            return redirect(url_for('login_bp.login'))
        except:
            flash("Password change failed. Please try again")
            return render_template('forgotpassword/index.html', form=form)
    return render_template('forgotpassword/index.html', form=form)
    
#logout route
@login_bp.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login_bp.login')) 
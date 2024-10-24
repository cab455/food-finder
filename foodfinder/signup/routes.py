from flask import render_template, request, redirect, url_for, flash
from flask import current_app as app
from foodfinder.forms import SignupForm
from foodfinder.models.user import User
from foodfinder.extensions import db

from foodfinder.signup import signup_bp


#Signup route
@signup_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        #hashed_password = bcrypt.generate_password_hash(form.password.data)
        #new_user = User(form.name.data, form.username.data, hashed_password, form.email.data)
        new_user = User(form.name.data, form.username.data, form.password.data, form.email.data)
        try:
            db.session.add(new_user)
            db.session.commit()
            flash("Sign up was successful! Log in below.")
            return redirect(url_for('login_bp.login'))
        except Exception as e:
            print(e)
            return render_template('signup/index.html', form=form)
    return render_template('signup/index.html', form=form)


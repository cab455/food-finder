from flask import render_template, request, redirect, url_for, flash
from flask import current_app as app
from foodfinder.forms import SignupForm
from foodfinder.models.user import User
from foodfinder.__init__ import db

from foodfinder.signup import signup_bp


#Signup route
@signup_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        #hashed_password = bcrypt.generate_password_hash(form.password.data)
        #new_user = User(form.name.data, form.username.data, hashed_password, form.email.data)
        new_user = User(form.name.data, form.username.data, form.password.data, form.email.data, )
        try:
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('login_bp.login'))
        except Exception as e:
            print(e)
            return redirect(url_for('signup_bp.signup'))
    return render_template('signup/index.html', form=form)


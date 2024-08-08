from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask import current_app as app
from foodfinder.forms import SignupForm
from foodfinder.models import User
from foodfinder.__init__ import db

signup_bp = Blueprint(
    'signup_bp', __name__,
    template_folder='templates',
    static_folder='static'
)

#Signup method/html
@signup_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        username = form.username.data
        password = form.password.data #need to hash password with bcrypt
        new_user = User(name, username, email)
        new_user.set_password(password)
        try:
            db.session.add(new_user)
            db.commit()
            return redirect(url_for('login'))
        except:
            flash('There was an error signing up that user. Please try again.')
            return redirect(url_for('signup'))
    return render_template('signup.html', form=form)
    #if request.method == 'POST':
        #msgs = []
        #nm = request.form['name']
        #un = request.form['username']
        #pw = request.form['password']
        #em = request.form['email']
        #temp_user = User.query.filter_by(email=em).first()
        #if temp_user:
        #    msg = "A user with that email already exists. Please log in."
        #    msgs.append(msg)
        #    #flash('That email address already exists. Please login.')
        #    #return redirect(url_for('signup'))
        #    return render_template('signup.html', msgs=msgs)
        #else:
        #    if len(pw) < 8:
        #        msg = "Password must be at least 8 characters"
        #        msgs.append(msg)
        #    temp_user = User.query.filter_by(username=un).first()
        #    if temp_user:
        #        msg = "Username is taken. Please choose a different one."
        #        msgs.append(msg)
        #    if len(msgs) == 0:
        #        msg = "You've successfully signed up! Login below."
        #        msgs.append(msg)
        #        new_user = User(name=nm, username=un, password=pw, email=em)
        #        #user_datastore.create_user(name=nm, username=un, password=hash_password(pw), email=em)
        #        try:
        #            db.session.add(new_user)
        #            db.session.commit()
        #            #return redirect(url_for('home'))
        #            return redirect(url_for('/login'))
        #        except:
        #            'There was an issue siging up that user'
        #            return redirect('/signup')
        #    else:
        #        return render_template('signup.html', msgs=msgs)
    #else:
        #return render_template('signup.html')

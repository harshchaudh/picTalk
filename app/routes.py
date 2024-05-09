from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user

from sqlalchemy.exc import IntegrityError

from app.model import db, USER
from app.forms import CreateContentForm

from app.utilities import UsernameValidation, PasswordValidation

picTalk_bp = Blueprint('picTalk', __name__)

@picTalk_bp.route('/')
def home():
    return render_template('home.html', current_user=current_user)

@picTalk_bp.route('/gallery')
def gallery():
    return render_template('gallery.html')

@picTalk_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == "POST":
        signup_username = request.form['signup-username'].lower()
        signup_psw = request.form['signup-psw']
        signup_pswConfirm = request.form['signup-pswConfirm']

        if signup_psw != signup_pswConfirm:
            flash('Passwords do not match.', 'warning')
            return render_template('signup.html')
        
        if UsernameValidation.validate(signup_username):
            flash('Username does not meet criteria.', 'warning')
            return render_template('signup.html')
        
        if PasswordValidation.validate(signup_psw):
            flash('Password does not meet criteria.', 'warning')
            return render_template('signup.html')

        existing_user = USER.query.filter_by(username=signup_username).first()
        if existing_user:
            flash('Username is already in use.', 'danger')
            return render_template('signup.html')

        # Only pass the username and unhashed password
        new_user = USER(username=signup_username, password=signup_psw)
        db.session.add(new_user)
        db.session.commit()
        flash('Account created successfully! Please log in.', 'success')
        return redirect(url_for('picTalk.login'))

    return render_template("signup.html")

@picTalk_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        login_username = request.form['login-username'].lower()
        login_password = request.form['login-password']
        
        user = USER.query.filter_by(username=login_username).first()
        if user and user.check_password(login_password):
            login_user(user)
            flash('Logged in successfully.', 'success')
            return redirect(url_for('picTalk.home'))
        else:
            flash('Invalid username or password.', 'warning')

    return render_template('login.html')

@picTalk_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('picTalk.home'))

@picTalk_bp.route('/profile')
@login_required
def profile():
    return render_template('profile.html', user=current_user)

@picTalk_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    form = CreateContentForm()
    if form.validate_on_submit():
        # form handling logic
        flash('Post created successfully!', 'success')
        return redirect(url_for('picTalk.home'))
    return render_template('create_post.html', form=form)

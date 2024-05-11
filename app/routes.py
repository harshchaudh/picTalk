from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user

from sqlalchemy.exc import IntegrityError

import base64

from app.model import db, USER, SUBMISSION, TAGS
from app.forms import CreateContentForm

from app.utilities import UsernameValidation, PasswordValidation, organiseColumnImages

picTalk_bp = Blueprint('picTalk', __name__)

@picTalk_bp.route('/')
def home():
    return render_template('home.html', current_user=current_user)

@picTalk_bp.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == "POST":
        query = request.form['search'].lower()
        
        users = USER.query.filter(USER.username.like(f"%{query}%")).all()
        tags = TAGS.query.filter(TAGS.tag.like(f"%{query}%")).all()
        return render_template('search.html', users = users, tags = tags, query=query)

    return render_template('search.html')

@picTalk_bp.route('/gallery')
def gallery():
    images = SUBMISSION.query.order_by(SUBMISSION.created_at).all()
    base64_images = [base64.b64encode(image.image).decode("utf-8") for image in images] 
    base64_images.reverse()

    base64_images_firstColumn = organiseColumnImages(base64_images)[0]
    base64_images_secondColumn = organiseColumnImages(base64_images)[1]
    base64_images_thirdColumn = organiseColumnImages(base64_images)[2]

    return render_template('gallery.html', user=current_user, 
                           images_firstColumn = base64_images_firstColumn, 
                           images_secondColumn = base64_images_secondColumn, 
                           images_thirdColumn = base64_images_thirdColumn)

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
    submission_count = SUBMISSION.query.filter_by(username_id=current_user.username_id).count()
    
    images = SUBMISSION.query.filter_by(username_id=current_user.username_id).order_by(SUBMISSION.created_at).all()
    base64_images = [base64.b64encode(image.image).decode("utf-8") for image in images] 
    base64_images.reverse()

    base64_images_firstColumn = organiseColumnImages(base64_images)[0]
    base64_images_secondColumn = organiseColumnImages(base64_images)[1]
    base64_images_thirdColumn = organiseColumnImages(base64_images)[2]

    return render_template('profile.html', user=current_user, 
                           submission_count=submission_count, 
                           images_firstColumn = base64_images_firstColumn, 
                           images_secondColumn = base64_images_secondColumn, 
                           images_thirdColumn = base64_images_thirdColumn)

# User page for other users, not current logged in user. Had to navigate around '@login_required'. 
@picTalk_bp.route('/user/<int:username_id>')
def user_page(username_id):
    user = USER.query.get(username_id)
    
    if user:
        submission_count = SUBMISSION.query.filter_by(username_id=username_id).count()

        images = SUBMISSION.query.filter_by(username_id=username_id).order_by(SUBMISSION.created_at).all()
        base64_images = [base64.b64encode(image.image).decode("utf-8") for image in images] 
        base64_images.reverse()

        base64_images_firstColumn = organiseColumnImages(base64_images)[0]
        base64_images_secondColumn = organiseColumnImages(base64_images)[1]
        base64_images_thirdColumn = organiseColumnImages(base64_images)[2]

        return render_template('user_page.html', user=user, 
                            submission_count=submission_count, 
                            images_firstColumn = base64_images_firstColumn, 
                            images_secondColumn = base64_images_secondColumn, 
                            images_thirdColumn = base64_images_thirdColumn)
    else:
        flash('Error - user does not exist.', 'danger')
        return redirect(url_for('picTalk.home'))

@picTalk_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    form = CreateContentForm()
    if form.validate_on_submit():
        image_file = form.image.data
        image_data = image_file.read()

        new_submission = SUBMISSION(image = image_data,
                                    caption = form.caption_text.data,
                                    username_id = current_user.username_id)
        try:
            db.session.add(new_submission)
            db.session.commit()
            flash('Post created successfully!', 'success')
            return redirect(url_for('picTalk.home'))
        except:
            flash('Post failed to submit.', 'danger')
            render_template('create_post.html')

    return render_template('create_post.html', form=form)

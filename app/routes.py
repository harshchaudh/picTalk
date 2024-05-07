from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_user, logout_user, login_required, current_user

from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash

from sqlalchemy.exc import IntegrityError

from app.model import db, USER, SUBMISSION
from app.forms import CreateContentForm
from app.utilities import username_validation, password_validation

picTalk_bp = Blueprint('picTalk', __name__)

# Route for the home page.
@picTalk_bp.route('/')
def home():
    return render_template('home.html', current_user=current_user)

# Route for the gallery page.
@picTalk_bp.route('/gallery')
def gallery():
    return render_template('gallery.html')

# Route for the sign up page
@picTalk_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == "POST":
        signup_username = request.form['signup-username']
        signup_psw = request.form['signup-psw']
        signup_pswConfirm = request.form['signup-pswConfirm']

        if signup_psw != signup_pswConfirm:
            return render_template('signup.html', error = 'Passwords do not match')
        
        existing_user = USER.query.filter_by(username = signup_username).first()
        if existing_user:
            return render_template('signup.html', error = 'Username is already in use')

        if not username_validation(signup_username):
            return render_template('signup.html', error = 'Username does not meet criteria')
        
        if not password_validation(signup_psw):
            return render_template('signup.html', error = "Password does not meet criteria")
        
        signup_username = signup_username.lower()

        try: 
            # Create a new user
            new_user = USER(username = signup_username, password = generate_password_hash(signup_psw, method='pbkdf2:sha256'))
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('picTalk.login'))
        except IntegrityError:
            return render_template('signup.html', error='Error, unable to create an account')
        except Exception as e:
            return render_template('signup.html', error=f'Error: {str(e)}')
    else:
        return render_template("signup.html")

# Route for the login page
@picTalk_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        login_username = request.form['login-username']
        login_password = request.form['login-password']

        login_username = login_username.lower()
        user = USER.query.filter_by(username = login_username).first()
        
        if user and check_password_hash(user.password, login_password):
            login_user(user)
            return redirect(url_for('picTalk.home'))
        else:
            return render_template('login.html', error = 'Invalid username or password')
    
    return render_template('login.html')

@picTalk_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('picTalk.home'))

@picTalk_bp.route('/profile')
@login_required
def profile():
    return render_template('profile.html')

# Route for the creating a post page
@picTalk_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    form = CreateContentForm()
    if form.validate_on_submit():
        image_data = form.image.data.read()
        caption_text = form.caption_text.data
        tags = form.tag_text.data.split(',')

        try: 
            # Create a new submission
            submission = SUBMISSION(image = image_data, caption = caption_text)
            db.session.add(submission)
            db.session.commit()
            return redirect(url_for('picTalk.home'))
        except IntegrityError:
            return render_template('create_post.html', error='Error, unable to make a submission')
        except Exception as e:
            return render_template('create_post.html', error=f'Error: {str(e)}')
            

    return render_template('create_post.html', form = form)


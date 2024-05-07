from flask import Blueprint, render_template, request, redirect, url_for
from app.forms import CreateContentForm

from sqlalchemy.exc import IntegrityError

from app.model import db, USER

picTalk_bp = Blueprint('picTalk', __name__)

# Route for the home page.
@picTalk_bp.route('/')
def home():
    return render_template('home.html')

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
    
        try: 
            # Create a new user
            new_user = USER(username = signup_username, password = signup_psw)
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

        user = USER.query.filter_by(username = login_username).first()
        if user:
            if user.password == login_password:
                return redirect(url_for('picTalk.home'))
            else:
                return render_template('login.html', error = 'Invalid username or password')
        else:
            return render_template('login.html', error = 'Invalid username or password')
    
    return render_template('login.html')

# Route for the creating a post page
@picTalk_bp.route('/create', methods=['GET', 'POST'])
def create():
    form = CreateContentForm()
    if form.validate_on_submit():
        print(form.image.data)
        print(form.caption_text.data)
        tags = form.tag_text.data.split(',')
        print(tags)
    return render_template('create_post.html', form = form)
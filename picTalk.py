from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
from flask_bcrypt import Bcrypt

# Create a Flask application instance
app = Flask(__name__, template_folder='app/templates', static_folder='app/static')

# Configure SQLAlchemy database URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///picTalk.db'
# Initialize SQLAlchemy
db = SQLAlchemy(app)

# Initialize bcrypt
bcrypt = Bcrypt(app)

with app.app_context():
    class USER(db.Model):
        __tablename__ = 'USER'
        
        username = db.Column(db.String(20), primary_key = True)
        password = db.Column(db.String(1000), nullable = False)
        
        def __init__(self, username, password):
            self.username = username
            self.password = password

    db.create_all()
    
# Route for the sign up page
@app.route('/', methods=['GET', 'POST'])
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
            return redirect(url_for('login'))
        except:
            return render_template('login.html', error = 'Error, unable to create an account')

    else:
        return render_template("signup.html")

# Route for the login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        login_username = request.form['login-username']
        login_password = request.form['login-password']

        user = USER.query.filter_by(username = login_username).first()
        if user:
            if user.password == login_password:
                return redirect(url_for('home'))
            else:
                return render_template('login.html', error = 'Invalid username or password')
        else:
            return render_template('login.html', error = 'Invalid username or password')
    
    return render_template('login.html')

@app.route('/home')
def home():
    return render_template('home.html')

if __name__ == '__main__':
    app.run(debug=True)

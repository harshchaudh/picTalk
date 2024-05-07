from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

from model import db, init_login
from routes import picTalk_bp

from config import Config

# Create a Flask application instance
app = Flask(__name__)
app.config.from_object(Config)

# Initialize SQLAlchemy
db.init_app(app)

# Initialize Flask-Login
login_manager = LoginManager(app)
login_manager.login_view = 'picTalk.login'

# Initialize Flask-Login in the model module
init_login(login_manager)

with app.app_context():
    db.create_all()

app.register_blueprint(picTalk_bp)

if __name__ == '__main__':
    app.run(debug=True)

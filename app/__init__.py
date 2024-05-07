from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

from model import db, init_login
from routes import picTalk_bp

from app.config import Config

app = Flask(__name__)
app.config.from_object(Config)
    
# Initialize SQLAlchemy
db.init_app(app)

# Initialize Flask-Login
login_manager = LoginManager(app)
login_manager.login_view = 'picTalk.login'

# Initialize Flask-Login in the model module
init_login(login_manager)

app.register_blueprint(picTalk_bp)

with app.app_context():
    db.create_all()

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate

from app.config import Config
from app.model import db, init_login
from app.routes import picTalk_bp
from app.utilities import format_profileNumbers, truncate_comment_time, truncate_username

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize SQLAlchemy
    db.init_app(app)

    # Initialize Flask-Migrate, moved to picTalk.py
    # migrate = Migrate(app, db)

    # Initialize Flask-Login
    login_manager = LoginManager()
    login_manager.login_view = 'picTalk.login'
    login_manager.login_message = u"Please log in to access this page or sign up for free."
    login_manager.login_message_category = "info"
    login_manager.init_app(app)

    # Initialize Flask-Login in the model module
    init_login(login_manager)

    # Register blueprints
    app.register_blueprint(picTalk_bp)

    # Register Jinja filters
    app.jinja_env.filters['format_profileNumbers'] = format_profileNumbers
    app.jinja_env.filters['truncate_username'] = truncate_username
    app.jinja_env.filters['truncate_comment_time'] = truncate_comment_time

    with app.app_context():
        db.create_all()

    return app

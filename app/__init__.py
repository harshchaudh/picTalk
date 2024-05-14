from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate

from app.model import db, init_login
from app.routes import picTalk_bp

from app.config import Config
from app.utilities import format_profileNumbers, truncate_username

app = Flask(__name__)
app.config.from_object(Config)
    
# Initialize SQLAlchemy
db.init_app(app)
migrate = Migrate(app, db)
# Initialize Flask-Login
login_manager = LoginManager(app)
login_manager.login_view = 'picTalk.login'

# Initialize Flask-Login in the model module
init_login(login_manager)

app.jinja_env.filters['format_profileNumbers'] = format_profileNumbers
app.jinja_env.filters['truncate_username'] = truncate_username

app.register_blueprint(picTalk_bp)

with app.app_context():
    db.create_all()

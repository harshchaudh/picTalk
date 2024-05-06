from flask import Flask
from app.config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config.from_object(Config)
    
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

with app.app_context():
    db.create_all()

from app.model import USER
from app.routes import picTalk_bp
app.register_blueprint(picTalk_bp)
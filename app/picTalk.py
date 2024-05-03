from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

from model import db
from routes import picTalk_bp

# Create a Flask application instance
app = Flask(__name__) #template_folder='app/templates', static_folder='app/static'

# Configure SQLAlchemy database URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///picTalk.db'
# Initialize SQLAlchemy
db.init_app(app)

# Initialize bcrypt
bcrypt = Bcrypt(app)

with app.app_context():
    db.create_all()

app.register_blueprint(picTalk_bp)

if __name__ == '__main__':
    app.run(debug=True)

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# USER table in picTalk.db
class USER(db.Model):
    __tablename__ = 'USER'
    
    username = db.Column(db.String(20), primary_key=True)
    password = db.Column(db.String(1000), nullable=False)
    
    def __init__(self, username, password):
        self.username = username
        self.password = password

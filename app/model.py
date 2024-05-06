from flask_sqlalchemy import SQLAlchemy
# from flask_bcrypt import Bcrypt

db = SQLAlchemy()

# USER table in picTalk.db
class USER(db.Model):
    __tablename__ = 'USER'
    
    username = db.Column(db.String(20), primary_key=True)
    password = db.Column(db.String(1000), nullable=False)
    
    def __init__(self, username, password):
        self.username = username
        self.password = password

# SUBMISSION table in picTalk.db
class SUBMISSION(db.Model):
    __tablename__ = 'SUBMISSION'

    submission_id = db.Column(db.String(20), primary_key=True)

    username = db.Column(db.String(20), db.ForeignKey('USER.username'), nullable=False)
    user = db.relationship('USER', backref='SUBMISSION', lazy=True)

    # Additional columns required image, caption and tags. Perhaps extra fields not sure.

# COMMENT table in picTalk.db
class COMMENT(db.Model):
    __tablename__ = 'COMMENT'

    comment_id  = db.Column(db.String(20), primary_key=True)
    comment = db.Column(db.String(20), nullable=False)

    username = db.Column(db.String(20), db.ForeignKey('USER.username'), nullable=False)
    user = db.relationship('USER', backref='COMMENT', lazy=True)
    
    submission_id = db.Column(db.String(20), db.ForeignKey('SUBMISSION.submission_id'), nullable=False)
    submit = db.relationship('SUBMISSION', backref='COMMENT', lazy=True)
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Initialize Flask-Login with the provided login_manager instance
def init_login(login_manager):
    @login_manager.user_loader
    def load_user(username):
        return USER.query.get(username)
    
# USER table in picTalk.db
class USER(UserMixin, db.Model):
    __tablename__ = 'USER'
    
    username = db.Column(db.String(32), primary_key=True)
    password = db.Column(db.String(128), nullable=False)
    
    def __init__(self, username, password):
        self.username = username
        self.password = password
        
    def get_id(self):
        return self.username


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


class TAGS():
    __tablename__ = "TAGS"

    tag = id
    
    submission_id = db.Column(db.String(20), db.ForeignKey('SUBMISSION.submission_id'), nullable=False)
    submit = db.relationship('SUBMISSION', backref='TAGS', lazy=True)
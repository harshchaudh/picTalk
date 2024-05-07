from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import LargeBinary

db = SQLAlchemy()

# Initialize Flask-Login with the provided login_manager instance
def init_login(login_manager):
    @login_manager.user_loader
    def load_user(username_id):
        return USER.query.get(username_id)
    
# USER table in picTalk.db
class USER(UserMixin, db.Model):
    __tablename__ = 'USER'

    username_id = db.Column(db.Integer, primary_key = True, autoincrement = True)

    username = db.Column(db.String(32), unique = True, nullable = False)
    password = db.Column(db.String(128), nullable=False)
    
    def __init__(self, username_id, username, password):
        self.username_id = username_id
        self.username = username
        self.password = password
    
    def get_id(self):
        return str(self.username_id)


# SUBMISSION table in picTalk.db
class SUBMISSION(db.Model):
    __tablename__ = 'SUBMISSION'

    submission_id = db.Column(db.Integer, primary_key=True, autoincrement = True)

    image = db.Column(LargeBinary)
    caption = db.Column(db.String(256))

    username_id = db.Column(db.Integer, db.ForeignKey('USER.username_id'), nullable=False)
    user = db.relationship('USER', backref='SUBMISSION', lazy=True)

    # Additional columns required image, and tags. Perhaps extra fields not sure.

# COMMENT table in picTalk.db
class COMMENT(db.Model):
    __tablename__ = 'COMMENT'

    comment_id  = db.Column(db.Integer, primary_key=True, autoincrement = True)

    comment = db.Column(db.String(20), nullable=False)

    username_id = db.Column(db.Integer, db.ForeignKey('USER.username_id'), nullable=False)
    user = db.relationship('USER', backref='COMMENT', lazy=True)
    
    submission_id = db.Column(db.Integer, db.ForeignKey('SUBMISSION.submission_id'), nullable=False)
    submit = db.relationship('SUBMISSION', backref='COMMENT', lazy=True)


class TAGS(db.Model):
    __tablename__ = "TAGS"

    tag_id = db.Column(db.Integer, primary_key = True, autoincrement = True)

    tag = db.Column(db.String(15), unique = True, nullable = False)
    
    submission_id = db.Column(db.Integer, db.ForeignKey('SUBMISSION.submission_id'), nullable=False)
    submit = db.relationship('SUBMISSION', backref='TAGS', lazy=True)
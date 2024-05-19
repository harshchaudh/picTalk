from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

from werkzeug.security import generate_password_hash, check_password_hash

from datetime import datetime

db = SQLAlchemy()

# Initialize Flask-Login with the provided login_manager instance
def init_login(login_manager):
    @login_manager.user_loader
    def load_user(user_id):
        return USER.query.get(int(user_id))

# USER table in picTalk.db
class USER(UserMixin, db.Model):
    __tablename__ = 'USER'

    username_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(
        db.String(32),
        unique=True,
        nullable=False,
        index=True)
    password = db.Column(db.String(128), nullable=False)
    about_me = db.Column(db.String(128))

    def __init__(self, username, password, about_me):
        self.username = username
        self.password = generate_password_hash(password)
        self.about_me = about_me

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def get_id(self):
        return str(self.username_id)

    def __repr__(self):
        return f'<USER {self.username_id}: {self.username}>'

# SUBMISSION table in picTalk.db
class SUBMISSION(db.Model):
    __tablename__ = 'SUBMISSION'

    submission_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    image = db.Column(db.LargeBinary)
    caption = db.Column(db.String(256))
    created_at = db.Column(db.DateTime, default=datetime.now)

    username_id = db.Column(
        db.Integer,
        db.ForeignKey('USER.username_id'),
        nullable=False)
    user = db.relationship(
        'USER',
        backref=db.backref(
            'submissions',
            lazy=True,
            cascade="all, delete-orphan"))

    def __repr__(self):
        return f'<SUBMISSION {self.submission_id} about {self.caption} by User {self.username_id}>'

# COMMENT table in picTalk.db
class COMMENT(db.Model):
    __tablename__ = 'COMMENT'

    comment_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    comment = db.Column(db.String(256), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)

    username_id = db.Column(
        db.Integer,
        db.ForeignKey('USER.username_id'),
        nullable=False)
    user = db.relationship(
        'USER',
        backref=db.backref(
            'comments',
            lazy=True,
            cascade="all, delete-orphan"))

    submission_id = db.Column(db.Integer, db.ForeignKey(
        'SUBMISSION.submission_id'), nullable=False)
    submit = db.relationship(
        'SUBMISSION',
        backref=db.backref(
            'comments',
            lazy=True,
            cascade="all, delete-orphan"))

    def __repr__(self):
        return f'<COMMENT {self.comment_id} on Submission {self.submission_id}>'

# TAGS table in picTalk.db
class TAGS(db.Model):
    __tablename__ = "TAGS"

    tag_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tag = db.Column(db.String(15), nullable=False)

    submission_id = db.Column(db.Integer, db.ForeignKey(
        'SUBMISSION.submission_id'), nullable=False)
    submit = db.relationship(
        'SUBMISSION',
        backref=db.backref(
            'tags',
            lazy=True,
            cascade="all, delete-orphan"))

    def __repr__(self):
        return f'<TAG {self.tag} on Submission {self.submission_id}>'

# Follower table in picTalk.db
class FOLLOWER(db.Model):
    __tablename__ = "FOLLOWER"

    id = db.Column(db.Integer, primary_key=True)
    follower_id = db.Column(
        db.Integer,
        db.ForeignKey('USER.username_id'),
        nullable=False)
    followed_id = db.Column(
        db.Integer,
        db.ForeignKey('USER.username_id'),
        nullable=False)

    follower = db.relationship(
        "USER",
        foreign_keys=[follower_id],
        backref="following")
    followed = db.relationship(
        "USER",
        foreign_keys=[followed_id],
        backref="followers")

    # Unique constraint to ensure a user can't follow another user multiple
    # times
    __table_args__ = (
        db.UniqueConstraint(
            'follower_id',
            'followed_id',
            name='_follower_followed_uc'),
    )

    def __repr__(self):
        return f'< {self.follower_id} Followers {self.followed_id}>'

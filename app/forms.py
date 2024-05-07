from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed

from wtforms import StringField, PasswordField, SubmitField, TextAreaField, validators
from wtforms.validators import DataRequired, Length, EqualTo, Regexp

from app.utilities import ValidateTags

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=20)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class SignupForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=20)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6), EqualTo('confirm_password', message='Passwords must match')])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired()])
    submit = SubmitField('Sign Up')

class CreateContentForm(FlaskForm):
    image = FileField('', validators=[FileRequired(), FileAllowed(['jpg', 'png', 'jpeg'], '.jpg, .png, and .jpeg only.')])
    caption_text = TextAreaField('Enter your caption', validators=[DataRequired(), Regexp('^[a-zA-Z ,.!?]+$', message='No special characters in caption.')])
    tag_text = StringField('Enter your tags', validators=[DataRequired(), ValidateTags, Regexp('^[a-zA-Z,]+$', message='Alphabetical characters in tags only.')])
    submit = SubmitField('Submit')
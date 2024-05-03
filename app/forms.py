from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed

from wtforms import StringField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, EqualTo

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
    image = FileField('', validators=[FileRequired(), FileAllowed(['jpg', 'png', 'jpeg'], 'Images only')])
    caption_text = TextAreaField('Enter your caption', validators=[DataRequired()])
    tag_text = StringField('Enter your tags', validators=[DataRequired()])
    submit = SubmitField('Submit')
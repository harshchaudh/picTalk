from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed

from wtforms import StringField, PasswordField, SubmitField, TextAreaField, validators
from wtforms.validators import DataRequired, Length, EqualTo, Regexp, ValidationError

from app.utilities import ValidateTags, UsernameValidation, PasswordValidation

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=20)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class SignupForm(FlaskForm):
    username = StringField('Username', validators=[
                            DataRequired(), 
                            Length(min=3, max=20), 
                            UsernameValidation()
                            ])

    password = PasswordField('Password', validators=[
                            DataRequired(), 
                            Length(min=8),  
                            PasswordValidation()
                            ])
    
    confirm_password = PasswordField('Confirm Password', validators=[
                                    DataRequired(),
                                    EqualTo('password', message='Passwords must match')])
    
    submit = SubmitField('Sign Up')

class CreateContentForm(FlaskForm):
    image = FileField('', validators=[FileRequired(), FileAllowed(['jpg', 'png', 'jpeg'], '.jpg, .png, and .jpeg only.')])
    caption_text = TextAreaField('Enter your caption', validators=[DataRequired(), Regexp('^[a-zA-Z ,.!?]+$', message='No special characters in caption.')])
    tag_text = StringField('Enter your tags', validators=[DataRequired(), ValidateTags, Regexp('^[a-zA-Z,]+$', message='Alphabetical characters in tags only.')])
    submit = SubmitField('Submit')

class EditProfileForm(FlaskForm):
    username = StringField('Username', validators=[
                        DataRequired(), 
                        Length(min=3, max=20), 
                        UsernameValidation()
                        ])
    about_me = TextAreaField('About me', validators=[Length(min=0, max=140)])
    submit = SubmitField('Submit')
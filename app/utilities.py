import re
from wtforms import ValidationError, validators
from app.model import USER 

# Validate tags used in forms.py
def ValidateTags(form, field):
    tags = field.data.split(',')
    if len(tags) > 5:
        raise validators.ValidationError('You must not submit more than 5 tags.')
    if '' in tags:
        raise validators.ValidationError('Tags can not be empty.')

# Validate username used in routes.py
class UsernameValidation:
    # Only allows letters (a-z and A-Z), digits (0-9), underscore (_) and periods (.)
    # The username must also be a minimum of 3 characters and a maximum of 20 characters
    # The username cannot begin with a digit, underscore or period. 
    # The username cannot end with an underscore or period.
    # The username cannot be a string of numbers
    regex = r'^[a-zA-Z][a-zA-Z0-9_.]{1,18}[a-zA-Z0-9]$'

    def __init__(self, message = None):
        if not message:
            message = "Username does not meet criteria."
        self.message = message

    def __call__(self, form, field):
        if not re.match(self.regex, field.data):
            raise ValidationError(self.message)
    
    @classmethod
    def validate(cls, username):
        return not re.match(cls.regex, username)


    
# Validate password used in routes.py
class PasswordValidation:
    # Minimum eight characters, at least one letter and one number
    regex = r"^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$"

    def __init__(self, message = None):
        if not message:
            message = "Password does not meet criteria.oakdpo"
        self.message = message

    def __call__(self, form, field):
        if not re.match(self.regex, field.data):
            raise ValidationError(self.message)

    @classmethod
    def validate(cls, password):
        return not re.match(cls.regex, password)

        
# Truncate usernames when username is too long for navigation bar.
def truncate_username(username, max_length = 10):
    if len(username) > max_length:
        username = username[:(max_length - 3)] + "..."
    return username

# Truncate submission, follower and following values when they exceed thresholds.
def format_profileNumbers(value):
    if value >= 1_000_000:
        return "{:.0f}M".format(value / 10000) #just in case theres a million and one users one day.
    if value >= 10000:
        return "{:.0f}K".format(value / 1000)
    else:
        return "{:,}".format(value)
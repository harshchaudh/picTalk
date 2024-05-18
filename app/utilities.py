from datetime import datetime, timedelta
import re
from wtforms import ValidationError, validators
from flask import flash
from app.model import USER, FOLLOWER

# Validate tags used in forms.py
def ValidateTags(form, field):
    tags = field.data.split(',')
    if len(tags) > 5:
        raise validators.ValidationError(
            'You must not submit more than 5 tags.')
    if '' in tags:
        raise validators.ValidationError('Tags can not be empty.')
    unique_tags = set(tags)
    if len(unique_tags) != len(tags):
        raise ValidationError('Duplicate tags are not allowed.')

# Validate username used in routes.py
class UsernameValidation:
    # Only allows letters (a-z and A-Z), digits (0-9), underscore (_) and periods (.)
    # The username must also be a minimum of 3 characters and a maximum of 32 characters
    # The username cannot begin with a digit, underscore or period.
    # The username cannot end with an underscore or period.
    # The username cannot be a string of numbers
    regex = r'^[a-zA-Z][a-zA-Z0-9_.]{1,18}[a-zA-Z0-9]$'

    def __init__(self, message=None):
        if not message:
            message = "Username does not meet criteria"
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

    def __init__(self, message=None):
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
def truncate_username(username, max_length=10):
    if len(username) > max_length:
        username = username[:(max_length - 3)] + "..."
    return username

# Fomat profile numbers if they exceed a certain threshold.
def format_profileNumbers(value):
    if value >= 1_000_000:
        return "{:.0f}M".format(value / 10000)
    if value >= 10000:
        return "{:.0f}K".format(value / 1000)
    else:
        return "{:,}".format(value)

# Split a list into three seperate lists using a given structure.
def organiseColumnImages(elements):
    return elements[::3], elements[1::3], elements[2::3]

# Truncate time so it looks more natural and readable to the user.
def truncate_comment_time(comment_time):
    time_diff = (datetime.now() - comment_time)
    day_diff = time_diff.days

    yrs = day_diff // 365
    months = (day_diff % 365) // 30

    if yrs > 0:
        return f"{yrs} years ago"
    elif months > 0:
        return f"{months} months ago"
    elif day_diff > 0:
        return f"{day_diff} days ago"
    else:
        hrs = time_diff.seconds // 3600
        mins = (time_diff.seconds % 3600) // 60
        if hrs > 0:
            return f"{hrs} hours ago"
        else:
            if mins == 0:
                return "now"
            else:
                return f"{mins} minutes ago"

# Check if two users are following each other.
def is_following(follower_id, followed_id):
    follower_entry = FOLLOWER.query.filter_by(
        follower_id=follower_id, followed_id=followed_id).first()

    if follower_entry is not None:
        return True
    else:
        return False

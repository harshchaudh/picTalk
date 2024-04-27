import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'un-guessable'
    UPLOAD_FOLDER = 'uploads/'
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
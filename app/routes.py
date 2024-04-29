from app import app
from flask import flash, redirect, render_template
from app.forms import CreateContentForm
from werkzeug.utils import secure_filename
import os

@app.route('/')
@app.route('/index')
def index():
    return render_template('home.html')

@app.route('/create', methods=['GET', 'POST'])
def create():
    form = CreateContentForm()
    if form.validate_on_submit():
        pass
    return render_template('create_post.html', form=form)
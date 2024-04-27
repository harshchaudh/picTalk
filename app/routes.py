from app import app
from flask import render_template
from app.forms import ImageForm

@app.route('/')
@app.route('/index')
def index():
    return render_template('home.html')

@app.route('/create', methods=['GET', 'POST'])
def create():
    form = ImageForm()
    return render_template('create_post.html', form=form)
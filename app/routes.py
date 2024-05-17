from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user

from sqlalchemy.exc import IntegrityError

import base64

from app.model import db, USER, SUBMISSION, COMMENT, TAGS, FOLLOWER
from app.forms import CreateContentForm, EditProfileForm, CommentForm
from app.utilities import UsernameValidation, PasswordValidation, organiseColumnImages, is_following

picTalk_bp = Blueprint('picTalk', __name__)


@picTalk_bp.route('/')
def home():
    return render_template('home.html', current_user=current_user)


@picTalk_bp.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == "POST":
        query = request.form['search'].lower()

        if current_user.is_authenticated:  # Makes sure that current user is not included in the results
            users = USER.query.filter(
                USER.username.like(
                    f"%{query}%"),
                USER.username != current_user.username).all()
        else:
            users = USER.query.filter(USER.username.like(f"%{query}%")).all()

        tags = TAGS.query.filter(TAGS.tag.like(f"%{query}%")).all()
        return render_template(
            'search.html', users=users, tags=tags, query=query)

    return render_template('search.html')


@picTalk_bp.route('/gallery')
def gallery():
    images = SUBMISSION.query.order_by(SUBMISSION.created_at).all()

    base64_images_firstColumn = base64_images_secondColumn = base64_images_thirdColumn = []
    if images:
        base64_images = [
            {"id": image.submission_id,
             "data": base64.b64encode(image.image).decode("utf-8")}
            for image in images
        ]
        base64_images.reverse()

        base64_images_firstColumn = organiseColumnImages(base64_images)[0]
        base64_images_secondColumn = organiseColumnImages(base64_images)[1]
        base64_images_thirdColumn = organiseColumnImages(base64_images)[2]
    followed_count = 0
    base64_images_firstColumn_following = base64_images_secondColumn_following = base64_images_thirdColumn_following = []
    if current_user.is_authenticated:
        images_following = (
            SUBMISSION.query .join(
                FOLLOWER, FOLLOWER.followed_id == SUBMISSION.username_id) .filter(
                FOLLOWER.follower_id == current_user.username_id) .order_by(
                SUBMISSION.created_at) .all())
        base64_images_following = [
            {"id": image.submission_id,
             "data": base64.b64encode(image.image).decode("utf-8")}
            for image in images_following
        ]
        base64_images_following.reverse()

        base64_images_firstColumn_following = organiseColumnImages(
            base64_images_following)[0]
        base64_images_secondColumn_following = organiseColumnImages(
            base64_images_following)[1]
        base64_images_thirdColumn_following = organiseColumnImages(
            base64_images_following)[2]

        followed_count = FOLLOWER.query.filter_by(
            follower_id=current_user.username_id).count()
    return render_template(
        'gallery.html',
        user=current_user,
        followed_count=followed_count,

        images_firstColumn=base64_images_firstColumn,
        images_secondColumn=base64_images_secondColumn,
        images_thirdColumn=base64_images_thirdColumn,

        images_firstColumn_following=base64_images_firstColumn_following,
        images_secondColumn_following=base64_images_secondColumn_following,
        images_thirdColumn_following=base64_images_thirdColumn_following)


@picTalk_bp.route('/gallery/<string:tag>')
def gallery_tags(tag):
    tag = TAGS.query.filter_by(tag=tag).first()

    base64_images_firstColumn_tag = base64_images_secondColumn_tag = base64_images_thirdColumn_tag = []
    if tag:
        images_tag = SUBMISSION.query.filter_by(
            submission_id=tag.submission_id).all()

        base64_images_tag = [
            {"id": image.submission_id,
             "data": base64.b64encode(image.image).decode("utf-8")}
            for image in images_tag
        ]
        base64_images_tag.reverse()

        base64_images_firstColumn_tag = organiseColumnImages(
            base64_images_tag)[0]
        base64_images_secondColumn_tag = organiseColumnImages(
            base64_images_tag)[1]
        base64_images_thirdColumn_tag = organiseColumnImages(
            base64_images_tag)[2]

    return render_template(
        'gallery_tags.html',
        tag=tag,
        images_firstColumn_tag=base64_images_firstColumn_tag,
        images_secondColumn_tag=base64_images_secondColumn_tag,
        images_thirdColumn_tag=base64_images_thirdColumn_tag)


@picTalk_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == "POST":
        signup_username = request.form['signup-username'].lower()
        signup_psw = request.form['signup-psw']
        signup_pswConfirm = request.form['signup-pswConfirm']

        if signup_psw != signup_pswConfirm:
            flash('Passwords do not match.', 'warning')
            return render_template('signup.html')

        if UsernameValidation.validate(signup_username):
            flash('Username does not meet criteria.', 'warning')
            return render_template('signup.html')

        if PasswordValidation.validate(signup_psw):
            flash('Password does not meet criteria.', 'warning')
            return render_template('signup.html')

        existing_user = USER.query.filter_by(username=signup_username).first()
        if existing_user:
            flash('Username is already in use.', 'danger')
            return render_template('signup.html')

        # Only pass the username and unhashed password
        new_user = USER(username=signup_username, password=signup_psw, about_me="")
        db.session.add(new_user)
        db.session.commit()
        flash('Account created successfully! Please log in.', 'success')
        return redirect(url_for('picTalk.login'))

    return render_template("signup.html")


@picTalk_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        login_username = request.form['login-username'].lower()
        login_password = request.form['login-password']

        user = USER.query.filter_by(username=login_username).first()
        if user and user.check_password(login_password):
            login_user(user)
            flash('Logged in successfully.', 'success')
            return redirect(url_for('picTalk.home'))
        else:
            flash('Invalid username or password.', 'warning')

    return render_template('login.html')


@picTalk_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('picTalk.home'))


@picTalk_bp.route('/profile/<string:username>')
def profile(username):
    user = USER.query.filter_by(username=username).first_or_404()
    submission_count = SUBMISSION.query.filter_by(
        username_id=user.username_id).count()

    images = SUBMISSION.query.filter_by(
        username_id=user.username_id).order_by(
        SUBMISSION.created_at).all()
    base64_images = [
        {"id": image.submission_id, "data": base64.b64encode(
            image.image).decode("utf-8")}
        for image in images
    ]
    base64_images.reverse()

    base64_images_firstColumn = organiseColumnImages(base64_images)[0]
    base64_images_secondColumn = organiseColumnImages(base64_images)[1]
    base64_images_thirdColumn = organiseColumnImages(base64_images)[2]

    check_following = False
    if current_user.is_authenticated:
        check_following = is_following(
            current_user.username_id, user.username_id)

    follower_count = FOLLOWER.query.filter_by(
        followed_id=user.username_id).count()
    followed_count = FOLLOWER.query.filter_by(
        follower_id=user.username_id).count()

    return render_template('profile.html', user=user,
                           submission_count=submission_count,
                           check_following=check_following,
                           follower_count=follower_count,
                           followed_count=followed_count,
                           images_firstColumn=base64_images_firstColumn,
                           images_secondColumn=base64_images_secondColumn,
                           images_thirdColumn=base64_images_thirdColumn)


@picTalk_bp.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved.', 'success')
        return redirect(url_for('picTalk.profile',
                        username=current_user.username))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    else:
        flash('Username did not meet criteria', 'warning')

    return render_template('edit_profile.html',
                           title='Edit Profile', form=form)


@picTalk_bp.route('/image/<int:submission_id>', methods=['GET', 'POST'])
@login_required
def view_post(submission_id):
    form = CommentForm()
    image = SUBMISSION.query.get(submission_id)
    base64_image = base64.b64encode(image.image).decode("utf-8")
    comments = COMMENT.query.filter_by(submission_id=submission_id).all()
    creator = USER.query.get(image.username_id)

    if form.validate_on_submit():
        new_comment = COMMENT(comment=form.comment.data,
                              username_id=current_user.username_id,
                              submission_id=submission_id)
        try:
            db.session.add(new_comment)
            db.session.commit()
            flash('Comment created successfully.', 'success')
        except BaseException:
            flash('Comment failed to submit. Please try again.', 'danger')
        return redirect(url_for('picTalk.view_post',
                        submission_id=submission_id))

    return render_template(
        'view_post.html',
        form=form,
        image=image,
        base64_image=base64_image,
        comments=comments,
        creator=creator)


@picTalk_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    form = CreateContentForm()
    if form.validate_on_submit():
        image_file = form.image.data
        image_data = image_file.read()
        tags = form.tag_text.data.split(',')

        new_submission = SUBMISSION(image=image_data,
                                    caption=form.caption_text.data,
                                    username_id=current_user.username_id)
        try:
            db.session.add(new_submission)
            db.session.commit()

            for tag in tags:
                newtag = TAGS(tag=tag.strip(),
                              submission_id=new_submission.submission_id)
                db.session.add(newtag)
            db.session.commit()

            flash('Post created successfully!', 'success')
            return redirect(url_for('picTalk.home'))
        except BaseException:
            flash('Post failed to submit.', 'danger')
            render_template('create_post.html')

    return render_template('create_post.html', form=form)


@picTalk_bp.route('/follow/<int:username_id>', methods=['POST'])
def follow(username_id):
    follower_id = current_user.username_id
    user = USER.query.filter_by(username_id=username_id).first()

    if follower_id:
        new_follower = FOLLOWER(
            follower_id=follower_id,
            followed_id=username_id)
        db.session.add(new_follower)
        db.session.commit()
        flash('Sucessfully followed user', 'success')
        return redirect(url_for('picTalk.profile', username=user.username))
    else:
        flash('Error could not follow!', 'warning')
        return redirect(url_for('picTalk.profile', username=user.username))


@picTalk_bp.route('/unfollow/<int:username_id>', methods=['POST'])
def unfollow(username_id):
    follower_id = current_user.username_id
    user = USER.query.filter_by(username_id=username_id).first()

    if follower_id:
        FOLLOWER.query.filter_by(
            follower_id=follower_id,
            followed_id=username_id).delete()
        db.session.commit()
        flash('Sucessfully unfollowed user', 'success')
        return redirect(url_for('picTalk.profile', username=user.username))
    else:
        flash('Error could not unfollow!', 'warning')
        return redirect(url_for('picTalk.profile', username=user.username))

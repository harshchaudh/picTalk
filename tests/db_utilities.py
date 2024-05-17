from app import db
from app.model import USER, SUBMISSION, COMMENT, TAGS, FOLLOWER

def populate_db():
    user1 = USER(username='user1', password='password1', about_me='I am user 1')
    user2 = USER(username='user2', password='password2', about_me='I am user 2')
    user3 = USER(username='user3', password='password3', about_me='I am user 3')

    db.session.add(user1)
    db.session.add(user2)
    db.session.add(user3)
    db.session.commit()

    submission1 = SUBMISSION(image=b'image_data_1', caption='This is my first submission', username_id=user1.username_id)
    submission2 = SUBMISSION(image=b'image_data_2', caption='This is another submission', username_id=user2.username_id)

    db.session.add(submission1)
    db.session.add(submission2)
    db.session.commit()

    comment1 = COMMENT(comment='Great submission!', username_id=user2.username_id, submission_id=submission1.submission_id)
    comment2 = COMMENT(comment='Nice photo!', username_id=user3.username_id, submission_id=submission1.submission_id)
    comment3 = COMMENT(comment='Well done!', username_id=user1.username_id, submission_id=submission2.submission_id)

    db.session.add(comment1)
    db.session.add(comment2)
    db.session.add(comment3)
    db.session.commit()

    tag1 = TAGS(tag='nature', submission_id=submission1.submission_id)
    tag2 = TAGS(tag='photography', submission_id=submission1.submission_id)
    tag3 = TAGS(tag='art', submission_id=submission2.submission_id)

    db.session.add(tag1)
    db.session.add(tag2)
    db.session.add(tag3)
    db.session.commit()

    follow1 = FOLLOWER(follower_id=user1.username_id, followed_id=user2.username_id)
    follow2 = FOLLOWER(follower_id=user2.username_id, followed_id=user3.username_id)
    follow3 = FOLLOWER(follower_id=user3.username_id, followed_id=user1.username_id)

    db.session.add(follow1)
    db.session.add(follow2)
    db.session.add(follow3)
    db.session.commit()
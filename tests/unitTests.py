import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

os.environ['DATABASE_URL'] = 'sqlite:///:memory:'

import unittest
from app import app, db
from app.model import USER, SUBMISSION, COMMENT, TAGS, FOLLOWER
from app.utilities import ValidateTags, UsernameValidation, PasswordValidation, truncate_username, is_following
from wtforms import Form, StringField, ValidationError

class MockForm(Form):
    field = StringField()

class BasicUnitTests(unittest.TestCase):
    def setUp(self):
        self.app_context = app.app_context()
        self.app_context.push()
        db.create_all()
        self.populate_db()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def populate_db(self):
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

    def test_password_hashing(self):
        user1 = USER.query.filter_by(username='user1').first()
        self.assertIsNotNone(user1, "User1 should not be None")
        self.assertFalse(user1.check_password('notpassword1'))
        self.assertTrue(user1.check_password('password1'))

    def test_is_following(self):
        user1 = USER.query.filter_by(username='user1').first()
        user2 = USER.query.filter_by(username='user2').first()
        user3 = USER.query.filter_by(username='user3').first()
        self.assertIsNotNone(user1, "User1 should not be None")
        self.assertIsNotNone(user2, "User2 should not be None")
        self.assertIsNotNone(user3, "User3 should not be None")

        self.assertTrue(is_following(user1.username_id, user2.username_id))
        self.assertFalse(is_following(user2.username_id, user1.username_id))
        self.assertTrue(is_following(user2.username_id, user3.username_id))
        self.assertTrue(is_following(user3.username_id, user1.username_id))
        self.assertFalse(is_following(user1.username_id, user3.username_id))

    def test_validate_tags(self):
        form = MockForm()
        
        # Test valid tags
        form.field.data = "nature,photography,art"
        self.assertIsNone(ValidateTags(form, form.field))
        
        # Test too many tags
        form.field.data = "nature,photography,art,landscape,portrait,extra"
        with self.assertRaises(ValidationError):
            ValidateTags(form, form.field)
        
        # Test empty tags
        form.field.data = "nature,,photography"
        with self.assertRaises(ValidationError):
            ValidateTags(form, form.field)

    def test_username_validation(self):
        form = MockForm()
        validator = UsernameValidation()

        #Test valid usernames
        valid_usernames = ["user1", "valid_user", "test123"]
        for username in valid_usernames:
            form.field.data = username
            self.assertIsNone(validator(form, form.field))

        #Test invalid usernames
        invalid_usernames = ["", "a"*21, "invalid user!", "123username", "user_", "user.", "1234567890"]
        for username in invalid_usernames:
            form.field.data = username
            with self.assertRaises(ValidationError):
                validator(form, form.field)

    def test_password_validation(self):
        form = MockForm()
        validator = PasswordValidation()

        # Test valid passwords
        valid_passwords = ["password1", "1234abcd"]
        for password in valid_passwords:
            form.field.data = password
            try:
                validator(form, form.field)
            except ValidationError:
                self.fail(f"Valid password '{password}' raised ValidationError")

        # Test invalid passwords with no nums | no characters
        invalid_passwords = ["password", "12345678", "short", "nonumber"]
        for password in invalid_passwords:
            form.field.data = password
            with self.assertRaises(ValidationError):
                validator(form, form.field)


    def test_truncate_username(self):
        # Test username truncation
        self.assertEqual(truncate_username("short"), "short")
        self.assertEqual(truncate_username("verylongusername"), "verylon...")
        self.assertEqual(truncate_username("mediumlongname"), "mediuml...")

if __name__ == '__main__':
    unittest.main(verbosity=2)

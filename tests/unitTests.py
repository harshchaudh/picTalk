import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import multiprocessing
import unittest
from app import create_app, db
from app.config import TestingConfig
from app.model import USER, SUBMISSION, COMMENT, TAGS, FOLLOWER
from app.utilities import ValidateTags, UsernameValidation, PasswordValidation, truncate_username, is_following
from wtforms import Form, StringField, ValidationError
from db_utilities import populate_db

class MockForm(Form):
    field = StringField()

class BasicUnitTests(unittest.TestCase):
    def setUp(self):
        testApp = create_app(TestingConfig)
        self.app_context = testApp.app_context()
        self.app_context.push()
        db.create_all()
        populate_db()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()


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

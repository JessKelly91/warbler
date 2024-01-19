"""User model tests."""
import os
from unittest import TestCase

from models import db, User, Message, Follows

#connect to test database + import app
os.environ['DATABASE_URL'] = "postgresql:///warbler-test"

from app import app

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

with app.app_context():
    db.drop_all()
    db.create_all()


class UserModelTestCase(TestCase):
    """Test views for messages."""

    def setUp(self):
        """Create test client, add sample data."""

        with app.app_context():
            User.query.delete()
            Message.query.delete()
            Follows.query.delete()

            self.client = app.test_client()

    def test_user_model(self):
        """Does basic model work?"""

        u = User(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD"
        )

        with app.app_context():
            db.session.add(u)
            db.session.commit()

            # User should have no messages & no followers & no likes & shouldn't be followed by anyone
            self.assertEqual(len(u.messages), 0)
            self.assertEqual(len(u.followers), 0)
            self.assertEqual(len(u.following), 0)
            self.assertEqual(len(u.likes), 0)

    def test_user_signup_method(self):
        """ensure signup method works when validations met"""

        with app.app_context():
            valid_test_user = User.signup(
                email="test@test.com", 
                username="testuser", 
                password="HASHED_PASSWORD",
                image_url=None)
            
            # User should have no messages & no followers & no likes & shouldn't be followed by anyone
            self.assertEqual(len(valid_test_user.messages), 0)
            self.assertEqual(len(valid_test_user.followers), 0)
            self.assertEqual(len(valid_test_user.following), 0)
            self.assertEqual(len(valid_test_user.likes), 0)

    def test_repr_method(self):

        u = User(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD"
        )

        actual = repr(u)
        expected = f"<User #{u.id}: {u.username}, {u.email}>"

        self.assertEqual(actual, expected)


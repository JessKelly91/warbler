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

            # User should have no messages & no followers
            self.assertEqual(len(u.messages), 0)
            self.assertEqual(len(u.followers), 0)

# TO BE IMPLEMENTED:
# __repr__ method
# is_following detects followers correctly
# is_followed_by detects is or is not following
# user.create creates a new User
# user.create fails if validations not met
# user.authenticate works with valid details and fails with incorrect details
# def logged_in_see_followers_following()
# def logged_out_see_followers_following()
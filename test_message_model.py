"""Message model tests."""
import os
from unittest import TestCase
from sqlalchemy.exc import DataError
from datetime import datetime, timedelta

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


class MessageModelTestCase(TestCase):
    """Test views for messages."""

    def setUp(self):
        """Create test client, add sample data."""

        with app.app_context():
            User.query.delete()
            Message.query.delete()
            Follows.query.delete()

            self.client = app.test_client()

            test_user = User(
                email="test@test.com",
                username="testuser",
                password="HASHED_PASSWORD"
            )

            db.session.add(test_user)
            db.session.commit()

            self.test_user_id = test_user.id

    def test_message_model(self):
        """Does basic model work?"""
        with app.app_context():
            m = Message(text="test message",
                        timestamp=None,
                        user_id=self.test_user_id)
            
            db.session.add(m)
            db.session.commit()

            msg = Message.query.one()
        
        self.assertEqual(msg.text, "test message")        
            
    def test_message_timestamp_defaults_to_utc_now(self):
        """Does the timestamp default to UTC now?"""
        with app.app_context():
            m = Message(text="test message", user_id=self.test_user_id)
            
            db.session.add(m)
            db.session.commit()

            msg = Message.query.one()

        self.assertIsNotNone(msg.timestamp)
        self.assertIsInstance(msg.timestamp, datetime)
        self.assertLessEqual(datetime.utcnow() - msg.timestamp, timedelta(seconds=1))

    def test_message_relationship_with_user(self):
        """Does the relationship with User work?"""
        with app.app_context():
            m = Message(text="test message", user_id=self.test_user_id)
            
            db.session.add(m)
            db.session.commit()

            msg = Message.query.one()
            msg_user = msg.user

        self.assertEqual(msg.user_id, self.test_user_id)
        self.assertIsInstance(msg_user, User)
        self.assertEqual(msg_user.username, "testuser")

    def test_message_text_max_length(self):
        """Does the text have a maximum length of 140 characters?"""
        with app.app_context():
            m = Message(
                text="a" * 141,  # More than 140 characters
                user_id=self.test_user_id
            )

            with self.assertRaises(DataError):
                db.session.add(m)
                db.session.commit()
            db.session.rollback()
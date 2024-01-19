"""User View tests."""

import os
from unittest import TestCase
from models import db, Message, User

#connect to test database and import app
os.environ['DATABASE_URL'] = "postgresql:///warbler-test"
from app import app, CURR_USER_KEY

#create all tables before running tests
with app.app_context():
    db.drop_all()
    db.create_all()

# disable CSRF, since it's a pain to test
app.config['WTF_CSRF_ENABLED'] = False

class UserViewsTestCase(TestCase):
    """Test views for users."""

    def setUp(self):
        """Create test client, add sample data."""
        with app.app_context():
            User.query.delete()
            Message.query.delete()

            self.client = app.test_client()

            self.testuser = User.signup(username="testuser",
                                        email="test@test.com",
                                        password="testuser",
                                        image_url=None)
                        
            db.session.commit()

            other_user = User.signup(username="anotheruser", 
                                     email="anotheruser@test.com",
                                     password="testuser2",
                                     image_url=None)
            
            db.session.commit()

            self.testuser_id = self.testuser.id
            self.other_user_id = other_user.id


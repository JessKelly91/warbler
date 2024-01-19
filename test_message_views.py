"""Message View tests."""

# run these tests like:
#
#    FLASK_ENV=production python -m unittest test_message_views.py


import os
from unittest import TestCase

from models import db, Message, User


# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ['DATABASE_URL'] = "postgresql:///warbler-test"


# Now we can import app

from app import app, CURR_USER_KEY

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

# #added app context here based on error
with app.app_context():
    db.drop_all()
    db.create_all()

# Don't have WTForms use CSRF at all, since it's a pain to test

app.config['WTF_CSRF_ENABLED'] = False


class MessageViewTestCase(TestCase):
    """Test views for messages."""

    def setUp(self):
        """Create test client, add sample data."""
        #added app context here based on error
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
            

    def test_add_own_message(self):
        """Can use add a message?"""

        # Since we need to change the session to mimic logging in,
        # we need to use the changing-session trick:
        
        with self.client as c:
            with c.session_transaction() as sess:
                #added app context to try to solve error
                with app.app_context():
                    sess[CURR_USER_KEY] = self.testuser_id


            # Now, that session setting is saved, so we can have
            # the rest of ours test

            resp = c.post("/messages/new", data={"text": "Hello"})

            # Make sure it redirects
            self.assertEqual(resp.status_code, 302)

            msg = Message.query.one()
            self.assertEqual(msg.text, "Hello")

    def test_show_own_message(self):
        """Show a single message from the logged in user"""
        with self.client as c:
            with c.session_transaction() as sess:
                with app.app_context():
                    sess[CURR_USER_KEY] = self.testuser_id
                    
                    test_msg = Message(text="test message", 
                                       timestamp="2017-01-21 11:04:53.522807", 
                                       user_id=self.testuser_id)
            
                    db.session.add(test_msg)
                    db.session.commit()

                    self.test_msg_id = test_msg.id

            resp = c.get(f"/messages/{self.test_msg_id}")

            self.assertEqual(resp.status_code, 200)
            self.assertIn(b'<div class="message-area">', resp.data)
            self.assertIn(b"Delete", resp.data)

    def test_show_other_message(self):
        """Show a single message from anyone other than the logged in user"""

        with self.client as c:
            with c.session_transaction() as sess:
                with app.app_context():
                    sess[CURR_USER_KEY] = self.testuser_id
                    
                    test_msg = Message(text="test message", 
                                       timestamp="2017-01-21 11:04:53.522807", 
                                       user_id=self.other_user_id)
            
                    db.session.add(test_msg)
                    db.session.commit()

                    self.test_msg_id = test_msg.id

            resp = c.get(f"/messages/{self.test_msg_id}")

            self.assertEqual(resp.status_code, 200)
            self.assertIn(b'<div class="message-area">', resp.data)

            #Delete button only available on own messages
            self.assertNotIn(b"Delete", resp.data)


    def test_delete_own_message(self):
        """Testing deleting message"""
        with self.client as c:
            with c.session_transaction() as sess:
                 with app.app_context():
                    sess[CURR_USER_KEY] = self.testuser_id
                    
                    test_msg = Message(text="test message", 
                                       timestamp="2017-01-21 11:04:53.522807", 
                                       user_id=self.testuser_id)
            
                    db.session.add(test_msg)
                    db.session.commit()

                    self.test_msg_id = test_msg.id
                    
            resp = c.post(f"/messages/{self.test_msg_id}/delete")
            self.assertEqual(resp.status_code, 302)
            
            #test that looking up that message after deletion now raises an error
            resp2 = c.get(f"/messages/{self.test_msg_id}")
            self.assertEqual(resp2.status_code, 404)

#TO BE IMPLEMENTED
#def test_add_other_message
#def test_delete_other_message
#def test_logged_out_add_message
#def test_logged_out_delete_message

import unittest
from server import app
from model import db, connect_to_db #ALSO LIST NAME OF FUNCTIONS TO TEST
from flask import session
from model import * 
import server 
from test_data import * 

class TestGoalsSite(unittest.TestCase):
    """Test flask routes"""

    def setUp(self):
        """Code to run before every test."""

        self.client = server.app.test_client()
        server.app.config['TESTING'] = True

    def test_homepage_rendering(self):
        """Can we reach the homepage?"""

        result = self.client.get("/")
        self.assertIn(b"Make Some Goals Today", result.data)

    def test_register_page(self):
        """Can you see the registration page."""

        result = self.client.get("/register")
        self.assertIn(b"Registration", result.data)

    def test_render_login(self):
        """Can see login page."""

        result = self.client.get("/login")
        self.assertIn(b"LOG IN", result.data)

class TestGoalsDatabase(unittest.TestCase):
    """Tests test_goals database"""

    def setUp(self):
        """Code to run before every test."""

        app.config['TESTING'] = True
        self.client = app.test_client()

        connect_to_db(app)

        db.create_all()
        test_data()

        with self.client as c:
            with c.session_transaction() as sess:
                sess['email'] = 'mel@sample.com'
                sess['user_id'] = '1'

    def test_login(self):
        """Tests user log in"""

        with self.client as c:
            result = c.post('/login',
                            data={'email': 'mel@sample.com', 'password': 'password'},
                            follow_redirects=True
                            )
            self.assertEqual(result.status_code, 200)
            self.assertIn(b'What is life without goals?', result.data)

    def test_process_registration(self):
        """Tests continuation of registration with email in session"""

        with self.client as c:
            result = c.post('/register',
                            data={'f_name': 'tester',
                                  'l_name': 'unicorn',
                                  'email': 'testing@unicorn.com',
                                  'password': 'password1'},
                            follow_redirects=True)

        self.assertEqual(result.status_code, 200)
        self.assertIn(b'Make Some Goals Today!', result.data)

    def test_logout(self):
        """Tests logout route"""

        with self.client as c:
            with c.session_transaction() as sess:
                sess['email'] = 'mel@sample.com'
                sess['user_id'] = '1'

            result = self.client.get('/logout', follow_redirects=True)

            self.assertNotIn(b'email', sess)
            self.assertIn(b'Make Some Goals Today!', result.data)

    def tearDown(self):
        """Code to run after every test"""

        db.session.remove()
        db.drop_all()
        db.engine.dispose()


if __name__ == "__main__":
    unittest.main()
import unittest 
from server import app
from model import *
from calculations import * 
from metrics_helper import * 


class TracerTests(unittest.TestCase):
    """Test NextBook site"""
    def setUp(self):
        self.client = app.test_client()
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    def test_homepage(self):
        """Test homepage"""
        result = self.client.get("/")
        self.assertEqual(result.status_code, 200)
        self.assertIn(b"Welcome to Tracer!", result.data)

    def test_register_form(self):
        """Test register page intital rendering"""
        result = self.client.get('/register')
        self.assertEqual(result.status_code, 200)
        self.assertIn(b"<h1>Registration</h1>", result.data)

    def test_login_form(self):
        """Test login page intial rendering"""
        result = self.client.get('/login')
        self.assertEqual(result.status_code, 200)
        self.assertIn(b"Email", result.data)

    def test_language_change(self):
      """Test guest_user route"""
      result = self.client.get('/lang')
      self.assertEqual(result.status_code, 200)
      self.assertIn(b"Language/Idioma", result.data)


class TracerTestsDatabase(unittest.TestCase):

    def setUp(self):
        """Set up for database function testing"""

        #Get the Flask test client
        self.client = app.test_client()
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

        #connect to test database
        connect_to_db(app, db_uri='postgresql:///testdb') 

        #create the tables and add the sample data
        db.create_all()
        example_data()

        
    def tearDown(self):
        """Do at end of every test."""

        db.session.close()
        db.drop_all()

    def test_login_process(self):
      """Test if an exisiting user can login"""
      result = self.client.post('/login', 
                                  data={'email': '123@test.com', 
                                        'password': 'password' }, 
                                        follow_redirects=True)
      self.assertEqual(result.status_code, 200)
      self.assertIn(b"Welcome to Tracer!", result.data)

    def test_logout_session(self):
        """Sets session user_id, tests if user can log out"""
        with self.client as c:
            with c.session_transaction() as sess:
                sess['user_id'] = 1
        result = c.get('/logout', follow_redirects=True)
        self.assertEqual(result.status_code, 200)
        #redirects to homepage if successful, so we'll test for that
        self.assertIn(b"Welcome to Tracer", result.data)

    def test_user_profile(self):
      """Test User Profile"""
      with self.client as c:
        with c.session_transaction() as sess:
          sess['user_id'] = 1

      result = self.client.get('/user_profile')
      self.assertEqual(result.status_code, 200)
      self.assertIn(b"<h1>User Information</h1>", result.data)

    # def test_register_process(self):
    #   """Test if new user can register"""
    #   result = self.client.post('/register', data={'email': 'newuser@test.com', 
    #                                                 'password': 'password' }, 
    #                                                   follow_redirects=True)
    #   self.assertEqual(result.status_code, 200)
    #   #redirects to login page if successful, so we'll test for that
    #   self.assertIn(b"Transportation", result.data)

    def test_recs(self):
      """Recs rendered"""

      result = self.client.get('/recs')
      self.assertEqual(result.status_code, 200)
      self.assertIn(b"Recommendations", result.data) 

    # def test_adding_recs(self):
    #   """Test to add rating to db"""
    #   rating6 = Rec(rec_id=6, user_id=1, comment="I am vegan", rec_date="2019-11-27 03:44:48.075786")
    #   self.assertEqual(result.status_code, 200)
    #   self.assertIn(b"Recommendations", result.data) 

    # def test_score(self):
    #   """Test if an if user can generate final score"""

    #   result = self.client.get('/pollution_metrics')
    #   self.assertEqual(result.status_code, 200)
    #   #redirects to login page if successful, so we'll test for that
    #   self.assertIn(b"Score", result.data) 
          


      


if __name__ == "__main__": 

    unittest.main()
    init_app()



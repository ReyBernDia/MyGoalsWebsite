from sqlalchemy import func
from model import *
from server import app

def test_data():
    test_user()


def test_user():
    """Creates test user in test database"""

    test_user = Users(f_name = 'Melon', 
                      l_name = 'Melonly', 
                      email = 'mel@sample.com', 
                      password = 'password')
    db.session.add(test_user)
    db.session.commit()


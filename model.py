from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import asc, update

db = SQLAlchemy()

##############################################################################
# Model definitions

class Users(db.Model):
    """Registered users."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    f_name = db.Column(db.String(25), nullable=False)
    l_name = db.Column(db.String(25), nullable=True)
    email = db.Column(db.String(120), nullable=False)
    password = db.Column(db.String(128), nullable=False)

    def __repr__(self):
        return f"<Name: {self.f_name} {self.l_name} ID: {self.user_id}>"

class Goals(db.Model):
    """User goals"""

    __tablename__ = "goals"

    goal_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    u_goal = db.Column(db.String(200), nullable=False)

    user_goals = db.relationship("Users", 
                          backref=db.backref("goals"))

    def __repr__(self):
        return f"<goal_id: {self.goal_id} user_id: {self.user_id}>"

##############################################################################
# Helper functions

def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our PstgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///goals'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.
    from server import app
    connect_to_db(app)
    print("Connected to DB.")
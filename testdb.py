"""Models and database functions for Carbon Footprint Calculator"""

from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash



# This is the connection to the PostgreSQL database; we're getting this through
# the Flask-SQLAlchemy helper library. On this, we can find the `session`
# object, where we do most of our interactions (like committing, etc.)
db = SQLAlchemy()

################################################################################

class User(db.Model):

    """User of Carbon Footprint Calculator"""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    fname = db.Column(db.String(20), nullable=True, index=True)
    lname = db.Column(db.String(20), nullable=True, index=True)
    zipcode = db.Column(db.Integer, nullable=True, index=True)
    email = db.Column(db.String(70), nullable=True, unique=True, index=True)
    password_hash = db.Column(db.String(128))
    profile_created_date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
 #below our user model, we will create our hashing functions

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        """Helpful representation when printed"""

        return f"<User Info: user_id= {self.user_id}, name= {self.fname}, email={self.email}>"


class Metric(db.Model):

    """User pollution metrics"""

    __tablename__ = "metrics"

    metric_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    trans_metric = db.Column(db.Integer, nullable=True)
    energy_metric = db.Column(db.Integer, nullable=True)
    waste_metric = db.Column(db.Integer, nullable=True)
    food_metric = db.Column(db.Integer, nullable=True)
    clothing_metric = db.Column(db.Integer, nullable=True)
    created_date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)


    user = db.relationship("User",
                            backref=db.backref("metrics"))

    def __repr__(self):
        """Helpfull representation when printed"""

        return f"""< Metrics: 
                    trans_metric = {self.trans_metric}, 
                    energy_metric = {self.energy_metric}, 
                    waste_metric = {self.waste_metric}, 
                    food_metric = {self.food_metric},
                    clothing_metric = {self.clothing_metric}>
                """


class Rec(db.Model):
    """Recommendations table"""
    __tablename__ = "recs"

    rec_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    comment = db.Column(db.Text, nullable=True)
    rec_date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    user = db.relationship("User", 
                                backref=db.backref("recs"), 
                                order_by=rec_id)

    def __repr__(self):
        """Helpfull representation when printed"""
        return f"""<rec_date: {self.rec_date}, 
                    user_id: {self.user_id},
                    comment: {self.comment}>"""



################################################################################
##############################################################################
# Helper functions

def init_app():
    # So that we can use Flask-SQLAlchemy, we'll make a Flask app.
    from flask import Flask
    app = Flask(__name__)

    connect_to_db(app)
    print("Connected to DB.")

def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our PstgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///carboncalculator'
    app.config['SQLALCHEMY_ECHO'] = False
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

   init_app()

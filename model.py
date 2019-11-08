"""Models and database functions for Carbon Footprint Calculator"""

from flask_sqlalchemy import SQLAlchemy
import datetime
from datetime import datetime

# This is the connection to the PostgreSQL database; we're getting this through
# the Flask-SQLAlchemy helper library. On this, we can find the `session`
# object, where we do most of our interactions (like committing, etc.)
db = SQLAlchemy()

################################################################################

class User(db.Model):

    """User of Carbon Footprint Calculator"""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    fname = db.Column(db.String(20), nullable=True)
    lname = db.Column(db.String(20), nullable=True)
    zipcode = db.Column(db.Integer, nullable=True)
    email = db.Column(db.String(70), nullable=True, unique=True)
    password = db.Column(db.String(20), nullable=True)
    profile_created_date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def __repr__(self):
        """Helpful representation when printed"""

        return f"<User Info: user_id= {self.user_id}, name= {self.fname}, email={self.email}>"


class PollutionMetric(db.Model):

    """User pollution metrics"""

    __tablename__ = "pollution_metrics"

    metric_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    trans_metric = db.Column(db.Integer, nullable=True)
    energy_metric = db.Column(db.Integer, nullable=True)
    waste_metric = db.Column(db.Integer, nullable=True)
    food_metric = db.Column(db.Integer, nullable=True)
    created_date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def __repr__(self):
        """Helpfull representation when printed"""

        return f"""<Pollution metric: 
                    trans_metric = {self.trans_metric}, 
                    energy_metric = {self.energy_metric}, 
                    waste_metric = {self.waste_metric}, 
                    food_metric = {self.food_metric}
                """

    user = db.relationship("User",
                            backref=db.backref("pollution_metrics"))

################################################################################
def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our PstgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///carboncalculator'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)

if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from server import app
    connect_to_db(app)
    print("Connected to DB.")



















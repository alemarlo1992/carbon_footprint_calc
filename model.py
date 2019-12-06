"""Models and database functions for Carbon Footprint Calculator"""

from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.inspection import inspect
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
#test samples 
def example_data():
    """Populate a databse with sample data for testing purposes."""

    db.create_all()


    #Empty out data from previous runs
    User.query.delete()
    Metric.query.delete()
    Rec.query.delete()

    #Add sample users, books, and ratings

    #sample users
    user1 = User(user_id=1, email='123@test.com', password_hash='password')
    user2 = User(user_id=2, email='456@test.com', password_hash='password')
    user3 = User(user_id=3, email='789@test.com', password_hash='password')
    user4 = User(user_id=4, email='987@test.com', password_hash='password')
    user5 = User(user_id=5, email='654@test.com', password_hash='password')

    user1_metric = Metric(metric_id=1, 
                            user_id=1, 
                            trans_metric=10, 
                            energy_metric=10,
                            waste_metric=2,
                            food_metric=2, 
                            clothing_metric=10, 
                            created_date="2019-11-27 03:43:47.907932")

    user2_metric = Metric(metric_id=2, 
                            user_id=2, 
                            trans_metric=15, 
                            energy_metric=10,
                            waste_metric=5,
                            food_metric=2, 
                            clothing_metric=10,
                            created_date="2019-11-27 03:43:47.907932")

    user3_metric = Metric(metric_id=3, 
                            user_id=3, 
                            trans_metric=20, 
                            energy_metric=10,
                            waste_metric=2,
                            food_metric=2, 
                            clothing_metric=10,
                            created_date="2019-11-27 03:43:47.907932")

    user4_metric = Metric(metric_id=4, 
                            user_id=4, 
                            trans_metric=10, 
                            energy_metric=20,
                            waste_metric=2,
                            food_metric=2, 
                            clothing_metric=15,
                            created_date="2019-11-27 03:43:47.907932")

    user5_metric = Metric(metric_id=5, 
                            user_id=5, 
                            trans_metric=10, 
                            energy_metric=30,
                            waste_metric=2,
                            food_metric=2, 
                            clothing_metric=15,
                            created_date="2019-11-27 03:43:47.907932")

    user1_rec = Rec(rec_id=1, 
                        user_id=1, 
                        comment="I eat veggies", 
                        rec_date="2019-11-27 03:44:48.075786")

    user2_rec = Rec(rec_id=2, 
                        user_id=2, 
                        comment="I drive a tesla", 
                        rec_date="2019-11-27 03:44:48.075786")
    user3_rec = Rec(rec_id=3, 
                        user_id=3, 
                        comment="I drive a prius", 
                        rec_date="2019-11-27 03:44:48.075786")
    user4_rec = Rec(rec_id=4, 
                        user_id=4, 
                        comment="I take public trans", 
                        rec_date="2019-11-27 03:44:48.075786")
    user5_rec = Rec(rec_id=5, 
                        user_id=5, 
                        comment="I'm vegan", 
                        rec_date="2019-11-27 03:44:48.075786")

     #Add all to session and commit
    db.session.add_all([user1, user2, user3, user4, user5, user1_metric, user2_metric,
                        user3_metric, user4_metric, user5_metric, user1_rec, user2_rec, 
                        user3_rec, user4_rec, user5_rec])

    db.session.commit()


################################################################################
def connect_to_db(app, db_uri='postgresql:///carboncalculator'):
    """Connect the database to our Flask app."""

    # Configure to use our PstgreSQL database
    # Configure to use our PostgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    db.app = app
    db.init_app(app)

if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.
    from server import app
    # init_app()
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False















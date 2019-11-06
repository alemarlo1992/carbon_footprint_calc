"""Carbon Footprint Calculator"""

from jinja2 import StrictUndefined

from flask import Flask, render_template, redirect, request, flash, session
from flask_debugtoolbar import DebugToolbarExtension

from model import User, PollutionMetrics, connect_to_db, db

import calculations


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABCDEFG"

# Normally, if you use an undefined variable in Jinja2, it fails
# silently. This is horrible. Fix this so that, instead, it raises an
# error.
app.jinja_env.undefined = StrictUndefined

@app.route('/')
def index():
    """Homepage."""
    return render_template("homepage.html")

@app.route('/trans_metrics', methods=[GET])
def transportation():

    user_zipcode = request.args.get("user_zipcode")
    num_people = request.args.get("num_people")
    miles_per_week = request.args.get("miles_per_week")
    vehicle_num = request.args.get("vehicle_num")
    air_miles_yr = request.args.get("air_miles_yr")

    
if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    # make sure templates, etc. are not cached in debug mode
    app.jinja_env.auto_reload = app.debug

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(port=5000, host='0.0.0.0')

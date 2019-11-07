"""Carbon Footprint Calculator"""

from jinja2 import StrictUndefined

from flask import Flask, render_template, redirect, request, flash, session
from flask_debugtoolbar import DebugToolbarExtension

from model import User, PollutionMetrics, connect_to_db, db

from calculations import vehicle_emissions, public_trans, air_travel, energy


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

@app.route('/register', methods=["GET"])
def registration_form(): 
    """Render template registration.html"""
    return render_template("registration.html")

@app.route('/register', methods=["POST"])
def registration_process(): 
    fname = request.form["fname"]
    lname = request.form["lname"]
    zipcode = request.form["user_zipcode"]
    email = request.form["email"]
    password = request.form["password"]

    new_user = User(fname=fname, 
                    lname=lname,
                    zipcode=zipcode, 
                    email=email,
                    password=password)

    db.session.add(new_user)
    db.session.commit()

    return redirect("/")

@app.route('/login', methods=["GET"])
def login(): 
    """Render template login.html"""
    return render_template("login.html")

@app.route('/login', methods=["POST"])
def login_process(): 
    email = request.form["email"]
    password = request.form["password"]

    user = User.query.filter_by(email=email).first()

    if not user:
        # flash("No such user")
        return redirect("/login")

    if user.password != password:
        # flash("Incorrect password")
        return redirect("/login")

    session["user_id"] = user.user_id

    # flash("Logged in")
    return redirect("trans_metrics")

@app.route("/logout")
def logout():
    #delete info from session
    session.pop('user_id')
    #From solution: del session["user_id"]

    return redirect('/')

@app.route("/guest_user")
def guest(): 
    guest = User()
    db.session.add(guest)
    db.session.commit()


@app.route('/trans_metrics', methods=["GET"])
def transportation():
    """Transporation form"""

    return render_template("trans_metrics.html")

@app.route('/get_trans_metrics', methods=["POST"])
def get_trans_metric():
    """Get user form inputs from transportation & calculate their trans_metrics emissions"""

    miles_per_week = request.form["miles_per_week"]
    vehicle_num = request.form["vehicle_num"]
    air_miles_yr = request.form["air_miles_yr"]

    print("ITS HERE !!!!!!!!!!!!!!!!!!!!")
    print(vehicle_emissions(vehicle_num, miles_per_week))
    print(public_trans(miles_per_week))
    print(air_travel(air_miles_yr))
    print("ITS HERE !!!!!!!!!!!!!!!!!!!!")

    # if user is logedin 
    # save their metrics 
    # else 
    # still save them 

    return redirect('/energy_metrics')

@app.route('/energy_metrics', methods=["GET"])
def energy_metrics():
    """Energy form inputs"""

    return render_template("energy_metrics.html")

@app.route('/get_energy_metrics', methods=["POST"])
def get_energy_metrics():
    """Get user form inputs from energy form & calculate their energy_metrics emissions"""
    user_zipcode = request.form["user_zipcode"]
    electricity_amount = request.form["electricity_amount"]
    natural_gas_amount = request.form["natural_gas_amount"]
    fuel_oil_amount = request.form["fuel_oil_amount"]
    propane_amount = request.form["propane_amount"]

    print("ITS HERE !!!!!!!!!!!!!!!!!!!!")
    print(energy(user_zipcode, natural_gas_amount, electricity_amount, fuel_oil_amount, propane_amount))
    print("ITS HERE !!!!!!!!!!!!!!!!!!!!")

    return redirect('/waste_metrics')

# @app.route('/waste_metrics')
# def waste_metrics():
#     """waste_metrics Energy Inputs"""

#     return render_template("waste_metrics.html")




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

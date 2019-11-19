"""Carbon Footprint Calculator"""

from jinja2 import StrictUndefined

from flask import Flask, render_template, redirect, request, flash, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension
# from flask.ext.babel import Babel, gettext, ngettext, lazy_gettext

from model import User, Metric, Rec, connect_to_db, db
from calculations import energy, food, percentage_difference
from metrics_helper import transportation_conditional, waste_conditional



app = Flask(__name__)
# app.config.from_pyfile('mysettings.cfg')
# babel = Babel(app)


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

    #Adding new user to users data table 
    new_user = User(fname=fname, 
                    lname=lname,
                    zipcode=zipcode, 
                    email=email,
                    password=password)

    db.session.add(new_user)
    db.session.commit()
    session['user_id'] = new_user.user_id


    return redirect("/pollution_metrics")


@app.route('/user_data.json')
def user_data():
    user_metric = Metric.query.filter_by(user_id=session['user_id']).all()
    for m in user_metric: 
        trans_metric = m.trans_metric
        energy_metric = m.energy_metric
        waste_metric = m.waste_metric
        food_metric = m.food_metric

    data_dict = {
                    "labels": [
                        "Transportation",
                        "Energy",
                        "Waste",
                        "Food"
                    ],
                    "datasets": [
                        {
                            "data": [trans_metric, energy_metric, waste_metric, food_metric],
                            "backgroundColor": [
                                "#FF6384",
                                "#36A2EB",
                                "#FFCE56",
                                "#63FFDE"
                            ],
                    "hoverBackgroundColor": [
                        "#FF6384",
                        "#36A2EB",
                        "#FFCE56",
                        "#63FF90"
                    ]
                }]
        }
    return jsonify(data_dict)

@app.route('/user_profile')
def user_profile():
    """User profile information"""
    user_metric = Metric.query.filter_by(user_id=session['user_id']).all()
    for m in user_metric: 
        score = m.trans_metric + m.energy_metric + m.waste_metric + m.food_metric

    avg_comparison = int(percentage_difference(score))
    return render_template("users.html", score=score, avg_comparison=avg_comparison)


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
        flash("No such user")
        return redirect("/login")

    if user.password != password:
        flash("Incorrect password")
        return redirect("/login")

    session["user_id"] = user.user_id

    flash("Logged in")
    return redirect("/pollution_metrics")

@app.route("/logout")
def logout():
    #delete info from session
    session.pop('user_id')
    #From solution: del session["user_id"]

    return redirect('/')

@app.route("/guest_user")
def guest(): 
    """Guest user is being added to user data table and to the session"""
    fname = "Guest"
    user = User(fname=fname)

    db.session.add(user)
    
    db.session.commit()

    session['user_id'] = user.user_id
    return redirect('/pollution_metrics')


@app.route('/pollution_metrics', methods=["GET"])
def transportation():
    """Transporation form"""

    return render_template("pollution_metrics.html")

@app.route('/pollution_metrics', methods=["POST"])
def get_pollution_metric():
    """Get user form inputs from transportation & calculate their trans_metrics emissions"""
    # metrics = dict(request.form)
    # print(metrics)

    transportation = request.form["transportation"]
    pt_miles_per_week = request.form["pt_miles_per_week"]
    air_miles_yr = request.form["air_miles_yr"]
    #set default value for user 

    vehicle_num = request.form["vehicle_num"]
    mi_wk_1 = request.form["mi_wk_1"]
    mi_wk_2 = request.form["mi_wk_2"]
    mi_wk_3 = request.form["mi_wk_3"]
    mi_wk_4 = request.form["mi_wk_4"]
    mi_wk_5 = request.form["mi_wk_5"]

    user_zipcode = request.form["user_zipcode"]
    electricity_amount = request.form["electricity_amount"]
    natural_gas_amount = request.form["natural_gas_amount"]
    fuel_oil_amount = request.form["fuel_oil_amount"]
    propane_amount = request.form["propane_amount"]

    num_people = request.form["num_people"]
    metal_waste = request.form["metal_waste"]
    plastic_waste = request.form["plastic_waste"]
    glass_waste = request.form["glass_waste"]

    meat_serv = request.form["meat_serv"]
    grain_serv = request.form["grain_serv"]
    dairy_serv = request.form["dairy_serv"]
    fruit_serv = request.form["fruit_serv"]


    """Transportation metric"""
    trans_metric = transportation_conditional(transportation,
                                                num_people,
                                                pt_miles_per_week,
                                                air_miles_yr,
                                                mi_wk_1, 
                                                mi_wk_2, 
                                                mi_wk_3,
                                                mi_wk_4,
                                                mi_wk_5, 
                                                vehicle_num)


    """Energy metric"""
    energy_metric = energy(user_zipcode, 
                            natural_gas_amount,
                            electricity_amount, 
                            fuel_oil_amount, 
                            propane_amount)


    """Waste metric"""
    waste_metric = waste_conditional(num_people, 
                                        metal_waste, 
                                        plastic_waste, 
                                        glass_waste)
  

    """Food metric"""
    food_metric = food(meat_serv, 
                        grain_serv, 
                        dairy_serv, 
                        fruit_serv)

    #Assigning corresponding pollution metrics for each user in the polution_metrics table 
    pollution_metric = Metric(user_id=session['user_id'], 
                        trans_metric=trans_metric,  
                        energy_metric= energy_metric,
                        waste_metric=waste_metric,
                        food_metric=food_metric)
    #Adding corresponding metrics to db table 
    db.session.add(pollution_metric)
    #commiting those changes 
    db.session.commit()

    return redirect('/score')


@app.route('/data.json')
def datajs():
    user_metric = Metric.query.filter_by(user_id=session['user_id']).all()
    
    for m in user_metric: 
        trans_metric = m.trans_metric
        energy_metric = m.energy_metric
        waste_metric = m.waste_metric
        food_metric = m.food_metric

    data_dict = {
                    "labels": [
                        "Transportation",
                        "Energy",
                        "Waste",
                        "Food"
                    ],
                    "datasets": [
                        {
                            "data": [trans_metric, energy_metric, waste_metric, food_metric],
                            "backgroundColor": [
                                "#FF6384",
                                "#36A2EB",
                                "#FFCE56",
                                "#63FFDE"
                            ],
                    "hoverBackgroundColor": [
                        "#FF6384",
                        "#36A2EB",
                        "#FFCE56",
                        "#63FF90"
                    ]
                }]
        }
    return jsonify(data_dict)


@app.route('/score', methods=["GET"])
def score():   
    """Render template score.html"""
    user_metric = Metric.query.filter_by(user_id=session['user_id']).all()
    for m in user_metric: 
        score = m.trans_metric + m.energy_metric + m.waste_metric + m.food_metric
    
    avg_comparison = int(percentage_difference(score))
    print(avg_comparison)

    if avg_comparison > 30: 
        flash('''Congratulations!
                     You are an awesome HUMAN!
                     Your input in our recommendations section would 
                     be greatly appreciated so, other humans can follow your 
                     footprint. ''')
    else: 
        flash('Find ways reduce your footprint in our recommendations section!')
       
    return render_template("score.html", 
                                score=score, 
                                avg_comparison=avg_comparison)

@app.route('/recs', methods=["GET"])
def comments(): 
    """Render recommendations.html"""
    comments = Rec.query.order_by(Rec.rec_date.desc()).all()
    
    return render_template("recommendations.html", comments=comments)


@app.route('/recs', methods=["POST"])
def get_comments(): 
    """Save user comments in recs datatable"""
    comment = request.form["comment"]

    add_comment = Rec(user_id=session['user_id'], comment=comment)
    db.session.add(add_comment)
    db.session.commit()

    return redirect('/recs')



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

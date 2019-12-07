"""Carbon Footprint Calculator"""

from jinja2 import StrictUndefined

from flask import Flask, render_template, redirect, request, flash, session, jsonify, g 
from flask_debugtoolbar import DebugToolbarExtension
from flask_babel import Babel, gettext 

from model import User, Metric, Rec, connect_to_db, db
from calculations import *
from metrics_helper import *

app = Flask(__name__)
#Sets the locale to english 
app.config['BABEL_DEFAULT_LOCALE'] = 'en'
babel = Babel(app)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABCDEFG"

# Normally, if you use an undefined variable in Jinja2, it fails
# silently. This is horrible. Fix this so that, instead, it raises an
# error.
app.jinja_env.undefined = StrictUndefined

#------------------------------------------------------------------------------#
"""Babel localselector will be used to return the users preferred languague"""
@babel.localeselector
def get_locale():
    """Return desired language, either english or spanish"""
    
    if session.get('lang') == 'es':
        return 'es'
    else: 
        return 'en'


#------------------------------------------------------------------------------#
@app.route('/')
def index():
    """Homepage."""
    
    return render_template('homepage.html')


#------------------------------------------------------------------------------#
@app.route('/lang')
def get_lang(): 
    """Render template lang.html"""
    return render_template('lang.html')

@app.route('/lang', methods=["POST"])
def change_lang(): 
    """Get user preferred languague, either spanish or english"""

    lang = request.form["lang"]
    languague = get_user_lang(lang)
    return redirect('/')


#------------------------------------------------------------------------------#
@app.route('/register', methods=["GET"])
def registration_form(): 
    """Render template registration.html"""

    return render_template('registration.html')

@app.route('/register', methods=["POST"])
def registration_process(): 
    """Registering user and saving form inputs to users datatable"""

    fname = request.form["fname"]
    lname = request.form["lname"]
    email = request.form["email"]
    password_hash = request.form["password"]

    # Adding new user to users data table 
    new_user = User(fname=fname, 
                    lname=lname,
                    email=email,
                    password_hash=password_hash)

    new_user.set_password(password_hash)

    db.session.add(new_user)
    db.session.commit()
    session['user_id'] = new_user.user_id


    return redirect('/pollution_metrics')


#------------------------------------------------------------------------------#
@app.route('/user_data.json')
def user_data():
    """Metrics for user in session"""

    try:
        user_metric = Metric.query.filter_by(user_id=session['user_id']).all()
        user_data = user_metrics(user_metric)
        return jsonify(user_data)
    except:
        return jsonify("User has not calculated carbon footprint")

@app.route('/user_profile')
def user_profile():
    """render User profile information"""

    try:
        user_metric = Metric.query.filter_by(user_id=session['user_id']).all()
        score = get_score(user_metric)
        avg_comparison = int(percentage_difference(score))
        user_comments = Rec.query.filter_by(user_id=session['user_id']).all()

        return render_template("users.html", 
                                score=score, 
                                avg_comparison=avg_comparison, 
                                user_comments=user_comments)
    except:
        flash("User has not calculated carbon footprint")
        return redirect("/")
        

#------------------------------------------------------------------------------#
@app.route('/settings', methods=["GET"])
def settings(): 
    """Render template settings.html"""

    user = User.query.get(session['user_id'])

    return render_template('settings.html', user=user)


@app.route('/settings', methods=["POST"])
def change_settings(): 
    """Change user settings and commit session to database"""
    try:
        user = User.query.filter_by(user_id=session['user_id']).first()

        fname = request.form["fname"]
        lname = request.form["lname"]
        email = request.form["email"]
        password_hash = request.form["password"]

        user.fname = fname 
        user.lname = lname 
        user.email = email 
        user.password_hash = password_hash

        db.session.commit()

        return redirect('/user_profile')
    except:

        return redirect('/')


#------------------------------------------------------------------------------#
@app.route('/login', methods=["GET"])
def login(): 
    """Render template login.html"""

    return render_template('login.html')


@app.route('/login', methods=["POST"])
def login_process(): 
    """User login process"""

    email = request.form["email"]
    password_hash = request.form["password"]

    user = User.query.filter_by(email=email).first()

    if user and user.check_password(password_hash):

        session["user_id"] = user.user_id

        flash(gettext('Logged in'))
        return redirect('/')
    else:
        flash(gettext('You have entered the wrong password!'))
        return redirect('/login')

#------------------------------------------------------------------------------#
@app.route("/logout")
def logout():
    """Log out user from session"""

    #delete info from session
    del session["user_id"]
    flash(gettext('Logged Out.'))
    return redirect('/')

#------------------------------------------------------------------------------#
@app.route("/guest_user")
def guest(): 
    """Guest user is being added to user data table and to the session"""

    fname = "Guest"
    user = User(fname=fname)

    db.session.add(user)
    
    db.session.commit()

    session['user_id'] = user.user_id
    return redirect('/pollution_metrics')

#------------------------------------------------------------------------------#
@app.route('/pollution_metrics', methods=["GET"])
def transportation():
    """Render transporation form"""

    return render_template('pollution_metrics.html')


@app.route('/pollution_metrics', methods=["POST"])
def get_pollution_metric():
    """Get user form inputs from transportation & calculate their trans_metrics emissions"""

    transportation = request.form["transportation"]
    pt_miles_per_week = request.form["pt_miles_per_week"]
    air_miles_yr = request.form["air_miles_yr"]

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

    clothes = request.form["clothes"]

    # Transportation metric
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

    # Energy metric
    energy_metric = energy(user_zipcode, 
                            natural_gas_amount,
                            electricity_amount, 
                            fuel_oil_amount, 
                            propane_amount)

    # Waste metric
    waste_metric = waste_conditional(num_people, 
                                        metal_waste, 
                                        plastic_waste, 
                                        glass_waste)
  
    # Food metric
    food_metric = food(meat_serv, grain_serv, dairy_serv, fruit_serv)

    # Clothing metric
    clothing_metric = clothing(clothes)

    #Assigning corresponding pollution metrics for each user in the polution_metrics table 
    pollution_metric = Metric(user_id=session['user_id'], 
                        trans_metric=trans_metric,  
                        energy_metric= energy_metric,
                        waste_metric=waste_metric,
                        food_metric=food_metric,
                        clothing_metric=clothing_metric)
     
    db.session.add(pollution_metric) # Adding corresponding metrics to db table 

    db.session.commit() # Commiting those changes 

    return redirect('/score')

#------------------------------------------------------------------------------#
@app.route('/data.json')
def datajs():
    """Metrics rendered to user_profile"""

    try: 
        user_metric = Metric.query.filter_by(user_id=session['user_id']).all()
        
        user_data = user_metrics(user_metric)

        return jsonify(user_data)
    except:
        return jsonify("User has not calculated carbon footprint")

#------------------------------------------------------------------------------#
@app.route('/score', methods=["GET"])
def score():   
    """Render template score.html"""
    user_metric = Metric.query.filter_by(user_id=session['user_id']).all()
    score = get_score(user_metric)
    avg_comparison = int(percentage_difference(score))
    avg_comp_flash = avg_flash_msgs(avg_comparison)
       
    return render_template("score.html", 
                                score=score, 
                                avg_comparison=avg_comparison)

#------------------------------------------------------------------------------#
@app.route('/recs', methods=["GET"])
def comments(): 
    """Render recommendations.html"""

    comments = Rec.query.order_by(Rec.rec_date.desc()).all()
    print(comments)

    return render_template("recommendations.html", comments=comments)


@app.route('/recs', methods=["POST"])
def get_comments(): 
    """Save user comments in recs datatable"""
    comment = request.form["comment"]

    add_comment = Rec(user_id=session['user_id'], comment=comment)
    db.session.add(add_comment)
    db.session.commit()

    return redirect('/recs')

#------------------------------------------------------------------------------#
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

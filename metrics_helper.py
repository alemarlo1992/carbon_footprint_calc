from calculations import vehicle_emissions, public_trans, air_travel, waste
from flask import flash, redirect, session
from flask_babel import Babel, gettext

#------------------------------------------------------------------------------#
"""Transportation conditions"""
def transportation_conditional(transportation,
                                num_people,
                                pt_miles_per_week,
                                air_miles_yr,
                                mi_wk_1, 
                                mi_wk_2, 
                                mi_wk_3,
                                mi_wk_4,
                                mi_wk_5, 
                                vehicle_num):
    """Obtain the transporation metric from user based on conditionals"""
    trans_metric = air_travel(air_miles_yr)
    if transportation == 'yes':
        public_trans_total = round((public_trans(num_people, pt_miles_per_week)), 2)
        trans_metric += public_trans_total
    elif transportation == 'no':
        veh_emission_total = round(vehicle_emissions(vehicle_num, 
                                                        mi_wk_1, 
                                                        mi_wk_2, 
                                                        mi_wk_3,
                                                        mi_wk_4,
                                                        mi_wk_5), 2)
        trans_metric += veh_emission_total
    else: 
        veh_emission_total = round(vehicle_emissions(vehicle_num, 
                                                        mi_wk_1, 
                                                        mi_wk_2, 
                                                        mi_wk_3,
                                                        mi_wk_4,
                                                        mi_wk_5), 2)
        public_trans_total = round((public_trans(num_people, pt_miles_per_week)), 2)
        trans_metric += veh_emission_total + public_trans_total 

    return trans_metric

#------------------------------------------------------------------------------#

"""Waste conditions"""
def waste_conditional(num_people, metal_waste, plastic_waste, glass_waste): 
    """Obtain waste metric from user, based on conditionals"""
    #Checking if the user recycles aluminum, plastic, and glass
    waste_metric = waste(num_people)
    #Reductions in lb/yr, data from EPA. 
    metal_reduction = -89.38
    plastic_reduction = -35.56
    glass_reduction = -25.39
    tons_conversion = 0.0005

    if metal_waste == 'yes':
        waste_metric += metal_reduction

    if plastic_waste == 'yes':
        waste_metric += plastic_reduction

    if glass_waste == 'yes':
        waste_metric += glass_reduction

    waste_metric = round((waste_metric * tons_conversion), 3)

    return waste_metric

#------------------------------------------------------------------------------#

def user_login(user, password_hash):
    """User email and password verification"""
    if not user:
        flash("No such user")
        return redirect("/login")

    if user.password_hash != password_hash:
        flash("Incorrect password")
        return redirect("/login")

#------------------------------------------------------------------------------#

def user_metrics(user_metric):
    """User metrics for chart.js"""
    for m in user_metric: 
        trans_metric = m.trans_metric
        energy_metric = m.energy_metric
        waste_metric = m.waste_metric
        food_metric = m.food_metric
        clothing_metric = m.clothing_metric

    data_dict = {
                    "labels": [
                        gettext("Transportation"),
                        gettext("Energy"),
                        gettext("Waste"),
                        gettext("Food"), 
                        gettext("Clothing")
                    ],
                    "datasets": [
                        {
                            "data": [trans_metric, energy_metric, waste_metric, food_metric, clothing_metric],
                            "backgroundColor": [
                                "#FF6384",
                                "#36A2EB",
                                "#FFCE56",
                                "#63FFDE", 
                                '#CC65FE'
                            ],
                    "hoverBackgroundColor": [
                        "#FF6384",
                        "#36A2EB",
                        "#FFCE56",
                        "#63FF90", 
                        '#CC65FE'
                    ]
                }]
        }

    return data_dict

#------------------------------------------------------------------------------#

def get_score(user_metric):
    """Calculates user score"""
    for m in user_metric: 
        score = m.trans_metric + m.energy_metric + m.waste_metric + m.food_metric + m.clothing_metric
        return score

#------------------------------------------------------------------------------#

def avg_flash_msgs(avg_comparison):
    """Flash messages based on comparison with average american"""
    if avg_comparison > 30: 
        flash(gettext('''Congratulations!
                     You are an awesome HUMAN! Add a recommendation so 
                     other humans can follow your footprint. '''))
    else: 
        flash(gettext('Find ways reduce your footprint in our recommendations section!'))

#------------------------------------------------------------------------------#

def get_user_lang(lang):
    """Based on form input commit add language to session"""
    if lang == "English": 
        session['lang'] = 'en'
    else: 
        session['lang'] = 'es'
        
#------------------------------------------------------------------------------#





















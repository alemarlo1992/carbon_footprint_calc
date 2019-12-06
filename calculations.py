"""Calculations applied to the pollution metrics"""

from RawData.zipcodeData import get_zipcodes
import statistics

#------------------------------------------------------------------------------#
"""Transportation metric calculation"""
def vehicle_emissions(vehicle_num, 
                        mi_wk_1, 
                        mi_wk_2, 
                        mi_wk_3,
                        mi_wk_4,
                        mi_wk_5):
    """Calculates the emissions released due to vehicle use per year in tons/yr"""
    # 52.14 = weeks/yr, 21.6 = Average household fuel, 19.6 = lb of CO2 emitted/yr, 1.01 = lb of other gases /yr 
    mi_for_veh = [int(mi_wk_1), int(mi_wk_2), int(mi_wk_3), int(mi_wk_4), int(mi_wk_5)]
    mi_list = []
    for miles in mi_for_veh: 
        if miles > 0: 
            mi_list.append(miles)

    avg_miles = sum(mi_list)/ len(mi_list)

    veh_num = int(vehicle_num) 

    emission_lb = round((((veh_num * avg_miles * 52.14) / 21.6) * 19.6 * 1.01), 2)
    print(emission_lb)

    vehicle_emission_ton = round((emission_lb * 0.0005), 2)


    return vehicle_emission_ton

#------------------------------------------------------------------------------#

def public_trans(num_people, pt_miles_per_week):
    """Calculated the emissions released due to public trans in tons/yr"""
    # y = mx + b => parameters calculated from coolclimate.org 
    public_trans_emission_ton = round((int(num_people) *(0.0002 * int(pt_miles_per_week) * 52.14 + 0.0016)), 2)

    return public_trans_emission_ton

#------------------------------------------------------------------------------#

def air_travel(air_miles_yr):
    """Calculates the emissions released due to air travel per year in tons/yr"""
    # y = mx + b => parameters calculated from coolclimate.org 
    if air_miles_yr == None:
        travel_emission_ton = 0
    else:
        travel_emission_ton = round((0.0005 * int(air_miles_yr) - 0.0022), 2)

    return travel_emission_ton

#------------------------------------------------------------------------------#

"""Energy Metrics calculation"""
def energy(user_zipcode, natural_gas_amount, electricity_amount, fuel_oil_amount, propane_amount): 
    """Calculates the emissions released due to energy per year in tons/yr"""
    # y = mx + b => parameters calculated from coolclimate.org 
    zipcode_dict = get_zipcodes() #make function from zipcodeData.py a variable to access values 
    region_co2 = zipcode_dict[user_zipcode] #gets emissions by zipcode
    emission_factor = int(region_co2) / 1000 #conversion factor per household
    # $10.68 = natural gas cost, 119.58 = pounds of CO2 / thousand cubic ft of natural gas, 12 mo/yr
    natural_gas_emission = round(((int(natural_gas_amount) / 10.68) * 119.58 * 12), 2)

    # $0.1188 = cost per KWh, emission_factor comes from zipcode data,12 mo/yr
    electricity_emission = round(((int(electricity_amount) / 0.1188) * emission_factor * 12), 2)

    #  $4.02 = fuel oil cost, 22.61 = fuel emission factor, 12 mo/yr
    fuel_emission = round(((int(fuel_oil_amount) / 4.02) * 22.61 * 12), 2)

    # $2.47 = propane cost, 12.43 = propane emission factor, 12 mo/yr 
    propane_emission = round(((int(propane_amount) / 2.47) * 12.43 * 12), 2)

    total_energy_emission_lb = round((natural_gas_emission + electricity_emission + fuel_emission + propane_emission), 2)

    #conversion from lb to ton 
    total_energy_emission_ton = round((total_energy_emission_lb * 0.0005), 2)

    return total_energy_emission_ton

#------------------------------------------------------------------------------#

"""Waste Metrics calculation"""
def waste(num_people): 
    """Calculates the emissions released due to waste per year in tons/yr"""
    waste_emission_lb = round((int(num_people) * 692), 2)

    return waste_emission_lb

#------------------------------------------------------------------------------#

"""Food Metrics calculation"""
def food(meat_serv, grain_serv, dairy_serv, fruit_serv):
    """Calculates the emissions released due to food consumption per year in tons/yr"""
    # y = mx + b => parameters calculated from coolclimate.org 
    meat_emission = round((2.131 * int(meat_serv) + 0.005), 2)
    grain_emission = round((0.40 * int(grain_serv) - 0.01), 2)
    dairy_emission = round((0.88 * int(dairy_serv)), 2)
    fruit_emission = round((0.435 * int(fruit_serv) - 0.02), 2)

    total_food_emission_ton = meat_emission + grain_emission + dairy_emission + fruit_emission

    return round(total_food_emission_ton, 2)

#------------------------------------------------------------------------------#

"""Clothing Metrics calculation"""
def clothing(clothes):
    """Calculates the emissions released due to clothing purchase per year in tons/yr"""
    # y = mx + b => parameters calculated from coolclimate.org 
    clothes_emission = round((0.0016 * int(clothes) + 0.0003), 2)

    return clothes_emission
#------------------------------------------------------------------------------#

"""Percentage Difference Calculation"""
def percentage_difference(score):
    """Calculated the percentage difference between average American & user"""
    avg_american = 44.09 #Calculated using average parameters. 
    if score < avg_american: 
        percentage_diff = abs(avg_american - score) / ((avg_american + score) / 2) * 100
    else: 
        percentage_diff = - abs(avg_american - score) / ((avg_american + score) / 2) * 100

    return percentage_diff














































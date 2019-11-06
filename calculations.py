"""Calculations applied to the pollution metrics"""

from RawData.zipcodeData import get_zipcodes


"""Transportation metric"""
# print(get_zipcodes())
# number_of_vehicles = float(input('Enter amount of vehicles your household owns: '))
# miles_per_week = float(input('Miles that you travel per week: '))
# travel_miles_yr = float(input('How many miles did you air travel this year?: '))

def vehicle_emissions(number_of_vehicles, miles_per_week):
    
    # 52.14 = weeks/yr, 21.6 = Average household fuel, 19.6 = lb of CO2 emitted/yr, 1.01 = lb of other gases /yr 
    emission_lb = round((((number_of_vehicles * miles_per_week * 52.14) / 21.6) * 19.6 * 1.01), 2)
    # conversion from lb to ton 
    vehicle_emission_ton = round((emission_lb * 0.0005), 2)

    return vehicle_emission_ton

# vehicle_emissions(number_of_vehicles, miles_per_week)


def public_trans(miles_per_week):

    # y = mx + b => parameters calculated from coolclimate.org 
    public_trans_emission_ton = round((0.0002 * miles_per_week * 52.14 + 0.0016), 2)

    return public_trans_emission_ton

# public_trans(miles_per_week)


def air_travel(travel_miles_yr):

    travel_emission_ton = round((0.0005 * travel_miles_yr - 0.0022), 2)

    return travel_emission_ton

# air_travel(travel_miles_yr)

"""Energy Metrics"""
user_zipcode = input('Zipcode: ')
natural_gas_amount = float(input('How much do you pay for Natural gas per month?: '))
electricity_amount = float(input('How much do you pay for electrity per month?: '))
fuel_oil_amount = float(input('How much do you pay for fuel per month?: '))
propane_amount = float(input('How much do you pay for propane per month?: '))
def energy(user_zipcode, natural_gas_amount, electricity_amount, fuel_oil_amount, propane_amount): 

    region_co2 = zipcodes_co2[zipcode]
    emission_factor = int(region_co2) / 1000
    # $10.68 = natural gas cost, 119.58 = pounds of CO2 / thousand cubic ft of natural gas, 12 mo/yr
    natural_gas_emission = round(((natural_gas_amount / 10.68) * 119.58 * 12), 2)

    # $0.1188 = cost per KWh, emission_factor comes from zipcode data,12 mo/yr
    electricity_emission = round(((electricity_amount / 0.1188) * emission_factor * 12), 2)

    #  $4.02 = fuel oil cost, 22.61 = fuel emission factor, 12 mo/yr
    fuel_emission = round(((fuel_oil_amount / 4.02) * 22.61 * 12), 2)

    # $2.47 = propane cost, 12.43 = propane emission factor, 12 mo/yr 
    propane_emission = round(((propane_amount / 2.47) * 12.43 * 12), 2)

    total_energy_emission_lb = round((natural_gas_emission + electricity_emission + fuel_emission + propane_emission), 2)

    #conversion from lb to ton 
    total_energy_emission_ton = round((total_energy_emission_lb * 0.0005), 2)

    return total_energy_emission_ton

print(energy(user_zipcode, natural_gas_amount, electricity_amount, fuel_oil_amount, propane_amount))





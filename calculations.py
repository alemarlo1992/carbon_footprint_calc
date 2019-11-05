"""Calculations applied to the pollution metrics"""

"""Transportation metric"""

number_of_vehicles = float(input('Enter amount of vehicles your household owns: '))
miles_per_week = float(input('Miles that you travel per week: '))
travel_miles_yr = float(input('How many miles did you air travel this year?: '))

def vehicle_emissions(number_of_vehicles, miles_per_week):
    
    emission_lb = int(((number_of_vehicles)*(miles_per_week)*float(52.14)/float(21.6))*float(19.6)*float(1.01))
    # conversion from lb to ton 
    vehicle_emission_ton = int(emission_lb * float(0.0005))

    return vehicle_emission_ton

vehicle_emissions(number_of_vehicles, miles_per_week)


def public_trans(miles_per_week):

    public_trans_emission_ton = int(float(0.0002) * miles_per_week * float(52.14) + 0.0016)

    return public_trans_emission_ton

public_trans(miles_per_week)


def air_travel(travel_miles_yr):

    travel_emission_ton = int(float(0.0005) * (travel_miles_yr) - float(0.0022))

    return travel_emission_ton

air_travel(travel_miles_yr)


def energy(natural_gas_amount, electricity_amount, fuel_oil_amount, propane_amount): 
    # natural_gas_amount = float(input('How much do you pay for Natural gas per month?: '))
    # electricity_amount = float(input('How much do you pay for Natural gas per month?: '))
    # fuel_oil_amount = float(input('How much do you pay for Natural gas per month?: '))
    # propane_amount = float(input('How much do you pay for Natural gas per month?: '))

    # $10.68 = natural gas cost, 119.58 = pounds of CO2 / thousand cubic ft of natural gas, 12 mo/yr
    natural_gas_emission = int((natural_gas_amount / float(10.68)) * float(119.58) * 12) 

    # $0.1188 = cost per KWh, emission_factor comes from zipcode data,12 mo/yr
    electricity_emission = int((electricity_amount / float(0.1188)) * emission_factor * 12)

    #  $4.02 = fuel oil cost, 22.61 = fuel emission factor, 12 mo/yr
    fuel_emission = int((fuel_oil_amount / float(4.02)) * float(22.61) * 12)

    # $2.47 = propane cost, 12.43 = propane emission factor, 12 mo/yr 
    propane_emission = int((propane_amount / float(2.47)) * float(12.43) * 12)

    total_energy_emission_lb = natural_gas_emission + electricity_emission + fuel_emission + propane_emission

    #conversion from lb to ton 
    total_energy_emission_ton = total_energy_emission_lb * float(0.0005)

    return total_energy_emission_ton






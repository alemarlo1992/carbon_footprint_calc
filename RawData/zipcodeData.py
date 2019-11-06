import csv 

def get_zipcodes():
    """Extractin zipcodes,  states, and CO2 Emmissions from zipcodes.txt"""
    #line 6 will only be executed if I run in through Vagrant. 
    with open('/home/vagrant/src/CarbonFootPrintCalculator/RawData/Zipcodes.csv') as csvfile: #Opens CSV file 
        reader = csv.DictReader(csvfile) #CSV file -> Dictionary 
        zipcodes_co2 = {}
        for row in reader: #iterate through data

            zipcode = row['zip']
            state = row['state']
            emission_rate = row['CO2'] 
            zipcodes_co2[zipcode] = emission_rate
        return zipcodes_co2
get_zipcodes()


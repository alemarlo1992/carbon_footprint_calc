import csv 

def zipcodes():
    """Extractin zipcodes,  states, and CO2 Emmissions from zipcodes.txt"""
    with open('Zipcodes.csv') as csvfile: #Opens CSV file 
        reader = csv.DictReader(csvfile) #CSV file -> Dictionary 
        for row in reader: #iterate through data
            zipcode = row['zip'] 
            state = row['state']
            emission_rate = row['CO2'] 
zipcodes()

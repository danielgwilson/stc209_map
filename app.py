import glob, os
os.chdir("./reports")
files = glob.glob("most_utilized_folders_by_usage_*.csv")


def get_router_locations():
    from geopy.geocoders import GoogleV3
    google_keys = [
        'AIzaSyDFNq0sdWuTb1OPZKI8_pzptX4bK7WBDcY',
        'AIzaSyBOAiq7lqzOVSH8PtYtG80DqjP2Y2LpNLM',
        'AIzaSyAacHXIDCNV6ptUDPQRdsHqNyQZRJu8k1A'
        ]
    import random # choosing a key randomly

    locations = {}

    for name in router_names[0:120]:
        strip_name = name.split('> ', 1)[1]
        strip_name = strip_name.replace(' >', '')
        print(strip_name)
        location = GoogleV3(random.choice(google_keys)).geocode(strip_name + ', Princeton, NJ', timeout = 10)
        locations[strip_name] = []
        try:
            print(location.latitude, location.longitude)
            locations[strip_name].append(location.latitude)
            locations[strip_name].append(location.longitude)
        except AttributeError:
            print('BAD ADDRESS')
            locations[strip_name].append(0.0)
            locations[strip_name].append(0.0)

    import csv
    with open('locations.csv', 'w') as f:
        w = csv.writer(f)
        w.writerows(locations.items())

import math
def remap(x, y):
    ppi = 72
    wh = 23.4
    gridlines = ppi * wh / 18
    ax = math.floor(x / gridlines)
    ay = math.floor(y / gridlines)
    return ax, ay

import datetime as dt
# generate list of times as keys
base = dt.datetime(2017, 5, 5, 2) # Y, M, D, H
date_list = [base + dt.timedelta(hours = 2 * x) for x in range(0, len(files))]
tstamps = [d.strftime("%m%d%H") for d in date_list]

# print(tstamps)

reports = {}

import pandas as pd
for i in range(0, len(files)):
    reports[tstamps[i]] = pd.read_csv(files[i])

import csv
reader = csv.reader(open('locations_map.csv', 'r'))
locations = {}
for row in reader:
    key, value = row
    locations[key] = value

print(locations)
# get_router_locations()
print(remap(155.11, 153.75))

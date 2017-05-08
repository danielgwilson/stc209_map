import glob, os
os.chdir("./reports")
files = glob.glob("most_utilized_folders_by_usage_*.csv")

# get router locations from google maps---this isn't working yet
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

# remapping function for building coordinates to 18x18 grid
import math
def remap(x, y):
    ppi = 72
    wh = 23.4
    gridlines = ppi * wh / 18
    ax = math.floor(x / gridlines)
    ay = math.floor(y / gridlines)
    return [ax, ay]

# create a list of date times to index/key our list of data frames
import datetime as dt
# generate list of times as keys
base = dt.datetime(2017, 5, 5, 2) # Y, M, D, H
date_list = [base + dt.timedelta(hours = 2 * x) for x in range(0, len(files))]
tstamps = [d.strftime("%m%d%H") for d in date_list]

# import all the data as pandas data frames indexed by date time
reports = {}

import pandas as pd
import numpy as np

for i in range(0, len(files)):
    reports[tstamps[i]] = pd.read_csv(files[i])

# router_names = reports[tstamps[0]]['Folder']
# print(router_names)

# load our known locations
locations = pd.read_csv(glob.glob("locations_map.csv")[0])

# get router locations if we're using google maps---not working yet
# get_router_locations()

# Load the location of a router in the data if we have a known location on our map
# Also attach intensities here

dfms = {}
max_clients = 0.0

for date in tstamps:
    print(date)
    report = reports[date]

    # create data frame for date
    mappings = {}
    router_names = report['Folder']
    for name in router_names:
        # print(name)
        if (name == 'Top' or name == 'Top > 20 Washington Road (Old Frick)'):
            continue # edge case where there is no carrot and where parens mess it up
        strip_name = name.split('> ', 1)[1]
        strip_name = strip_name.replace(' >', '')
        if not locations[locations['building'].str.match(strip_name)].empty:
            building = locations[locations['building'].str.match(strip_name)]
            mapping = remap(np.unwrap(building['x']), np.unwrap(building['y']))
            # print(building['x'], building['y'])
            router = report[report['Folder'].str.match(name)]
            clients = np.unwrap(router['Unique Clients'])[0]
            mappings[strip_name] = {}
            mappings[strip_name]['x'] = mapping[0]
            mappings[strip_name]['y'] = mapping[1]
            mappings[strip_name]['clients'] = clients
            # print('%-28s : %-8s : %-s' %
            #     (strip_name, str(mapping), str(clients)))
    df = pd.DataFrame(mappings).transpose()
    dfms[date] = df
    if max(df['clients']) > max_clients:
        max_clients = max(df['clients'])

print(max_clients)
print(dfms)
# print(mappings['050816'])

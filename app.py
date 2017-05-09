import glob, os
import random # choosing a key randomly
# from geopy.geocoders import GoogleV3
import csv
import math
import datetime as dt

import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
import matplotlib.animation as animation

import time

# get router locations from google maps---this isn't working yet
def get_router_locations():

    google_keys = [
        'AIzaSyDFNq0sdWuTb1OPZKI8_pzptX4bK7WBDcY',
        'AIzaSyBOAiq7lqzOVSH8PtYtG80DqjP2Y2LpNLM',
        'AIzaSyAacHXIDCNV6ptUDPQRdsHqNyQZRJu8k1A'
        ]


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

    with open('locations.csv', 'w') as f:
        w = csv.writer(f)
        w.writerows(locations.items())

# remapping function for building coordinates to 18x18 grid
def remap(x, y):
    ppi = 72
    wh = 23.4
    gridlines = ppi * wh / 18
    ax = math.floor(x / gridlines)
    ay = math.floor(y / gridlines)
    return [ax, ay]

def dancefloor_makeouts():
    # create a list of date times to index/key our list of data frames
    # generate list of times as keys
    os.chdir("./reports")
    files = glob.glob("most_utilized_folders_by_usage_*.csv")

    base = dt.datetime(2017, 5, 5, 2) # Y, M, D, H
    date_list = [base + dt.timedelta(hours = 2 * x) for x in range(0, len(files))]
    tstamps = [d.strftime("%m%d%H") for d in date_list]

    # import all the data as pandas data frames indexed by date time
    reports = {}

    for i in range(0, len(files)):
        reports[tstamps[i]] = pd.read_csv(files[i])

    # get router locations if we're using google maps---not working yet
    # get_router_locations()

    # load our known locations
    locations = pd.read_csv(glob.glob("locations_map.csv")[0])

    # dfms is short for dataframes
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

    return dfms, (max_clients), (tstamps)


def toRGB(pop, max_pop):
    ratio = pop/max_pop
    if ratio < .5:
        r = (.5-ratio)*510
        g = ratio*510
        b = 0
    else:
        r = 0
        g = (.5-(ratio-.5))*510
        b = (ratio-.5)*510

def toR(pop, max_pop):
    ratio = pop/max_pop
    if ratio < .5:
        r = (.5-ratio)*510
    else:
        r = 0
    return r

def toG(pop, max_pop):
    ratio = pop/max_pop
    if ratio < .5:
        g = ratio*510
    else:
        g = (.5-(ratio-.5))*510

def toB(pop, max_pop):
    ratio = pop/max_pop
    if ratio < .5:
        b = 0
    else:
        b = (ratio-.5)*510
    return b

# globals defined for the sake of animation
dfms = {}
tstamps = []
rescale = None
im = None
def animate(n):
    n = n % len(tstamps) # allows animation to loop

    # bounds
    ny, nx = 18, 18

    # init empty pixel array
    pixels = []
    for i in range(0, nx):
        col = []
        for j in range(0, ny):
            col.append([0,0,0])
        pixels.append(col)

    for index, row in dfms[tstamps[n]].iterrows():
        x = row['x'].astype(int)
        y = row['y'].astype(int)
        k = row['clients'] # magnitude
        ratio = rescale(k)
        booster = 1.5
        midpoint = 0.25
        print(ratio)
        if ratio < midpoint:
            b = ratio * 4 * booster
            g = 0.1 * ratio * booster
            r = 0 * booster
        else:
            b = 0 * booster
            g = 0.1 * ratio * booster
            r = ratio - midpoint * booster
        pixels[y][x] = [r, g, b]

    im.set_array(pixels)

def save_animation():
    anim_txt = open('animation.txt', 'w')
    for n in range(0, len(tstamps)):
        # bounds
        ny, nx = 18, 18

        # init empty pixel array
        pixels = []
        for i in range(0, nx):
            col = []
            for j in range(0, ny):
                col.append([0,0,0])
            pixels.append(col)

        for index, row in dfms[tstamps[n]].iterrows():
            x = row['x'].astype(int)
            y = row['y'].astype(int)
            k = row['clients'] # magnitude
            ratio = rescale(k)
            booster = 1.5
            midpoint = 0.25
            print(ratio)
            if ratio < midpoint:
                b = ratio * 4 * booster
                g = 0.1 * ratio * booster
                r = 0 * booster
            else:
                b = 0 * booster
                g = 0.1 * ratio * booster
                r = ratio - midpoint * booster
            pixels[y][x] = [r, g, b]
        anim_txt.write("%s\n\n" % pixels)

def save_animation2():
    anim_txt = open('animation.txt', 'w')
    for n in range(0, len(tstamps)):
        # bounds
        num_buildings = 97

        # init empty pixel array
        pixels = []
        col = []
        for i in range(num_buildings):        
            col.append([0,0,0,0,0])
            pixels.append(col)

        for index, row in dfms[tstamps[n]].iterrows():
            x = row['x'].astype(int)
            y = row['y'].astype(int)
            k = row['clients'] # magnitude
            if k != 0:
                ratio = rescale(k)
                booster = 1.5
                midpoint = 0.25
                print(ratio)
                if ratio < midpoint:
                    b = ratio * 4 * booster
                    g = 0.1 * ratio * booster
                    r = 0 * booster
                else:
                    b = 0 * booster
                    g = 0.1 * ratio * booster
                    r = ratio - midpoint * booster
                pixels[y][x] = [x, y, r, g, b]
        anim_txt.write("%s\n\n" % pixels)


# def makeTextFile():
    # t = 44
    # b = 97
    # v = 5
    # values = [[[0 for k in xrange(t)] for j in xrange(b)] for i in xrange(5)]
    # for i in range(44):
    #     for j in range(97):
    #         for k in range(5):

def main():
    # setup from data
    global tstamps, dfms, rescale, im
    dfms, max_clients, tstamps = dancefloor_makeouts()

    # -----------------
    # ANIMATION TESTING
    # -----------------

    # Pixel field testing
    import matplotlib.pyplot as plt
    # Make some random data to represent your r, g, b bands.
    ny, nx = 18, 18

    # rescale to range function
    from scipy.interpolate import interp1d
    max_pixel_value = 1.0
    rescale = interp1d([0.0, max_clients], [0.0, max_pixel_value], bounds_error = False, fill_value = 'extrapolate')

    # save_animation()
    # for n in range(0, len(tstamps)):
    # bounds
    ny, nx = 18, 18

    # init empty pixel array
    pixels = []
    for i in range(0, nx):
        col = []
        for j in range(0, ny):
            col.append([0,0.5,0.5])
        pixels.append(col)

    fig = plt.figure()
    im = plt.imshow(pixels, interpolation='nearest', animated = True)
    ani = animation.FuncAnimation(fig, animate, interval = 650)
    plt.show()

if __name__ == "__main__":
    main()

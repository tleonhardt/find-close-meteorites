#!/usr/bin/env python3
"""
A demo project that uses Python and NASA to find meteorite landing sites located near a given location.
"""
import math
import requests


def calc_dist(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Calculate distance between two points given in degrees latidude and longitude."""
    lat1 = math.radians(lat1)
    lon1 = math.radians(lon1)
    lat2 = math.radians(lat2)
    lon2 = math.radians(lon2)

    h = math.sin((lat2 - lat1) / 2) ** 2 + \
        math.cos(lat1) * \
        math.cos(lat2) * \
        math.sin((lon2 - lon1) / 2) ** 2

    return 6372.8 * 2 * math.asin(math.sqrt(h))


def get_dist(a_meteor):
    """Function to use as a sort key for sorting the meteorite data by distance from a specified location."""
    return a_meteor.get('distance', math.inf)


if __name__ == '__main__':
    # Norther Virginia, USA
    my_loc = (38.9588, -77.3592)

    meteor_resp = requests.get('https://data.nasa.gov/resource/y77d-th95.json')
    meteor_data = meteor_resp.json()

    for meteor in meteor_data:
        if not ('reclat' in meteor and 'reclong' in meteor):
            continue

        meteor['distance'] = calc_dist(float(meteor['reclat']),
                                       float(meteor['reclong']),
                                       my_loc[0],
                                       my_loc[1])

    meteor_data.sort(key=get_dist)

    print(meteor_data[0:10])

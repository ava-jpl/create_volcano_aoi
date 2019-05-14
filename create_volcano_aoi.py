#!/usr/bin/env python

'''
Initiated from a VOLC-GVP product, creates an AOI around the volcano of X kilometers.
'''

from __future__ import print_function
import os
import json
import math
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

VERSION = "v1.0"
AOI_PROD = "AOI-GVN_{}-{}-{}"
STARTTIME = "1990-01-01T00:00:00Z"
ENDTIME = "2030-01-01T00:00:00Z"
INPUT_PROD_TYPE = "volcano"

def main():
    '''From a VOLC product and creates an AOI a given radius around the volcano'''
    ctx = load_context()
    prod_type = ctx.get("type", False)
    if prod_type.lower() != INPUT_PROD_TYPE:
        raise Exception("Input product type: {} does not match: {}".format(prod_type, INPUT_PROD_TYPE))
    aoi_radius_km = float(ctx.get("radius_km"))
    vname = ctx.get("volcano_name")
    gvn = ctx.get("volcano_number")
    clean_name = ctx.get("clean_name")
    latitude = ctx.get("latitude")
    longitude = ctx.get("longitude")
    location = gen_geojson(latitude, longitude, aoi_radius_km)
    prod_id = AOI_PROD.format(gvn, clean_name, VERSION)
    ds_obj = {'label': prod_id, 'version': VERSION, 'location': location,
              "starttime": STARTTIME, "endtime": ENDTIME}
    met_obj = {"latitude": latitude, "longitude": longitude, "clean_name": clean_name,
               "volcano_number": gvn, "volcano_name": vname, "radius": aoi_radius_km}
    save_product_met(prod_id, ds_obj, met_obj)

def gen_geojson(lat, lon, radius):
    '''generates the latitude and the longitude of the input given the radius'''
    lat = float(lat)
    lon = float(lon)
    l = range(0, 361, 20)
    coordinates = []
    for b in l:
        coords = shift(lat, lon, b, radius)
        coordinates.append(coords)
    return {"coordinates": [coordinates], "type": "Polygon"}

def save_product_met(prod_id, ds_obj, met_obj):
    '''generates the appropriate product json files in the product directory'''
    if not os.path.exists(prod_id):
        os.mkdir(prod_id)
    outpath = os.path.join(prod_id, '{}.dataset.json'.format(prod_id))
    with open(outpath, 'w') as outf:
        json.dump(ds_obj, outf)
    outpath = os.path.join(prod_id, '{}.met.json'.format(prod_id))
    with open(outpath, 'w') as outf:
        json.dump(met_obj, outf)

def shift(lat, lon, bearing, distance):
    '''generates a circular polygon'''
    R = 6378.1  # Radius of the Earth
    bearing = math.pi * bearing / 180  # convert degrees to radians
    lat1 = math.radians(lat)  # Current lat point converted to radians
    lon1 = math.radians(lon)  # Current long point converted to radians
    lat2 = math.asin(math.sin(lat1) * math.cos(distance / R) +
                     math.cos(lat1) * math.sin(distance / R) * math.cos(bearing))
    lon2 = lon1 + math.atan2(math.sin(bearing) * math.sin(distance / R) * math.cos(lat1),
                             math.cos(distance / R) - math.sin(lat1) * math.sin(lat2))
    lat2 = math.degrees(lat2)
    lon2 = math.degrees(lon2)
    return [lon2, lat2]

def load_context():
    '''loads the context file into a dict'''
    try:
        context_file = '_context.json'
        with open(context_file, 'r') as fin:
            context = json.load(fin)
        return context
    except:
        raise Exception('unable to parse _context.json from work directory')

if __name__ == '__main__':
    main()

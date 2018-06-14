# -*- coding: utf-8 -*-
"""
Created on Wed Jun  13 13:16:29 2018

@author: eion
"""

import os

# geospatial
import geopandas as gpd
import pandas as pd
import pysal as ps
import numpy as np
from numpy import linalg as LA

# visualization
import matplotlib.pyplot as plt


def find_district_utm(df):
    utm_district = []
    for ind in range(0, len(df)):
        utm_longitude = [126, 120, 114, 108, 102, 96, 90, 84, 78, 72, 66]
        i = abs(df_districts_key['intptlon'][ind]) # take the longitude for a particular district, adjusting for the fact that it's negative but the list is positive
        utm_longitude.append(i) # append it to the list of utms
        utm_rev = sorted(utm_longitude, reverse = True) # descending order
#        print("i =", i)
#        print("state =", df_districts_key["name"][ind])
#        print("utm zone =", 9 + utm_rev.index(i))
        utm_district.append(9 + utm_rev.index(i)) # append the index plus 9 (for centering) to the list of county utms
#    print(utm_county)
    print(len(df))
    print(len(utm_district))
    df['utm'] = str(utm_district) # figure out how to append a column
    return df



# pull and prepare data
data_folder = 'tl_rd13_us_cd113'
url = "https://www2.census.gov/geo/tiger/TIGERrd13/CD113/tl_rd13_us_cd113.zip"
from get_geodata_pa import get_and_unzip
get_and_unzip(url, ".")

# import Shapefile data
district_shp = os.path.join("tl_rd13_us_cd113.shp")
df_districts = gpd.read_file(district_shp)
df_districts.plot()

# set-up key and prepare indices
key = pd.read_csv('FIPSkey.csv', delimiter=',', dtype = {'STATEFP': str, 'NAME': str, 'UTM': str})
utms = ["02","04","05","10","11","12","13","14","15","16","17","18","19","20","55"]

df_districts_key = pd.merge(df_districts, key, how = 'left', on = 'STATEFP') # connect Shapefile data to key
df_districts_key.columns = map(str.lower, df_districts_key.columns) # make all column names miniscule
df_districts_key['intptlon'] = df_districts_key.centroid.x # compute and append column for longitude of district centroid
df_districts_key['intptlat'] = df_districts_key.centroid.y # compute and append column for latitude of district centroid
df_districts_key = find_district_utm(df_districts_key) # call function to add column of UTM zones by district

for utm in utms:
    df = df_districts_key.loc[df_districts_key['utm'] == utm] # filter states with desired UTM zone
    utm_epsg = int('269'+utm) # derive CRS code via UTM zone xN (unit is meter)
    df_area = df.to_crs(epsg=utm_epsg).area/1000**2 # compute projected areas in square kilometers
    df_key_area = df.assign(area_km2=df_area.values) # merge area values with GEOID info
    df_length = df.to_crs(epsg=utm_epsg).length/1000 # compute projected lengths (perimeters) in kilometers
    df_key_length = df.assign(length_km=df_length.values) # merge length values with GEOID info
    if utm == utms[0]:
        areas = df_key_area
        lengths = df_key_length
    else:
        areas = pd.concat([areas,df_key_area]) # accumulate area figures for all processed UTMs
        lengths = pd.concat([lengths,df_key_length]) # accumulate length figures for all processed UTMs

df_districts_key = pd.merge(df_districts_key, areas, how = 'left', on = ['statefp','cd113fp','geoid','namelsad','lsad','cdsessn','mtfcc','funcstat','aland','awater','intptlat','intptlon','name','utm']) # combine keyed "Shapefile" with area calculations
df_districts_key = pd.merge(df_districts_key, lengths, how = 'left', on = ['statefp','cd113fp','geoid','namelsad','lsad','cdsessn','mtfcc','funcstat','aland','awater','intptlat','intptlon','name','utm']) # combine keyed "Shapefile" with length calculations

df_districts_key.loc[df_districts_key['statefp'] == '42'][['statefp','cd113fp','area_km2','length_km']] # inspect a single state's district areas and perimeters

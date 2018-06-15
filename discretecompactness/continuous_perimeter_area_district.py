# -*- coding: utf-8 -*-
"""
Created on Wed Jun  13 13:16:29 2018

@author: eion + katie
"""

import os

# geospatial
import geopandas as gpd
import pandas as pd
import pysal as ps
import numpy as np
from numpy import linalg as LA
import math

# visualization
import matplotlib.pyplot as plt

def find_district_utm(df): # input is a dataframe composed of districts with coarse UTM zones
    for i in range(0, len(df)): # iterate through districts in dataframe
        district = df.iloc[[i]][['geoid','geometry','utm']] # isolate geometry and coarse UTM from district of interest
        utm = str(math.floor((df.iloc[[i]].centroid.x+180)*59/354)+1).zfill(2) # compute UTM zone according to the district's centroid longitude
        district_utm = district.assign(utm=utm) # update district's UTM with proper assignment
        if i==0: # begin aggregating correct UTM list
            district_utms = district_utm
        else: # continue aggregating correct UTM list
            district_utms = pd.concat([district_utms,district_utm])
    df['utm'] = district_utms['utm'] # update dataframe with correct UTM zones
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
df_districts_key = find_district_utm(df_districts_key) # call function to add column of UTM zones by district

for utm in utms:
    df = df_districts_key.loc[df_districts_key['utm'] == utm] # filter states with desired UTM zone
    utm_epsg = int('269'+utm) # derive CRS code via UTM zone xN (unit is meter)
    df_area = df.to_crs(epsg=utm_epsg).area/1000**2 # compute projected areas in square kilometers
    df_key_area = df.assign(area_km2=df_area.values) # merge area values with GEOID info
    df_length = df.to_crs(epsg=utm_epsg).length/1000 # compute projected lengths (perimeters) in kilometers
    df_key_length = df.assign(length_km=df_length.values) # merge length values with GEOID info
    if utm == utms[0]: # begin aggregating area and perimeter lists
        areas = df_key_area
        lengths = df_key_length
    else:
        areas = pd.concat([areas,df_key_area]) # accumulate area figures for all processed UTMs
        lengths = pd.concat([lengths,df_key_length]) # accumulate length figures for all processed UTMs

df_districts_key = pd.merge(df_districts_key, areas, how = 'left', on = ['statefp','cd113fp','geoid','namelsad','lsad','cdsessn','mtfcc','funcstat','aland','awater','intptlat','intptlon','name','utm']) # combine keyed "Shapefile" with area calculations
df_districts_key = pd.merge(df_districts_key, lengths, how = 'left', on = ['statefp','cd113fp','geoid','namelsad','lsad','cdsessn','mtfcc','funcstat','aland','awater','intptlat','intptlon','name','utm']) # combine keyed "Shapefile" with length calculations

#df_districts_key.loc[df_districts_key['statefp'] == '42'][['statefp','cd113fp','area_km2','length_km']] # inspect a single state's district areas and perimeters
#df_districts_key.loc[df_districts_key['statefp'] == '42'][['statefp','cd113fp','intptlon','utm']] # inspect a single state's district centroid longitude and UTM assignment

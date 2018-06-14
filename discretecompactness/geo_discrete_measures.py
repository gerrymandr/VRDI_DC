# -*- coding: utf-8 -*-
"""
Created on Tue Jun 12 14:15:13 2018

@author: assaf, ruth, katya, zach
"""
import geopandas as gpd
import pandas as pd
import pysal as ps
import numpy as np
from numpy import linalg as LA

import os
from urllib.request import urlopen
from zipfile import ZipFile

import csv


# Data retrieval
def get_and_unzip(url, data_dir=os.getcwd()):
    basename = url.split("/")[-1]
    name_with_path = os.path.join(data_dir, basename)
    if not os.path.exists(name_with_path):
        file_data = urlopen(url)
        data_to_write = file_data.read()
        with open(name_with_path, "wb") as f:
            f.write(data_to_write)

        zip_obj = ZipFile(name_with_path)
        zip_obj.extractall(data_dir)
        del(zip_obj)

# State FIPS codes - specify here your state of interest
FIPS = ["01"]       # Alabama


# Create file path to VTD shapefile if it does not exist
if not os.path.exists(os.path.join(os.getcwd(), 'VTD_SHP')):
    os.makedirs(os.path.join(os.getcwd(),'VTD_SHP'))

# Download VTD shapefiles for each FIPS code specified above
for FIP in FIPS:
    url = "https://www2.census.gov/geo/tiger/TIGER2012/VTD/tl_2012_"+FIP+"_vtd10.zip"
    get_and_unzip(url,"VTD_SHP")
    state_fip = FIP


# Create directory for shapefile of whole country
if not os.path.exists(os.path.join(os.getcwd(), 'CD_SHP')):
    os.makedirs(os.path.join(os.getcwd(),'CD_SHP'))
    
# Grab 113th congressional district TIGER shapefile from census
url_cd = "https://www2.census.gov/geo/tiger/TIGERrd13/CD113/tl_rd13_us_cd113.zip"
get_and_unzip(url_cd, "CD_SHP")
    

# Create the data frames and query out state of interest
df_vtds = gpd.read_file("VTD_SHP")
df_cds = gpd.read_file("CD_SHP")
df_statecds = df_cds.loc[df_cds['STATEFP'] == state_fip]

   
# Functions for calculating discrete area and perimeter
 
def get_discrete_area(df_container, df_units, area_col_name = "area_count"):
    """Takes in two data frames, one of a larger container geometry (i.e., congressional
    district) and one of a smaller unit geometry (i.e., VTDs). There is also the 
    option to input a specified string for the output area column name. This function
    calculates the number of smaller units within the larger geometries and appends these
    in a new column to the larger geometries data frame."""
    
    disc_area = np.zeros(len(df_container))
    for i in range(0,len(df_container)):
        count = 0
        for j in range(0,len(df_units)):
            if df_container.iloc[i].geometry.contains(df_units.iloc[j].geometry):
                count += 1
        disc_area[i] = count
        #print(disc_area)
    df_container[area_col_name] = disc_area
        
    
def get_discrete_perim(df_container, df_units, perim_col_name = "perim_count"):
    """Takes in two data frames, one of a larger container geometry (i.e., congressional
    district) and one of a smaller unit geometry (i.e., VTDs). There is also the 
    option to input a specified string for the output perimeter column name. This function
    calculates the number of smaller units that intersect the boundaries of the larger 
    geometries and appends these in a new column to the larger geometries data frame."""
    
    disc_perim = np.zeros(len(df_container))
    for i in range(0,len(df_container)):
        count = 0
        for j in range(0,len(df_units)):
            if df_units.iloc[j].geometry.intersects(df_container.iloc[i].geometry.boundary):
                count += 1
        disc_perim[i] = count
        #print(disc_perim)
    df_container[perim_col_name] = disc_perim

# Function calls
get_discrete_perim(df_statecds, df_vtds)
get_discrete_area(df_statecds, df_vtds)




















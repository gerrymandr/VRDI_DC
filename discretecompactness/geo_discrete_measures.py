# -*- coding: utf-8 -*-
"""
Created on Tue Jun 12 14:15:13 2018

@author: assaf, ruth, katya, zach

Example function calls:
    get_discrete_perim(df_statecds, df_vtds)
    get_discrete_area(df_statecds, df_vtds)

"""
import geopandas as gpd
import numpy as np
import os

from urllib.request import urlopen
from zipfile import ZipFile


   
# Functions for calculating discrete area and perimeter
 
def get_discrete_area(df_container, df_units, area_col_name = "area_count"):
    """Takes in two dataframes, one of a larger container geometry (i.e., congressional
    district) and one of a smaller unit geometry (i.e., VTDs). There is also the 
    option to input a specified string for the output area column name. This function
    calculates the number of smaller units within the larger geometries and appends these
    in a new column to the larger geometries dataframe."""
    
    disc_area = np.zeros(len(df_container))                 # create empty vector
    for i in range(0,len(df_container)):                    # loop through larger geometries
        count = 0
        for j in range(0,len(df_units)):                    # loop through smaller units
            # df_container is a dataframe, geometry calls its spatial data, and contains 
            # checks containment with other spatial data
            if df_container.iloc[i].geometry.contains(df_units.iloc[j].geometry):
                count += 1
        disc_area[i] = count
    df_container[area_col_name] = disc_area                 # add vector to dataframe
        
    
def get_discrete_perim(df_container, df_units, perim_col_name = "perim_count"):
    """Takes in two dataframes, one of a larger container geometry (i.e., congressional
    district) and one of a smaller unit geometry (i.e., VTDs). There is also the 
    option to input a specified string for the output perimeter column name. This function
    calculates the number of smaller units that intersect the boundaries of the larger 
    geometries and appends these in a new column to the larger geometries dataframe."""
    
    disc_perim = np.zeros(len(df_container))                # create empty vector
    for i in range(0,len(df_container)):                    # loop through larger geometries
        count = 0
        for j in range(0,len(df_units)):                    # loop through smaller units
            # df_container is a dataframe, geometry calls its spatial data, and intersects 
            # checks any overlap with other spatial data
            if df_units.iloc[j].geometry.intersects(df_container.iloc[i].geometry.boundary):
                count += 1
        disc_perim[i] = count
    df_container[perim_col_name] = disc_perim               # add vector to dataframe






















# -*- coding: utf-8 -*-
"""
Created on Thu Jun 14 13:42:55 2018

@author: eion + katie
"""

import os

# geospatial
import geopandas as gpd
import pandas as pd
import pysal as ps
import numpy as np
from numpy import linalg as LA
from bisect import bisect

# visualization
import matplotlib.pyplot as plt

# tutorial link from https://www.twilio.com/blog/2017/08/geospatial-analysis-python-geojson-geopandas.html
#stateplane_geojson = "https://opendata.arcgis.com/datasets/23178a639bdc4d658816b3ea8ee6c3ae_0.geojson"

# pull and prepare data
from get_geodata_pa import get_and_unzip
url_stateplane = "https://opendata.arcgis.com/datasets/23178a639bdc4d658816b3ea8ee6c3ae_0.zip"
url_districts = "https://www2.census.gov/geo/tiger/TIGERrd13/CD113/tl_rd13_us_cd113.zip"
get_and_unzip(url_stateplane, ".")
get_and_unzip(url_districts, ".")

# import Shapefile data
stateplane_shp = os.path.join("USA_State_Plane_Zones_NAD83.shp")
df_stateplane = gpd.read_file(stateplane_shp)
#df_stateplane.plot()

district_shp = os.path.join("tl_rd13_us_cd113.shp")
df_districts = gpd.read_file(district_shp)

# compute district centroids
df_centroids = df_districts[["STATEFP","GEOID"]]

df_centroids['cent'] = df_districts.centroid
df_centroids = gpd.GeoDataFrame(df_centroids, geometry=df_centroids.cent, crs={'init': 'epsg:4269'})
df_centroids.plot(ax = df_districts.plot(color="white", edgecolor="lightgray"), markersize = 1)

blah = gpd.sjoin(df_centroids.to_crs(epsg=2163),df_stateplane.to_crs(epsg=2163), op = 'intersects', how = 'left')
bad = blah.loc[pd.isnull(blah['ZONE'])]

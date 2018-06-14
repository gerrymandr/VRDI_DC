
import os

# geospatial
import geopandas as gpd
import pandas as pd
import pysal as ps
import numpy as np
import csv
from geopandas import GeoSeries, GeoDataFrame
from shapely.geometry import Point
from shapely.geometry import LineString, Point
from numpy import array

# visualization
#should work for Emilia's CA
import matplotlib.pyplot as plt
print(os.getcwd())
data_folder = '2012 California Shapefiles'
#url = "http://aws.redistricting.state.pa.us/Redistricting/Resources/GISData/2011-Voting-District-Boundary-Shapefiles.zip"
#from get_geodata_pa import get_and_unzip
#get_and_unzip(url, ".")

county_shp = "CA_Counties.shp"
df_counties = gpd.read_file(county_shp)
df_counties.plot()

county_centroids = df_counties.centroid
c_x = county_centroids.x
c_y = county_centroids.y


#make points
#point[i] = Point(c_x[i], c_y[i])

# Spatial Weightsos
rW = ps.rook_from_shapefile(county_shp)
rW[10] # View neighbors for specific row -> note, all weights = 1.0
rW.neighbors # View all neighbors
rW.full()[0] # View full contiguity matrix

# Would be nice to see attributes for neighbors:
self_and_neighbors = [10]
self_and_neighbors.extend(rW.neighbors[10])
df_counties.iloc[self_and_neighbors, :5]

# Show the dual graph on a map
basemap = df_counties.plot(color = "white", edgecolor = "lightgray")
county_centroids.plot(ax = basemap, markersize = 1)

for i, jj in rW.neighbors.items():
    for j in jj:
        basemap.plot([c_x[i], c_x[j]], [c_y[i],c_y[j]], linestyle = '-', linewidth = 1)

plt.title("Rook Neighbor Graph")


line_segments = []
centroid1 = []
centroid2 = []
for i, jj in rW.neighbors.items():
    for j in jj:
        line = LineString([(c_x[i],c_y[i]), (c_x[j], c_y[j])])
        line_segments.append(line)
        centroid1.append(str((c_x[i],c_y[i])))
        centroid2.append(str((c_x[j],c_y[j])))
print(line_segments)

with open('gep.csv', newline='', encoding='utf-8') as f:
    reader = csv.reader(f)
    for row in reader:
        print(row)
      
#making a dictionary, keys become column header and elements become elements of that column
dual = {
        "centroid1": centroid1,
        "centroid2": centroid2,
        "geometry": line_segments
        }
        
df_segments = gpd.GeoDataFrame(data = dual, geometry = "geometry", crs = "+init=epsg:4269")


    
df_segments.to_file('/home/user/folder/dual_graph.shp' )



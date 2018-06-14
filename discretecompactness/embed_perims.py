import os

# geospatial
import geopandas as gpd
import pysal as ps
import numpy as np
from geopandas import GeoSeries, GeoDataFrame

#importing district shapefile
DISTRICT_shp = os.path.join('/home/hannah/Desktop/Nevada', "DISTRICT.shp")
df_DISTRICT = gpd.read_file(DISTRICT_shp)
df_DISTRICT.plot()

#make centroids
DISTRICT_centroids = df_DISTRICT.centroid
c_x = DISTRICT_centroids.x
c_y = DISTRICT_centroids.y

#Make points from centroids
point[i] = Point(c_x, c_y)

# Spatial Weights
rW = ps.rook_from_shapefile(DISTRICT_shp)
rW[10] # View neighbors for specific row -> note, all weights = 1.0
rW.neighbors # View all neighbors
rW.full()[0] # View full contiguity matrix

# Would be nice to see attributes for neighbors:
self_and_neighbors = [10]
self_and_neighbors.extend(rW.neighbors[10])
df_DISTRICT.iloc[self_and_neighbors, :5]

# Show the dual graph on a map
basemap = df_NV.plot(color = "white", edgecolor = "lightgray")
NV_centroids.plot(ax = basemap, markersize = 1)

for i, jj in rW.neighbors.items():
    # origin = centroids[k]
    for j in jj:
       line[j] = LineString([(c_x[i], c_x[j]), (c_y[i], c_y[j])])

       DISTRICT_dual = df_DISTRICT.LineString 


import os

# geospatial
import pandas as pd
import geopandas as gpd
import pysal as ps
import numpy as np
import shapely.geometry
from shapely.geometry import Point, LineString

#importing district shapefile
#This works for Hannah's NV
NV_shp = os.path.join('/home/hannah/Desktop/Nevada', "NV.shp")
df_NV = gpd.read_file(NV_shp)

#make centroids
NV_centroids = df_NV.centroid
c_x = NV_centroids.x
c_y = NV_centroids.y


# Spatial Weights
rW = ps.rook_from_shapefile(NV_shp)
rW[10] # View neighbors for specific row -> note, all weights = 1.0
rW.neighbors # View all neighbors
rW.full()[0] # View full contiguity matrix

# Would be nice to see attributes for neighbors:
self_and_neighbors = [10]
self_and_neighbors.extend(rW.neighbors[10])
df_NV.iloc[self_and_neighbors, :5]




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

#making a dictionary, keys become column header and elements become elements of that column
dual = {
        "centroid1": centroid1,
        "centroid2": centroid2,
        "geometry": line_segments
        }
        
df_segments = gpd.GeoDataFrame(data = dual, geometry = "geometry", crs = "+init=epsg:4269")


    
df_segments.to_file('/home/hannah/Desktop/Nevada/dual_graph.shp' )



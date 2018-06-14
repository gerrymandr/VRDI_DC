"""
exportPerims.py

This script detects the boundaries of units in a .shp file. The algorithm builds
a matrix containing all faces of the dual graph, then determines which graph edges
of those faces are unpaired, indicating they bound the graph.

Authored by Jordan Kemp for the VRDI
June 13th, 2018

"""
#Constants
SRC_SHAPEFILE = "cb_2017_72_tract_500k/cb_2017_72_tract_500k.shp"
SAVE_FILE = "pr_county.gal";
SAVE_FILE_WITH_ID = "pr_county_geoid.gal";


import os

# geospatial tools
import geopandas as gpd
import pysal as ps
import numpy as np

# visualization tools
import matplotlib.pyplot as plt

# MapData class contains all useful information of the graph. Locations of Centroids
# (ie. vertices of the graph), and edges are stored using the pysal rook function.
class MapData:

    # Centroid contains the lists of x,y coordinates of all map centroids
    class Centroids:

        def __init__(self,c_x,c_y):
            self.x = c_x
            self.y = c_y

    # Get_edges takes a list of centroids and produces a list of edges in the form
    # of a (x1,y1),(x2,y2)) vertex pair list
    def get_edges(self,c):

        pairs = []
        for i,jj in self.weights.neighbors.items():
            for j in jj:
                pairs.append([[c.x[i],c.y[i]],[c.x[j],c.y[j]]])
        return pairs

    # Spatial weights, centroids, and edges
    def __init__(self,weights,c_x,c_y):

        self.weights = weights
        self.centroids = self.Centroids(c_x,c_y)
        self.edges = self.get_edges(self.centroids)

# Parses the map data to produce centroids, and the spatial weights. Packages them
# into the MapData class
def get_adjacencies(mapfile):

    # Identify the centroids of the file
    map_centroids = mapfile.centroid
    c_x = map_centroids.x
    c_y = map_centroids.y

    # Spatial Weights
    rW = ps.rook_from_shapefile(shp)

    return MapData(rW,c_x,c_y)

# Prints adjacency map/graph
def show_map(rW):

    basemap = df_clean_vtd.plot(color = "white", edgecolor = "lightgray")
    county_centroids.plot(ax = basemap, markersize = 1)

    for i, jj in rW.neighbors.items():
        # origin = centroids[k]
        for j in jj:
            segment = county_centroids
            basemap.plot([c_x[i], c_x[j]], [c_y[i], c_y[j]], linestyle = '-', linewidth = 1)




#Prints spatial weight data to .gal files
def export_adjacencies(mapData):

    # With useful ID
    mapData.weights = ps.rook_from_shapefile(shp, idVariable = "GEOID10")
    gal = ps.open(SAVE_FILE_WITH_ID, "w")
    gal.write(mapData.weights)
    gal.close()


    # Save Spatial Weights file in GAL format
    gal = ps.open(SAVE_FILE, "w")
    gal.write(mapData.weights)
    gal.close()


# Importing a .shp file
shp = SRC_SHAPEFILE
mapfile = gpd.read_file(shp)

mapData = get_adjacencies(mapfile)
export_adjacencies(mapData)
# print(mapData.edges)

"""
exportPerims.py
This script detects the boundaries of units in a .shp file. The algorithm builds
a matrix containing all faces of the dual graph, then determines which graph edges
of those faces are unpaired, indicating they bound the graph.
Authored by Jordan Kemp for the VRDI
June 13th, 2018
"""
#Constants
SRC_SHAPEFILE = "Data/cb_2017_72_tract_500k.shp"
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

def print_edge(edge):
    return "("+str(edge.v1.x)+","+str(edge.v1.y)+"),("+str(edge.v2.x)+","+str(edge.v2.y)+")"
            # for edge,adjs in self.edges.items():
            #     print("Vertex:" + str(edge.x)+","+str(edge.y)+"\n")
            #     for adj in adjs:
            #         print("Edge on:" + print_edge(adj))
            #         print("    with next:"+print_edge(adj.next)+"\n")
            #
            #     print("\n\n\n")

class MapData:

    #Centroid contains its coordinates and all of the other centroids to which it
    #directs to
    class Centroids:

        def __init__(self,c_x,c_y):
            self.x = c_x
            self.y = c_y
            self.adjs = []

    #Save edges as structs to be used as hash keys
    class Edge:

        def __init__(self,x1,y1,x2,y2,Map):
            self.v1 = Map.centroids[x1][y1]
            self.v2 = Map.centroids[x2][y2]
            self.adjs = []
            self.adj_angles = []
            self.next = None
            self.traversed = False

    # Get_edges takes a list of centroids and produces a list of edges in the form
    # of a (x1,y1),(x2,y2)) vertex pair list

    def find_boundaries(self):

        def compute_angles():
            return

        def build_face_matrix():
            return

        def find_next_fvertex():
            return

        for x, col in self.centroids:
            for y,centroid in col:
                for key,edge in centroids.edges:
                    return

    def generate_edges(self,c_x,c_y):

        def get_edges(c_x,c_y,Map):

            pairs = {Map.centroids[c_x[i]][c_y[i]]:[] for i in range(len(c_x))}
            for i,jj in self.weights.neighbors.items():
                for j in jj:

                    pairs[Map.centroids[c_x[i]][c_y[i]]].append(Map.Edge(c_x[i],c_y[i],c_x[j],c_y[j],Map))

                    Map.centroids[c_x[i]][c_y[i]].adjs.append(
                        Map.centroids[c_x[j]][c_y[j]])
            return pairs

        def calc_small_angle(edge,adjs):

            angles = []
            for adj in adjs:

                v0 = np.array([edge.v1.x,edge.v1.y]) - np.array([edge.v2.x,edge.v2.y])
                v1 = np.array([adj.v2.x,adj.v2.y]) - np.array([adj.v1.x,adj.v1.y])

                angle = np.math.atan2(np.linalg.det([v0,v1]),np.dot(v0,v1))
                angles.append(np.degrees(angle))

            angles, adjs = zip(*sorted(zip(angles, adjs)))

            return adjs[0]


        pairs = get_edges(c_x,c_y,self)
        for v1,edges in pairs.items():
            for edge in edges:
                edge.next = calc_small_angle(edge,pairs[edge.v2])

        return pairs


    # Spatial weights, centroids, and edges
    def __init__(self,weights,c_x,c_y):

        #Save the weights
        self.weights = weights
        #Save the centroids
        self.centroids = {c_x[i]:{c_y[i]:self.Centroids(c_x[i],c_y[i])}
                        for i in range(len(c_x))}
        #Save the edges to be used as keys in the
        self.edges = self.generate_edges(c_x,c_y)
        #Generate edge/face dict.
        self.face_dict = {edge:None for edge,adjs in self.edges.items()}


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
# export_adjacencies(mapData)
# print(mapData.edges)

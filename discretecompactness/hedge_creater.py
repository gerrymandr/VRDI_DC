"""
hedge_creater.py

Eugene Henninger-Voss 2018
For MGGG

Unique to this file:
    Vertex class
    make_vertices()
    next_vertex()
    make_face()
    make_faces()
    
Creates the data needed for a halfedge graph from a shapefile.

Given a shapefile these four functions work together to create a list of 
Vertex class objects representing every vertex which stores each vertex's 
coordinates and a list of adjecent vertices in a cyclic order.  A list of lists
is also created in which each interior list is an ordered list of vertices 
representing a face.


"""
#Constants
SRC_SHAPEFILE = "/Users/Eug/miniconda3/envs/vrdi/vrdi_data/Montana/MtGISData/tl_2012_mt_county/tl_2012_mt_county.shp"
SAVE_FILE = "pr_county.gal";
SAVE_FILE_WITH_ID = "pr_county_geoid.gal";


import os

# for sorting
from operator import itemgetter

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


class Vertex:

    def __init__(self, x ,y):
        self.x = x
        self.y = y
        self.adjs = []
        self.transversed = []

# alot like get_adjacencies
# returns list of all the vertices with coordinates and ordered list of 
# adjacencies from mapfile
def make_vertices(mapfile):
    
    # Identify the centroids of the file
    map_centroids = mapfile.centroid
    c_x = map_centroids.x
    c_y = map_centroids.y


    # Spatial Weights
    rW = ps.rook_from_shapefile(shp)
    
     #create place to store vertices
    vertices = []
    for i in range(len(map_centroids)):
        newVertex = Vertex(c_x[i], c_y[i])
        vertices.append(newVertex)

    # create ordered list of adjecent vertices for each vertex
    for i in range(len(vertices)):
        currVert = vertices[i]
        
        # find the neighbors
        numeric_adjs = rW.neighbors[i]
        for j in range(len(numeric_adjs)):
            currVert.adjs.append(vertices[numeric_adjs[j]])
            
        # find the angles of all the neighbors
        testList = []
        for j in range(len(currVert.adjs)):
            currAdj = currVert.adjs[j]
            xDifference = currAdj.x - currVert.x
            yDifference = currAdj.y - currVert.y
            angle = np.arctan2(yDifference,xDifference)
            testList.append((currAdj, angle))
        
        # order the neighbors 
        testList.sort(key=itemgetter(1))
        tempList = []
        for j in range(len(testList)):
            tempList.append(testList[j][0])
        currVert.adjs = tempList
        
    return vertices
    
def next_vertex(v1, v2):
    oldIndex = v2.adjs.index(v1)
    newIndex = oldIndex + 1 
    if newIndex == len(v2.adjs):
        newIndex = 0
    return v2.adjs[newIndex]

def make_face(v1, v2):
    newFace = [v1, v2]
    
    fromVertex = v1
    currVertex = v2
    while True:
        
        # mark that the current edge (vertex pair) has been transversed
        fromVertex.transversed.append(currVertex)
        
        # find the next vertex
        nextVertex = next_vertex(fromVertex, currVertex)
        
        # continue if not back where the face started
        if nextVertex == v1 :
            if v2 == next_vertex(currVertex, v1):
                break
            
        # update face and the vertex variables 
        newFace.append(nextVertex)
        fromVertex = currVertex
        currVertex = nextVertex
        
    return newFace
    
    
def make_faces(vertices):
    
    faces = []
    
    # for every edge (vertex ordered pair) that has not been counted towards a 
    # face yet start make_face on that edge
    for v1 in vertices:
        for v2 in v1.adjs:
            if not v2 in v1.transversed:
                faces.append(make_face(v1, v2))
    
    return faces
                
                
    

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
    mapData.weights = ps.rook_from_shapefile(shp, idVariable = "GEOID")
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

vertices = make_vertices(mapfile)
faces = make_faces(vertices)

mapData = get_adjacencies(mapfile)
export_adjacencies(mapData)
# print(mapData.edges)



# -*- coding: utf-8 -*-
"""
Created on Thu Jun 14 23:43:10 2018

@author: tug30201
"""

from embed_perims import gen_graph_gdf
import geopandas as gpd

gdf_vtd = gpd.read_file("../data/tl_2012_33_vtd10.shp")
gdf_cd = gpd.read_file("../data/tl_rd13_33_cd113.shp")

gdf_graph = gen_graph_gdf(gdf_vtd, "../data/NH_VTD_graph.shp")

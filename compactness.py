# -*- coding: utf-8 -*-
"""
Created on Wed Jun  6 22:39:44 2018

@author: tug30201
"""

import os
import geopandas as gpd
from math import pi

def polsby_popper(geo):
    return 4 * pi * geo.area / (geo.length ** 2)

def schwartzberg(geo):
    return polsby_popper(geo) ** -0.5

def c_hull_area(geo):
    return geo.area / geo.convex_hull.area


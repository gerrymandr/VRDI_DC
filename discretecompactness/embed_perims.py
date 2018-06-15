
import geopandas as gpd
import pysal as ps
from shapely.geometry import LineString

def gen_graph_gdf(geo, filename = None, driver = "ESRI Shapefile"):
    
    centroids = geo.centroid
    c_x = centroids.x
    c_y = centroids.y
    
    # Spatial Weights
    rW = ps.weights.Rook.from_dataframe(geo)

    line_segments = []
    centroid1 = []
    centroid2 = []
    for i, jj in rW.neighbors.items():
        for j in jj:
            line = LineString([(c_x[i],c_y[i]), (c_x[j], c_y[j])])
            line_segments.append(line)
            centroid1.append(str((c_x[i],c_y[i])))
            centroid2.append(str((c_x[j],c_y[j])))
              
    # Dictionary for GeoDataFrame constructor
    # Keys become column header, values become elements of that column
    dual = {
            "centroid1": centroid1,
            "centroid2": centroid2,
            "geometry": line_segments
            }
            
    gdf_segments = gpd.GeoDataFrame(data = dual, geometry = "geometry", crs = geo.crs)
    
    # Output files
    if filename != None:
        gdf_segments.to_file(filename, driver = driver)

    return gdf_segments

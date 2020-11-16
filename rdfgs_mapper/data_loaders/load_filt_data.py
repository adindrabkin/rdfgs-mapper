from rdfgs_mapper import cfg
import geopandas as gpd
from shapely.strtree import STRtree
from shapely.geometry import MultiPolygon

"""
loading for time complexity
1. load shapefiles into polygons

2. shapley STRtree 
r-tree should inherently use bounding boxes?

3. index the data as the centroid of the polygon. This takes compute power, but is the least likely to overlap
"""


def load_states(return_polys=False):
    """
    loads the state shp file as a STRTree, and as an index
    :param return_polys: return STRtree, index, raw_polys
    :return: STRTree of state polygons, {state_polygon.centroid.coords: state_abbr}
    :note: there are multiple polygons per state, as multipolygons cant be added to an strtree
    """
    # using geopandas to load shp file since this isn't 2010
    # shpfile contains idx, STATENS, ..., GEOID (STATEFP), STUSPS (ABBR), Name,
    polys = gpd.read_file(cfg.DATA.STATE_SHP)

    # removing any rows that contain an unlisted abbreviation
    polys = polys[polys.STUSPS.isin(cfg.ST_ABBRS)]

    poly_list = []
    state_index = {}
    for i in polys.itertuples():
        this_state_abbr = i.STUSPS

        # if it is a multipolygon
        if type(i.geometry) == MultiPolygon:
            # add each polygon as the state, only if their size is decent
            for poly in i.geometry:
                if len(poly.exterior.coords) > 50:  # arbitrary number, can be adjusted
                    state_index[poly.centroid.coords[0]] = this_state_abbr
                    poly_list.append(poly)

        else:
            # loading the individual polygon
            poly = i.geometry
            state_index[poly.centroid.coords[0]] = this_state_abbr
            poly_list.append(poly)
    tree = STRtree(poly_list)

    # returning the original polys for visualizing, if requested
    if return_polys:
        return tree, state_index, polys
    return tree, state_index

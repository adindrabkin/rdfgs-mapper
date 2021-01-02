from rdfgs_mapper import cfg
import geopandas as gpd
from pandas import DataFrame
from shapely.strtree import STRtree
from shapely.geometry import MultiPolygon
from dataclasses import dataclass

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
    :return: STRTree of state polygons, {state_polygon.centroid.coords: state_abbr}, polys
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


"""
using a dataclass for the counties each state contains
"""


@dataclass()
class CountyTree:
    tree = None
    county_index = {}  # {county_polygon.centroid.coords: county_geoid}
    geoseries = None

    def __init__(self, state_fp, geodataframe, store_polys=False, ignore_geoid=set()):
        """
        :param state_fp: fp (XY) of the state
        :param geodataframe: raw geodataframe from shapefile
        :param store_polys: if geoseries.geometry should be kept (geoseries kept regardless)
        :param ignore_geoid: set of str GEOIDs {'GEOID', 'GEOID'} - to be removed soon
        """
        self.state_fp = state_fp


        self.county_index = {}  # {county_polygon.centroid.coords: county_geoid}
        poly_list = []  # required for creating the tree
        for i in geodataframe.itertuples():
            this_county_geoid = i.GEOID  # geoid is "STATEFP" + "COUNTYFP"
            if this_county_geoid in ignore_geoid:
                continue

            # if it is a multipolygon
            if type(i.geometry) == MultiPolygon:
                # add each polygon as the state, only if their size is decent
                for poly in i.geometry:
                    if len(poly.exterior.coords) > 5:  # can be adjusted; performance isnt hit; may miss square counties
                        # len > {1,..,5} all are within 15 total polys??
                        self.county_index[poly.centroid.coords[0]] = this_county_geoid
                        poly_list.append(poly)

            else:
                # loading the individual polygon
                poly = i.geometry
                self.county_index[poly.centroid.coords[0]] = this_county_geoid
                poly_list.append(poly)

        self.tree = STRtree(poly_list)

        #  deleting the geometry polygons if store_polys is false
        if not store_polys:
            geodataframe = geodataframe.drop(columns=["geometry"])
        self.geodataframe = geodataframe  # raw polygons

    def get_county_name(self, geoids):
        """
        get the county names corresponding to the geoid(s) given (set/list/str)
        :param geoids: "GEOID"/{"GEOID"}/["GEOID"]
        :return: {geoid: countyname}
        """
        geoids = set(geoids)
        geo_dict = {}
        for geo in self.geoseries[self.geoseries.GEOID.isin(geoids)]:
            geo_dict[geo.GEOID] = geo.NAME
        return geo_dict


def load_counties(stateFPs):
    """
    load a specific states' counties
    :param stateFPs: [stateFP, stateFP] - the states to grab counties of (can be set or list)
    :return: list of CountyTree dataclasses [@CountyTree]
    """

    """
    there are a few counties with multiple ids...
    29:St. Louis:29510 (st. louis) ,29189 (st. louis county)
    24:Baltimore:24510 (baltimore),24005(baltimore county)
    51:Fairfax:51600 (Fairfax) ,51059 (Fairfax county)
    51:Richmond:51760 (richmond) ,51159 (richmond county)
    51:Roanoke:51770 (roanoke),51161 (roanoke county)
    51:Franklin:51620 (franklin), 51067 (franklin county)
    """
    ignore_geoid = {"29510", "24510", "51600", "51760", "51770", "51620"}

    polys = gpd.read_file(cfg.DATA.COUNTY_SHP)

    # county polyfile stores stateIDs as str, with an zfill of 2
    str_state_fps = [str(st).zfill(2) for st in stateFPs]

    # removing any rows with STATEFP not in :param stateFPs:
    polys = polys[polys.STATEFP.isin(str_state_fps)]

    # TODO remove geoid by doing a set operation (not isin) and then remove the check from the dataclass
    # polys = polys[polys.GEOID.isin(ignore_geoid)]

    # iterate over stateFPs, creating a CountyTree (containing all counties in state X) #
    state_county_trees = []  # @CountyTree
    for fp in stateFPs:
        these_counties = polys[polys.STATEFP == fp]  # SELECT * ... WHERE STATEFP = fp
        county_tree = CountyTree(fp, these_counties, ignore_geoid=ignore_geoid)
        state_county_trees.append(county_tree)

    return state_county_trees



def load_county_geoid(stateFPs):
    """
    load a json containing {state: {geoid: county_name}}
    :param stateFPs: list/dict of stateFPs (ca
    :return: {statefp: {geoid: county_name}}
    """
    import json
    with open(cfg.DATA.COUNTY_GEOIDS) as f:
        geos = json.load(f)
    return {statefp: geos.get(str(statefp).zfill(2)) for statefp in stateFPs}

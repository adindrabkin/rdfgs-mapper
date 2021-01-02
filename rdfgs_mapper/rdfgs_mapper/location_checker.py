"""
Given the route, where does the user go?
"""
from collections import defaultdict
from shapely.geometry import Point, LineString


def linestring_to_cordlist(linestring):
    """
    converts a linestring to a list of Points
    :param linestring:
    :return: [Points]
    """
    return [Point(tuple(list(cord[:-1]))) for cord in linestring.coords]

def points_in_polytree(usr_locs, poly_tree, poly_guide, save_cords=True):
    """
    :param line: LineString (userdata) or [Point]
    :param poly_tree: Packed STRTree of Polygons to compare against
    :param poly_guide: {(x,y): state_id} - (x,y) is the center point of the Polygon
    :return: {locality ids: [coordinates]}
    """
    local_to_cord = defaultdict(list)
    if type(usr_locs) == LineString: # LineString -> [Point]
        usr_locs = linestring_to_cordlist(usr_locs)
    for cord in usr_locs:
        # TODO this should skip cords that are too close together to save compute time (low risk points)
        res = poly_tree.query(cord)
        this_geom_id = poly_guide[tuple(res[0].centroid.coords)[0]]  # state id (center of the state)
        if save_cords:
            local_to_cord[this_geom_id].append(cord)
        else:
            local_to_cord[this_geom_id] = []  # should revisit how this is done

    return local_to_cord



"""
Visualize shape files. Useful for testing data and for (eventually) displaying a map to the user
"""
import sys

sys.path.append("..")  # TODO remove me once project is packaged
import matplotlib.pyplot as plt
from numpy import asarray
import geopandas as gpd


def plot_point(g, o, l):
    """
    :param g: geoms {x,y}
    :param o: shape/color?
    :param l: label
    """
    return plt.plot([g.x], [g.y], o, label=l)


def plot_line(g, o):
    """
    :param g: geoms {x,y}
    :param o: shape/color?
    """
    a = asarray(g)
    plt.plot(a[:, 0], a[:, 1], o)


#
def fill_polygon(g, o):
    a = asarray(g.exterior)
    plt.fill(a[:, 0], a[:, 1], o, alpha=0.5)


def fill_multipolygon(g, o):
    for g in g.geoms:
        fill_polygon(g, o)


def visualize(state_polys, county_polys=None, found_states=None, route=None):
    """
    Displays the polygons given. Puts the route on top of the polygons, if provided
    :param state_polys:
    :param county_polys:
    :param found_states: [STATE_ABBR] - highlights states
    :param route: None or {'route': LINESTRING, 'start': POINT, 'end': POINT}
    """
    # TODO when plotting, plot highlighting the inroute column
    state_polys['inroute'] = state_polys.apply(
        lambda x: 1 if x['STUSPS'] in found_states else 0, axis=1)

    base = state_polys.plot(figsize=(20, 10), edgecolor='black', column='inroute')
    if route is not None:
        route_gdf = gpd.GeoDataFrame([['A', route['start'], route['end'], route['route']]],
                                         columns=['id', 'beg_pt', 'end_pt', 'LineString_obj'],
                                         geometry='LineString_obj')  # declare LineString (last column) as the `geometry

        route_gdf.plot(ax=base, color='red')

    # TODO look at https://geopandas.org/mapping.html near the bottom

    plt.tight_layout()
    plt.show()

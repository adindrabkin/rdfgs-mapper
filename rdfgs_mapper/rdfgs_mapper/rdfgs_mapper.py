"""
main file fur running the rdfgs script
"""
import sys

import fiona  # needs to be imported before geopandas for some reason
from rdfgs_mapper.data_loaders import load_filt_data, load_user_route, load_rdfgs_xls
import rdfgs_mapper.rdfgs_mapper.location_checker as location_checker
from rdfgs_mapper import cfg
from rdfgs_mapper.visualize import visualize


def display_route(state_polys, county_polys, usr_kml):
    visualize.visualize(state_polys, county_polys, route=usr_kml)


def tabulate_result(res, title=None):
    """
    Create a nice table as the result
    :param res: [{name: name, other data: other data}] - must be uniform (i.e all keys the same, vals can be diff)
    """
    from beautifultable import BeautifulTable
    table = BeautifulTable()

    # set the title if applicable
    if title is not None:
        table.title = title

    # unspecific parameters to allow for county usage in the future
    headers = ['name']
    [headers.append(i) for i in list(res[0].keys()) if i != "name"]
    table.columns.header = headers
    for i in res:
        table.rows.append([str(i[k]) if i[k] else "" for k in headers])
    table.columns.alignment['notes'] = BeautifulTable.ALIGN_LEFT

    from os import get_terminal_size
    width = get_terminal_size().columns
    table.maxwidth = width
    print(table)

def run():
    """
    extract the route from the user path
    run it against the states
    for each state
        save the state
        check path against state.counties
            save each county

    """
    # TODO this should be overhauled to argparse
    try:
        usr_kml = sys.argv[1]
    except:
        print("load_user_data.py ran directly without a kml arg provided")
        exit(1)
    usr_data = load_user_route.run(usr_kml)  # {'route': linestring, 'start': point, 'end': point}
    print(f"locating {usr_data['start']} to {usr_data['end']}")
    state_tree, state_index, state_polys = load_filt_data.load_states(return_polys=True)
    found_states = location_checker.points_in_polytree(usr_data['route'], state_tree, state_index)


    # mapping state abbr to statefp
    found_state_fps = [str(cfg.ST_ABBRS[st]).zfill(2) for st in found_states]

    rdfgs = load_rdfgs_xls.Rdfgs_Xl()
    state_results = []

    for state in found_states:
        state_police = rdfgs.get_state_police(state)
        state_police['name'] = state
        state_results.append(state_police)

    tabulate_result(state_results, title="State Police")
    visualize.visualize(state_polys, found_states=list(found_states.keys()), route=usr_data)

    # only loading the counties trees that exist within found_state_fps
    # state_county_trees = [@CountyTree] for each state
    state_county_trees = load_filt_data.load_counties(found_state_fps)

    found_counties = {}  # {"statefp": {"county"}}

    # iterating over the county data for each state located
    for st in state_county_trees:  # for each @CountyTree
        state_abbr = cfg.STATE_ID_ABBR[int(st.state_fp)]  # i.e 6 -> CA since found_states is by abbr
        # found_states[st.state_fp] refers to the points confirmed to be in the current state
        found_counties = location_checker.points_in_polytree(found_states[state_abbr],
                                                             st.tree,
                                                             st.county_index,
                                                             save_cords=False)
        print(found_counties)
        exit()


    found_county_geos = [county for county in found_counties]

    for county in found_counties:
        county_police = rdfgs.get_county_info(state, county)
        state_police['name'] = state
        state_results.append(state_police)


   # TODO iterate over counties found



    exit()
    print("Located the following states:")
    print("note: general state info is not included yet. Check rdfgs.rdforum.org for state summaries")

    county_results = {}





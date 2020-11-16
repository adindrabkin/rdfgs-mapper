import geopandas as gpd
gpd.io.file.fiona.drvsupport.supported_drivers['KML'] = 'rw'



def run(usr_kml):
    """
    :param usr_kml_path: path to the user's KML file from gmaps
    :return: {'route': LINESTRING, 'start': POINT, 'end': POINT}
    """
    try:
        usr_extracted_kml = gpd.read_file(usr_kml, driver='KML')
    except:
        raise("unable to load the user's kml file with the gpd KML driver")
    try:
        route_line = usr_extracted_kml.geometry[0]
        start = usr_extracted_kml.geometry[1]
        end = usr_extracted_kml.geometry[2]
    except:
        raise("KML file possibly corrupted; unable to extract data points")
    return {'route':route_line, 'start':start, 'end': end}





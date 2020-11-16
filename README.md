# rdfgs-mapper
A tool to map rdforum.org RDFGS based on a provided route

### How to use
#### Pre-reqs
1. Download the latest version of python (https://www.python.org/)
2. Verify that all the required data is satisfied (including the route of your choosing!)
3. Using the terminal, navigate to the rdfgs-mapper main directory
3b. If you are on windows, please follow the "windows" steps at the bottom of the readme before you continue
4. run "pip3 install ." in the rdfgs-mapper main directory

#### usage
$> rdfgs-mapper [path_to_kml_file.kml]

### Required data (not automated yet)
#### 1. A US state shape file from the following URL  - INCLUDED IN ALPHA VERSION
(States section). 500k is preferred, but smaller should work. 
https://www.census.gov/geographies/mapping-files/time-series/geo/carto-boundary-file.html

Direct link: https://www2.census.gov/geo/tiger/GENZ2018/shp/cb_2018_us_state_500k.zip
a. Unzip this file and place it in the "data" folder, specifically as data/cb_2018_us_state_500k/[unzipped contents]

#### 2. RDFGS-Archive.xls - INCLUDED IN ALPHA VERSION
This is currently provided, but is from 2017, and is primarily for testing rather than accuracy. The current version was taken from https://www.rdforum.org/threads/59672/, then converted to xls to work with python

#### 3. A route of your choosing! This is the fun part.\
Here is how it's done:\
a. Go to google.com/maps/d \
b. click "Create a new map" in the top left. Wait for the map to appear\
c. underneath the search bar, near the top of the page, there is an icon that, when hovered, says "Add Directions". Click this, and a new layer should appear\
d. On the left side of the screen, there is now a Untitled layer that says "Driving". Modify the start and end to your liking, and a blue line should appear. Add as many stops/destinations as wanted\
    pro tip: you can drag the line to manually change the route\
e. in the top left, to the right of "untitled map" click the 3 dots. A dropdown box should appear. Click "Export to KML/KMZ"\
f. Click the box that says "entire map" and change it to Directions from [location] to [location]\
g. Check the box that says "Export as KML instead of KMZ"\
e. Download it!\


#### Special Windows Steps (3b)
Make sure NONE of the following have older versions installed (you may need to manually remove older versions of python). Once done, do the following commands, in the following order:\
pip install wheel\
pip install pipwin\

pipwin install numpy\
pipwin install pandas\
pipwin install shapely\
pipwin install gdal\
pipwin install fiona\
pipwin install pyproj\
pipwin install descartes\
pipwin install geopandas\

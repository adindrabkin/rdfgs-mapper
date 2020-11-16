from collections import namedtuple
import os.path

DATA_FOLDER = os.path.join(os.path.dirname(__file__), 'rdfgs_data')


_DATA = namedtuple('DATA', ['STATE_SHP', 'RDFGS'])
DATA = _DATA(STATE_SHP=os.path.join(DATA_FOLDER,"cb_2018_us_state_500k", "cb_2018_us_state_500k.shp"),
             RDFGS=os.path.join(DATA_FOLDER,"RDFGS-Archive.xls"))


STATE_ID_ABBR = {28: 'MS', 37: 'NC', 40: 'OK', 51: 'VA', 54: 'WV', 22: 'LA', 26: 'MI', 25: 'MA', 16: 'ID', 12: 'FL', 31: 'NE', 53: 'WA', 35: 'NM', 46: 'SD', 48: 'TX', 6: 'CA', 1: 'AL', 13: 'GA', 42: 'PA', 29: 'MO', 8: 'CO', 49: 'UT', 47: 'TN', 56: 'WY', 36: 'NY', 20: 'KS', 32: 'NV', 17: 'IL', 50: 'VT', 30: 'MT', 19: 'IA', 45: 'SC', 33: 'NH', 4: 'AZ', 11: 'DC', 34: 'NJ', 24: 'MD', 23: 'ME', 10: 'DE', 44: 'RI', 21: 'KY', 39: 'OH', 55: 'WI', 41: 'OR', 38: 'ND', 5: 'AR', 18: 'IN', 27: 'MN', 9: 'CT'}
ST_ABBRS = set([v for k, v in STATE_ID_ABBR.items()])

# currently required for Rdfgs_Xl
STATE_ABBREV = {
    'Alabama': 'AL',
    'Alaska': 'AK',
    'Arizona': 'AZ',
    'Arkansas': 'AR',
    'California': 'CA',
    'Colorado': 'CO',
    'Connecticut': 'CT',
    'Delaware': 'DE',
    'District of Columbia': 'DC',
    'Florida': 'FL',
    'Georgia': 'GA',
    'Hawaii': 'HI',
    'Idaho': 'ID',
    'Illinois': 'IL',
    'Indiana': 'IN',
    'Iowa': 'IA',
    'Kansas': 'KS',
    'Kentucky': 'KY',
    'Louisiana': 'LA',
    'Maine': 'ME',
    'Maryland': 'MD',
    'Massachusetts': 'MA',
    'Michigan': 'MI',
    'Minnesota': 'MN',
    'Mississippi': 'MS',
    'Missouri': 'MO',
    'Montana': 'MT',
    'Nebraska': 'NE',
    'Nevada': 'NV',
    'New Hampshire': 'NH',
    'New Jersey': 'NJ',
    'New Mexico': 'NM',
    'New York': 'NY',
    'North Carolina': 'NC',
    'North Dakota': 'ND',
    'Ohio': 'OH',
    'Oklahoma': 'OK',
    'Oregon': 'OR',
    'Pennsylvania': 'PA',
    'Puerto Rico': 'PR',
    'Rhode Island': 'RI',
    'South Carolina': 'SC',
    'South Dakota': 'SD',
    'Tennessee': 'TN',
    'Texas': 'TX',
    'Utah': 'UT',
    'Vermont': 'VT',
    'Virgin Islands': 'VI',
    'Virginia': 'VA',
    'Washington': 'WA',
    'West Virginia': 'WV',
    'Wisconsin': 'WI',
    'Wyoming': 'WY',
  }




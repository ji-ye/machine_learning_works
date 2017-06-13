'''
Python code for Machine Learning 30254 homework 1

Note: The following code is used for probing unfamiliar datasets and therefore
was written in a quick and nasty way to save human's time but not necessarily
computer run time.

Ji, Ye                       student ID: 12147151
'''
from datetime import datetime
from xml.etree import ElementTree
import requests
import pandas as pd
from pandas.stats.api import ols
# import numpy as np
#import json
import matplotlib.pyplot as plt
import seaborn as sns


'''
Problem 1: Data Acquisition and Analysis
'''
def count_requests():
    '''
    Helper function. Count the number of request by category.
    '''
    print('graffitti:  ', len(graffitti))
    print('pothole:    ', len(pothole))
    print('sanitation: ', len(sanitation))
    print('building:   ', len(building))

def calc_day_lapse(date1, date2):
    '''
    Helper function. Count the days between two days.

    Input:
        date1 & date2: (python datetime objects)

    Return:
        day_lapse: (int)
    '''
    delta = date2 - date1
    return delta.days

### Problem 1.1 Download and Combine Data
graffitti = pd.read_csv('311_Service_Requests_-_Graffiti_Removal.csv')
pothole = pd.read_csv('311_Service_Requests_-_Pot_Holes_Reported.csv')
sanitation = pd.read_csv('311_Service_Requests_-_Sanitation_Code_Complaints.csv')
building = pd.read_csv('311_Service_Requests_-_Vacant_and_Abandoned_Buildings_Reported.csv')

# Create Chicago Community list from city dataset "Community Areas"
# Defines neighborhood as Community Area.
nbhd = pd.read_csv('CommAreas.csv')
community_raw = []
CHICAGO_COMMUNITY_TOTAL = list(range(1, 78))

for num in nbhd['AREA_NUM_1']:
    if num in CHICAGO_COMMUNITY_TOTAL:
        community_raw.append((num, nbhd[nbhd['AREA_NUM_1']==num]['COMMUNITY'].iloc[0]))
community_raw.sort()

community = ['Community Name']
for num, name in community_raw:
    community.append(name) # index is area number, value is neighborhood name.
'''
Problem 1.2 Generate Summary statistics.
            1.2.1 number of requests by type
            1.2.2 by neighborhood
            1.2.3 response time by the city
'''
# print('\n', 'number of rows from raw data', '\n')
# count_requests()

# some format cleaning
graffitti['What Type of Surface is the Graffiti on?'].replace\
('Other / Unknown Surface', 'Other/Unknown Surface', inplace=True)

# Sanitation and building dataframe require cleaning.
# delete the repeated column headers to get rid off NaN.
sanitation = sanitation.drop(sanitation.index[0])
building = building.drop(building.index[0])

# get past year data
PATTERN = '2016'
graffitti = graffitti[graffitti[graffitti.columns[0]].str.contains(PATTERN)]
pothole = pothole[pothole[pothole.columns[0]].str.contains(PATTERN)]
sanitation = sanitation[sanitation[sanitation.columns[0]].str.contains(PATTERN)]
building = building[building[building.columns[2]].str.contains(PATTERN)]

# print('\n', 'number of requests in 2016 with duplicates', '\n')
# count_requests()

# remove duplicates from graffitti, pothole, sanitation:
graffitti = graffitti[graffitti[graffitti.columns[1]] != 'Completed - Dup']

pothole = pothole[pothole[pothole.columns[1]] != 'Completed - Dup']
pothole = pothole[pothole[pothole.columns[1]] != 'Open - Dup']

sanitation = sanitation[sanitation[sanitation.columns[1]] != 'Completed - Dup']
sanitation = sanitation[sanitation[sanitation.columns[1]] != 'Open - Dup']

# write cleaned df to csv.
graffitti.to_csv('graffitti_cleaned.csv')
sanitation.to_csv('sanitation_cleaned.csv')
pothole.to_csv('pothole_cleaned.csv')
building.to_csv('building_cleaned.csv')
### 1.2.1 number of requests by type
# print('\n', 'number of requests  in 2016', '\n')
# count_requests()

# inspecting subtypes of interests.
print(graffitti['What Type of Surface is the Graffiti on?'].value_counts())
print(sanitation['What is the Nature of this Code Violation?'].value_counts())
print(pothole['NUMBER OF POTHOLES FILLED ON BLOCK'].value_counts())
print(building['ANY PEOPLE USING PROPERTY? (HOMELESS, CHILDEN, GANGS)'].value_counts())

# initiate a dictionary to hold by neighborhood count.
requests_2016 = {
    'graffitti': {
        'total': len(graffitti), 'by neighborhood':{}},
    'pothole': {
        'total': len(pothole), 'by neighborhood':{}},
    'sanitation': {
        'total': len(sanitation), 'by neighborhood':{}},
    'building': {
        'total': len(building), 'by neighborhood':{}}
}


### 1.2.2 number of requests by neighborhood
requests_lst = [graffitti, pothole, sanitation, building]
requests_types = ['graffitti', 'pothole', 'sanitation', 'building']

CHICAGO_COMMUNITY_NUMBER = range(1, len(community))

for i in range(len(requests_types)):
    for num in CHICAGO_COMMUNITY_NUMBER:
        if num not in requests_2016[requests_types[i]]['by neighborhood']:
            requests_2016[requests_types[i]]['by neighborhood'][community[num]] = 0
            for j in requests_lst[i]['Community Area']:
                # filter out nan:
                if j == j:
                    if int(j) == num:
                        requests_2016[requests_types[i]]['by neighborhood'][community[num]] += 1

### 1.2.3 response time by the city
# For the past year, graffitti and sanitation requests are all resolved.
# One pothole case remains open.
datetime_pattern = '%m/%d/%Y'

requests_lst_response = [graffitti, pothole, sanitation]
requests_types_response = ['graffitti', 'pothole', 'sanitation']

for i in range(len(requests_types_response)):
    requests_2016[requests_types_response[i]]['by response time'] = {}
    total_time = 0
    for j in range(len(requests_lst_response[i])):
        request_date_str = requests_lst_response[i][requests_lst_response[i].columns[0]].iloc[j]
        resolve_date_str = requests_lst_response[i][requests_lst_response[i].columns[2]].iloc[j]
        if request_date_str == request_date_str and resolve_date_str == resolve_date_str:
            request_date = datetime.strptime(request_date_str, datetime_pattern)
            resolve_date = datetime.strptime(resolve_date_str, datetime_pattern)

            response_time = calc_day_lapse(request_date, resolve_date)
            total_time += response_time

            response_time_str = str(response_time) + ' days'
            if response_time_str not in requests_2016[requests_types_response[i]]['by response time']:
                requests_2016[requests_types_response[i]]['by response time'][response_time_str] = 0
                requests_2016[requests_types_response[i]]['by response time'][response_time_str] += 1
    requests_2016[requests_types_response[i]]['by response time']['average'] = total_time / len(requests_lst_response[i])

# There is no city response for vacant/abandoned buildings.
requests_2016['building']['by response time'] = None

'''
Problem 1.3 Five findings

    1.3.1 Finding #1: Average response time:
            graffitti: 0.59 day
            sanitation: 9.41 days
            pothole: 21.57 days

    1.3.2 Finding #2: Top-fives neighborhoods:
            1.3.2.1 most graffitti request:
                        (4885, 'LOWER WEST SIDE'),
                        (5339, 'AVONDALE'),
                        (5984, 'BRIGHTON PARK'),
                        (7881, 'LOGAN SQUARE'),
                        (9149, 'WEST TOWN')
                    least graffitti request:
                        (12, 'OAKLAND'),
                        (12, 'RIVERDALE'),
                        (31, 'PULLMAN'),
                        (38, 'AVALON PARK'),
                        (41, 'BURNSIDE'),

            1.3.2.2 most sanitation request:
                        (617, 'AUBURN GRESHAM'),
                        (716, 'LOGAN SQUARE'),
                        (747, 'WEST TOWN'),
                        (748, 'AUSTIN'),
                        (769, 'LINCOLN PARK')
                    least sanitation request:
                        (7, 'RIVERDALE'),
                        (17, 'OHARE'),
                        (20, 'EDISON PARK'),
                        (24, 'OAKLAND'),
                        (32, 'MONTCLARE'),

            1.3.2.3 most pothole request:
                        (1006, 'NORWOOD PARK'),
                        (1015, 'AUSTIN'),
                        (1099, 'NEAR WEST SIDE'),
                        (1114, 'NEAR NORTH SIDE'),
                        (1194, 'WEST TOWN')],
                    least pothole request:
                        (63, 'OAKLAND'),
                        (75, 'FULLER PARK'),
                        (80, 'BURNSIDE'),
                        (102, 'RIVERDALE'),
                        (125, 'WEST GARFIELD PARK'),

            1.3.2.4 most vacant building:
                        (249, 'NEW CITY'),
                        (280, 'AUBURN GRESHAM'),
                        (297, 'ROSELAND'),
                        (316, 'ENGLEWOOD'),
                        (453, 'WEST ENGLEWOOD')
                    least vacant building:
                        (0, 'NEAR SOUTH SIDE'),
                        (0, 'OHARE'),
                        (1, 'EDISON PARK'),
                        (1, 'LOOP'),
                        (1, 'ROGERS PARK'),

    1.3.3 Finding #3: Correlations:
        Between the requests, graffitti is postively related to sanitation,
        negatively related to vacant building, and has no significant relationship
        with pothole. Pothole has a postive correlation with sanitation. And
        sanitation has significant correlations with all other requests.

        The OLS result can be a good data point for talking about Broken Window theory.

    1.3.4 Finding #4: Implications
        If we are choosing neighborhood to live in, without more detailed information,
        the cleanness of a neighborhood could be used as a key indicator to eyeball.
        If a neighborhood is not clean, chances are it also has other issues.

        Stay out of West Town.

    1.3.5 Finding #5: How good of neighborhood is Hyde Park?
        Overall, not bad.
'''
# by neighborhood dictionary
by_nbhd = {}
for i in requests_types:
    if i not in by_nbhd:
        by_nbhd[i] = {}
    for j in requests_2016[i]['by neighborhood']:
        data = requests_2016[i]['by neighborhood'][j]
        by_nbhd[i][j] = data

df = pd.DataFrame.from_dict(by_nbhd)
result = ols(y=df['graffitti'], x=df[['building','sanitation', 'pothole']])
# print(result)


'''
Problem 2: Data Augmentation and APIs.

I am using ACS five year survey, it is the only dataset with block-level information.
'''
# building ACS api url, Doesn't seemed to require the key.
URL = 'http://api.census.gov/data/2015/acs5?get=B19013_001E,B01002_001E,B25010_001E,B01003_001E,B02011_001E&for=block+group:*&in=state:17&in=county:031&in=tract:__&key=517133652724f582b45535934e611443a4eda48e'
STATE_FIPS = '17'
COUNTY_FIPS = '031'
HEADERS = 'B19013_001E,B01002_001E,B25010_001E,B01003_001E,B02011_001E'
          # mean income, median age, avg hh size, population, Asian population

tracts_chicago = pd.read_csv('CensusTractsTIGER2010.csv')
tracts_chicago = tracts_chicago['TRACTCE10']

CHICAGO_TRACTS_STR = ''

for i in tracts_chicago:
    text = str(i) + ','
    CHICAGO_TRACTS_STR += text

CHICAGO_TRACTS_STR = CHICAGO_TRACTS_STR[:-1]
URL = URL.replace('__', CHICAGO_TRACTS_STR)
r = requests.get(URL)
request_json = r.json()
tracts_df = pd.DataFrame(request_json)
headers = ['mean income', 'median age', 'average household size', 'population', 'Asian population', 'state', 'county', 'tract', 'block group']
tracts_df.columns = headers
tracts_df = tracts_df[1:]
# Builds tracts_df, a dataframe that contains all the returned data from ACS API.
# Save the dataframe locally to replace ACS API.
# I could write code in a way that it queries the ACS in real time, but the data
# itself is not in real-time, so I don't see the point. Plus, loading it to Pandas
# makes it easier for me to learn about the dataset information.

def latlng_to_block(lat, lng):
    '''
    Given a coordinate, returns the corresponding block id in tracts_df.
    Used ElementTree package to parse xml & fcc API.

    Input: (float) lat, lng

    Return: (tuple) tract, block
    '''
    fcc_url = 'http://data.fcc.gov/api/block/find?latitude=[latitude]&longitude=[longitude]&showall=true'
    fcc_url = fcc_url.replace('[latitude]', str(lat)).replace('[longitude]', str(lng))

    r = requests.get(fcc_url)
    tree = ElementTree.fromstring(r.content)
    # save tract and block number by position.
    full_id = tree[0].attrib['FIPS'][5:]
    # tract = tree[0].attrib['FIPS'][5:11]
    # block = tree[0].attrib['FIPS'][11:12]
    return full_id


# For looking up all defined pandas dataframe
# ds_vars = [graffitti, pothole, sanitation, building, tracts_chicago, tracts_df, nbhd, by_nbhd, df]

'''
P2.1 What types of blocks get "Vacant and abandoned buildings" Reported?
P2.2 What types of blocks get "Sanitation Code Complaints"?
P2.3 Does that change over time in the data you collected?
P2.4 What is the difference in blocks that get "Vacant and abandoned buildings"
     vs. "Sanitation Code Complaints"?
'''
#2.1 What types of blocks get "Vacant and abandoned buildings" Reported?
#building.columns
#tracts_df.columns

#building[building['Location'].isnull()] # has one, index is 53664

# count vacant building for each block groups.
# request_date = datetime.strptime(request_date_str, datetime_pattern)
# END_OF_YEAR_DATE = datetime.strptime('12/31/2016', datetime_pattern)
# DAYS_IN_LAST_THREE_MONTHS = 92
#
# building_3mo = pd.DataFrame()
# #count = 0
# for i in range(len(building)):
#     time_str = building['DATE SERVICE REQUEST WAS RECEIVED'].iloc[i]
#     request_date = datetime.strptime(time_str, datetime_pattern)
#     # find request that dates within the last three months of 2016.
#     if calc_day_lapse(request_date, END_OF_YEAR_DATE) <= DAYS_IN_LAST_THREE_MONTHS:
#         #count += 1
#         #print()
#         building = building_3mo.append(building.iloc[i])
# #print(count)

# building_byBlock = {}
# for i in range(len(building)):
#     lat = building['LATITUDE'].iloc[i]
#     lng = building['LONGITUDE'].iloc[i]
#     if lat == lat and lng == lng:
#         tract, block_group, full_id = latlng_to_block(lat, lng)
#         #block_df = tracts_df[tracts_df['tract'] == tract and tracts_df['block group'] == block_group]
#         if full_id not in building_byBlock:
#             building_byBlock[full_id] = 0
#         building_byBlock[full_id] += 1

# rename
block_df = tracts_df
'''
latlng_lst = []
for i in range(len(building)):
    lat = building['LATITUDE'].iloc[i]
    lng = building['LONGITUDE'].iloc[i]
    if lat == lat and lng == lng:
        location = (lat, lng)
        latlng_lst.append(location)

# running ever slowly, works for a hundred, but needs to process 4000+.
bldg_by_block = {}
for location in latlng_lst:
    lat, lng = location
    fips = latlng_to_block(lat, lng)
    # t, b = rv
    if str(fips) not in bldg_by_block:
        bldg_by_block[str(fips)] = 0
    bldg_by_block[str(fips)] += 1
'''
#
# for i in bldg_by_block:
#     count = bldg_by_block[i]
#     bldg_by_block[i] = {'count':count, 'nbhd':[]}
#     tract_str = i[:6]
#     block_str = i[6:7]
#     print(tract_str, i)
#     for j in range(len(block_df['tract'])):
#         if tract_str == block_df['tract'].iloc[j]:
#             # print(tract_str, block_str)
#             tract_slice = block_df[block_df['tract']==tract_str]
#             block_slice = tract_slice[tract_slice['block group']==block_str]
#             bldg_by_block[i]['nbhd'] = block_slice

for i in bldg_by_block:
    count = bldg_by_block[i]
    bldg_by_block[i] = {'count':count, 'nbhd':[]}
    tract_str = i[:6]
    block_str = i[6:7]
    print(tract_str, i)
    for j in range(len(block_df['tract'])):
        if tract_str == block_df['tract'].iloc[j]:
            # print(tract_str, block_str)
            tract_slice = block_df[block_df['tract']==tract_str]
            block_slice = tract_slice[tract_slice['block group']==block_str]
            bldg_by_block[i]['nbhd'] = block_slice

sani_b_char = []
# avg_income = 0
for k in sani_b:
    for j in range(1, len(block_df)):
        total = 0
        if k[:6]==block_df['tract'].iloc[j]:
            if block_df['mean income'][j]:
                total += float(block_df['mean income'][j])
        avg_income = total / len(block_df)
        sani_b_char.append(avg_income)
'''
Problem 3
'''

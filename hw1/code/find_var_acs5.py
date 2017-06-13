'''
Functions used to explore/export ACS 5-year data variables.
'''

import os
import requests


def find_ACS_var(keyword):
    '''
    Find summary data variables in the ACS five-year dataset. This function searches
    the given keyword in ACS5 variable's concept tag. Reference American FactFinder's
    generated tables for keyword of interests.

    Input:
        keyword: (str) First letter must be capitalized.
            examples: 'Total Population', 'Median Income', 'Race', 'Asian', 'Median Age'

    Return: (list) data_kw_lst

    Output: (txt file)
    '''
    r = requests.get('http://api.census.gov/data/2015/acs5/variables.json')
    json_data = r.json()

    PuertoRico_DATA_PATTERN = 'PR'
    SUM_DATA_PATTERN = '_001E'

    data_kw_lst = []
    for variable in json_data['variables']:
        # if the variable is not part of Puerto Rico data, and is a summary data.
        if keyword in json_data['variables'][variable]['concept'] and\
         PuertoRico_DATA_PATTERN not in variable and SUM_DATA_PATTERN in variable:
            # 'PR' is the keyword for Puerto Rico Data.
            var_concept = json_data['variables'][variable]['concept'].split('.')[1]
            var_label = json_data['variables'][variable]['label']
            rv = (variable, var_concept, var_label)
            data_kw_lst.append(rv)
    data_kw_lst.sort()

    # write to txt for viewing pleasure.
    filename_str = keyword.replace(' ', '_')
    file_name = '{}_keyword_list.txt'.format(filename_str)

    f = open(file_name,'w')
    for i in data_kw_lst:
        k, data, label = i
        data = data.lstrip()
        f.write(k + ': ' + data + '\n')
    f.close()

    cmd = 'open ' + file_name
    print(cmd)
    os.system(cmd)

    return data_kw_lst

### sample, the variable may return null for the block-level dataset.
data_kw_lst = find_ACS_var('Asian')

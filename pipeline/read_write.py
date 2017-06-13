'''
Functions for reading and writing data using Pandas.
'''
import re
import pandas as pd


def get_ext(filepath):
    '''
    Given a filename, return its extension.

    Input:
        filepath: (str)

    Return:
        extension: (str) in form of ".xxx"
    '''
    extension = re.search('.\w+$', filepath).group()
    return extension


def read_data(filepath):
    '''
    Reads csv, dta, excel, json, and pickle file. Load it as Pandas DataFrame.

    Input:
        filepath: (str)

    Return: DataFrame.
    '''
    extension = get_ext(filepath)
    assert extension in ['.csv', '.dta', '.xlsx', '.xls', '.json', '.pkl'],\
    "read_data function does not support reading {} file".format(extension)

    if extension == '.csv':
        df = pd.read_csv(filepath)
    elif extension == '.dta':
        df = pd.read_stata(filepath)
    elif extension == '.xlsx':
        df = pd.read_excel(filepath)
    elif extension == '.json':
        df = pd.read_json(filepath)
    elif extension == '.pkl':
        df = pd.read_pickle(filepath)
    return df


def write_data(df, filename):
    '''
    Write DataFrame to csv, pickle，or stata file.

    Input:
        df: DataFrame
        filepath: (str)

    Output: Specified file.
    '''
    extension = get_ext(filepath)
    assert extension in ['.csv', '.dta', '.pkl'],\
    "write_data function does not support writing to {} file".format(extension)

    if extension == '.csv':
        df.to_csv(filename)
    elif extension == '.pkl':
        df.to_pickle(filename)
    elif extension == '.dta':
    # sometimes needed in program evaluation for doing Stata-specific operations.
        df.to_stata(filename)

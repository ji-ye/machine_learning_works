'''
Pipeline 1 of 6: Read and Write Data

For this section of the pipeline, the main change I made is rewriting the
read_data function so it reads several common file types instead of only csv
files. Then I added a similar write_data function.

- JY
'''
import re
import pandas as pd


def read_data(filepath):
    '''
    Reads csv, dta, excel, and json file. Load it as Pandas DataFrame.
    Return: DataFrame.
    '''
    extension = re.search('.\w+$', filepath).group()
    assert extension in ['.csv', '.dta', '.xlsx', '.xls', '.json'],\
    "this function can only read file with csv, dta, xlsx, xls, and json extensions"
    if extension == '.csv':
        df = pd.read_csv(filepath)
    elif extension == '.dta':
        df = pd.read_stata(filepath)
    elif extension == '.xlsx':
        df = pd.read_excel(filepath)
    elif extension == '.json':
        df = pd.read_json(filepath)
    return df


def write_data(df, filename):
    '''
    Write DataFrame to either csv or dta file.
    '''
    extension = re.search('.\w+$', filename).group()
    assert extension in ['.csv', '.dta', '.xlsx'],\
    "can only write to file with csv or dta extensions."
    if extension == '.csv':
        df.to_csv(filename)
    elif extension == '.dta':
    # sometimes needed in program evaluation to do Stata-specific operations.
        df.to_stata(filename)

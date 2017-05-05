'''
Pipeline 3 of 6: Pre-process Data

The major changes of Data Pre-processing is:
Improved fill missing value function. It can now take a parameter to fill
missing value by any new value (mean, mode, median, or just any about anything).
This change is made in response of TA feedback from the last assignment that I
should write a more generic fill missing value function to take missing values
in discrete and categorical variables into consideration.

- JY
'''
import pandas as pd


def fill_missing(col, new_value=None):
    '''
    Check and fill missing values in a pd.Series instance.

    Input:
        col: DataFrame Series
        new_value: value to fill the missing value. For discrete and categorical
         variables, it could be col.mode(), col.median(), zero, or any value.

    Return: None
    '''
    assert col.hasnans, "This column has no missing value."
    col.fillna(new_value, inplace=True)
    return


def preprocess_data(missing_val_col, new_value=None):
    '''
    Function that groups other pre-process functions.
    For now it only consists of filling missing values.

    Input:
        df: DataFrame
        missing_val_col: (list) of missing value columns
        new_value: value to fill the missing value. For discrete and categorical
         variables, it could be col.mode(), col.median(), zero, or any values.

    Return: None
    '''
    fill_missing(missing_val_col, new_value)

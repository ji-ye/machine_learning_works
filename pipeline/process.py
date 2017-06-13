'''
Some helper functions to process data.
'''
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import RobustScaler, StandardScaler, MinMaxScaler


def report_missing(df):
    """
    Get a report about the number of missing values in the df.

    Arg:
        df: pandas.DataFrame

    Return:
        rv: df; a report about missing values in descending order,
            containing the data types, the number of missing values,
            and the proportion of missing values for each attribute
    (by Han, Shen)
    """
    rv = pd.concat([pd.DataFrame(df.dtypes), df.isnull().sum()], axis=1)
    rv.columns = ['Type', 'Num_of_NaNs']
    rv.sort_values('Num_of_NaNs', ascending=False, inplace=True)
    rv['Proportion'] = rv.Num_of_NaNs / df.shape[0]
    return rv


def scale(X_train, X_test, scaling_type='robust'):
    '''
    Scale a list of DataFrame series using sklearn robust scaling after train-test-split.

    Input:
        X_train: DataFrame
        X_test: DataFrame
        cols: (list) of Series (DataFrame Columns)
        scaling_type: (str) can be any one of sklearn preprocessing's scaler
    Return: None, modification in place.

    Note: This is a makeshift function for use along the way.
    '''
    X_features=X_train.columns

    if scaling_type == 'robust':
        scaler = RobustScaler()
    elif scaling_type == 'minmax':
        scaler = MinMaxScaler()
    elif scaling_type == 'standard':
        scaler = StandardScaler()

    for i in X_features:
        X_train[i] = scaler.fit_transform(X_train[i].values.reshape(-1,1))
        X_test[i] = scaler.transform(X_test[i].values.reshape(-1,1))

    return


def cat_to_dummy(df, cat_cols, drop=True):
    '''
    Convert categorical variable into new columns of dummy/indicator variables.

    Inputs:
        df: Pandas dataframe
        cat_cols: list of column names to generate indicator columns for
        drop: a bool. If true, drop the original category columns

    Return: The modified dataframe
    '''

    for col in cat_cols:
        binary_cols = pd.get_dummies(df[col], col)
        df = pd.merge(df, binary_cols, left_index=True, right_index=True, how='inner')

    if drop:
        df.drop(cat_cols, inplace=True, axis=1)

    return df


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


def prep_df_for_joining(df, cols_to_keep, new_col_names):
    '''
    Prep df for joining by selecting columns of interest,
    then assign new names to what is left.

    Input:
        df: DataFrame
        cols_to_keep: (list) of columns to join onto other dataframe.
        new_col_names: (list) of new column names, snake case recommended.

    Return: The modified df
    '''
    df_new = df[cols_to_keep]
    df_new.columns = new_col_names
    return df_new


def merge_df(df1, df2, df1_col, df2_col):
    '''
    Merge two DataFrames by

    Input:
        df1: DataFrame (left)
        df2: DataFrame (right)
        left_key =

    Return: The merged df.
    '''
    return df1.merge(df2, left_on=df1_col, right_on=df2_col)

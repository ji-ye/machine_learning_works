'''
Pipeline 2 of 6: Data Exploration

The major changes for Data Exploration section are:
1. Improved style with function abstraction.
2. Added function to plot the distribution of variables.
3. Added function to plot the correlation matrix heatmap of variables.

- JY
'''
import re
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Note: In the future, write function that use clustering to find outliers,
# and function that creates cross-tabs.
def camel_to_snake(column_name):
    """
    converts a string that is camelCase into snake_case
    Example:
        print camel_to_snake("javaLovesCamelCase")
        > java_loves_camel_case
    See Also:
        http://stackoverflow.com/questions/1175208/elegant-python-function-to-convert-camelcase-to-camel-case
    """
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', column_name)
    s1 = s1.replace(" ", "_")
    s1 = s1.replace("__", "_")
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()


def find_missing_value(df):
    '''
    Find missing value and show it in cross-tabs.
    '''
    df_lng = pd.melt(df)
    null_variables = df_lng.value.isnull()
    print(null_variables.sum())
    print(pd.crosstab(df_lng.variable, null_variables, rownames=['variable'],
    colnames=['missing value']))


# Note to self: After learning about clustering, complete the find_outlier
# function and integrate into explore_data.
def find_outlier(column):
    '''
    Find outliers by looking at distribution of values.
    '''
    pass


def plot_dist(df, colormap=sns.set_palette("PuBuGn_d"), outlier=True):
    '''
    Plot the distribution of each column with and without outliers.

    Input:
        df: DataFrame
        colormap: seaborn colormap
    '''
    COL_NUM = len(df.columns)
    fig = plt.figure(figsize=(12, 20))

    if outlier:
        # Note to self: range starts at 1 to skip person_id.
        for i in range(1, COL_NUM):
            plt.subplot(COL_NUM, 1, i)
            df[df.columns[i]].plot.box(subplots=True, vert=False,
             figsize=(12,1), widths=.75, fontsize=14, colormap=colormap)
        plt.suptitle("Original distribution with outliers", fontsize=30, y=0.94)
        plt.show()
    else:
        fig = plt.figure(figsize=(12, 20))
        for i in range(1,COL_NUM):
            plt.subplot(COL_NUM, 1, i)
            df[df.columns[i]].plot.box(subplots=True, vert=False, figsize=(12,1),
            widths=.75, fontsize=14, showfliers=False, colormap=colormap)
        plt.suptitle("Distribution without outliers", fontsize=30, y=0.94)
        plt.show()


# Note: In future, change the plot to show numbers on the grid.
def plot_corr(df):
    '''
    Plots a correlation heatmap for each pair of columns in the dataframe.

    Input:
        df: pandas DataFrame
    '''
    corr = df.corr()
    sns.heatmap(corr,
                xticklabels=corr.columns.values,
                yticklabels=corr.columns.values,
                square=True)


def explore_data(df):
    '''
    General explore data function that snake case column names, find missing
    values, and plot correlations, by combining the functions above.

    Input:
        filepath: (str) Raw data file path
        df: DataFrame

    Return: None
    '''
    df.columns = [camel_to_snake(col) for col in df.columns]
    print()
    find_missing_value(df)
    print()
    plot_corr(df)
    print()
    plot_dist(df, outlier=True)
    plot_dist(df, outlier=False)

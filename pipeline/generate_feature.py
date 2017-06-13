import pylab as pl
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn import metrics
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.feature_selection import *
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import RobustScaler, StandardScaler, MinMaxScaler
from sklearn.feature_selection import SelectFromModel


def categorize(df, col_dir):
    '''
    Convert string categorical value to intger categorical values

    Input:
        df: old dataframe
        col_dir: a dictionary to map string variable to integer
        sample col_dir for gender and occupation:
            gender_map = {'MALE':1, 'FEMALE':0}
            occup_map = {'YES':1, 'NO':0}
            col_dir = {'gender':gender_map, 'occup':occup_map}

    Return: new_df
    '''
    for col in col_dir.keys():
        df[col].replace(col_dir[col], inplace=True)
    return df


def discretize_continuous_var(col_name, bins, group_names):
    '''
    Discretize continuous variables.

    Input:
        col_name: DataFrame column name for the continuous variable.
        bins: (int) number of bins
        group_names: (list) of string of the discretize names.

    Return: None
    '''
    new_var_name = col_name + '_group'
    df[new_var_name] = pd.cut(df[col_name], bins, labels=group_names)



def create_binary_from_continuous(df, col, threshold, new_col_name):
    '''
    Create binary dummy variables from continuous variables using given threshold.

    Input:
        df: DataFrame
        col: (str) column whose value are used to compared to the threshold.
        threshold: (float) lower bound threshold for the binary dummy.
        new_col_name: (str) column name for the created dummy variable.

    Return: None
    '''
    df[new_col_name] = df[col] >= threshold
    df[new_col_name] = df[new_col_name].astype(int)


def create_interaction_dummy(df, col1, col2, new_col_name):
    '''
    Create interaction dummies between two columns

    Input:
        df: DataFrame
        col1: (str) first column to multiply.
        col2: (str) second column to multiply.
        new_col_name: (str) column name for the created dummy variable.

    Return: None
    '''
    df[new_col_name] = df[col1] * df[col2]


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


def select_feature_classification(X, y, plot=True):
    '''
    Select feature for classification labels.

    Input:
        X_train: features array.
        y_train: label array, element needs to be int or string.

    Return: (list) of features/colummns
    '''
    forest = ExtraTreesClassifier(n_estimators=250)#, random_state=0)
    forest.fit(X, y)
    importances = forest.feature_importances_
    std = np.std([tree.feature_importances_ for tree in forest.estimators_],
                 axis=0)
    indices = np.argsort(importances)[::-1]
    model = SelectFromModel(forest, prefit=True)
    feature_num = model.transform(X).shape[1]
    all_feature = list(X.columns[indices].values)
    top_feature = list(all_feature)[:feature_num]

    print("Feature ranking:")

    for f in range(X.shape[1]):
        print("%d. feature %d (%f)" % (f + 1, indices[f], importances[indices[f]]))

    if plot:
        plt.figure()
        plt.title("Feature importances", fontsize=25)
        plt.bar(range(X.shape[1]), importances[indices], color="0.8",
         yerr=std[indices], align="center")
        plt.xticks(range(X.shape[1]), all_feature, rotation='vertical')
        plt.xlim([-1, X.shape[1]])
        plt.grid(False)
        plt.savefig('feature_importances.png')
        # plt.show()

    return (all_feature, top_feature)


def select_feature_regressor(X_train, y_train):
    '''
    Select feature for float label using RandomForestRegressor.
    (For this project, this means we are selecting feature for
    predicting total waste weight instead of predicting whether
    a toilet is full or not.
    In other words, not useful right now.)

    Input:
        X_train: features array.
        y_train: label array, needs to be float label.

    Return: (list) of features/colummns
    '''
    forest = RandomForestRegressor(n_estimators=100)
    forest.fit(X_train, y_train)
    importances = forest.feature_importances_
    std = np.std([tree.feature_importances_ for tree in forest.estimators_],
                 axis=0)
    indices = np.argsort(importances)[::-1]
    print("Feature ranking:")

    for f in range(X.shape[1]):
        print("%d. feature %d (%f)" % (f + 1, indices[f], importances[indices[f]]))

    plt.figure()
    plt.title("Feature importances")
    plt.bar(range(X.shape[1]), importances[indices], color="0.8",
     yerr=std[indices], align="center")
    plt.xticks(range(X.shape[1]), indices)
    plt.xlim([-1, X.shape[1]])
    plt.grid(False)
    plt.show()

    feature = X[indices].columns.values
    return list(feature)

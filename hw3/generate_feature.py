'''
Pipeline 4 of 6: Generate Features/Predictors

There is no major change made to this section. But I added some functions for
creating dummy variables that might be useful for my program evaluation work.

Note: It is not too useful for now, but n future perhaps write function for
test-train split and scaling.

- JY
'''
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn import metrics
from sklearn.ensemble import ExtraTreesClassifier


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


def create_binary_from_cat(df, col):
    '''
    Create binary dummy variables from categorical variables.

    Input:
        df: DataFrame
        col: (str) a column in df.

    Return: None
    '''
    return pd.get_dummies(col)


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


def select_feature(X, y):
    '''
    Select feature based on ExtraTreeClassifier.

    Input:
        X_train: DataFrame
        y_train: DataFrame

    Return:
        feature: (list) of features/colummns
    '''
    forest = ExtraTreesClassifier(n_estimators=250)#, random_state=0)
    forest.fit(X, y)
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
    plt.show()

    feature = X[indices].columns.values
    return list(feature)

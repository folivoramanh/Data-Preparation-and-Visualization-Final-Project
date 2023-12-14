'''
This file contains functions to print percentile values for given column and
    calculate percentage of defaulters per category in a column

Functions:
    1. print_percentiles: function
        Function to print percentile values for given column
    2. defaulter_percentage_count_per_cat: function
        Function to calculate percentage of defaulters per category in a column
'''
import numpy as np
import pandas as pd


def print_percentiles(data, column_name, percentiles=None):
    '''
    Function to print percentile values for given column

    Inputs:
        data: DataFrame
            The DataFrame from which to print percentiles
        column_name: str
            Column's name whose percentiles are to be printed
        percentiles: list, default = None
            The list of percentiles to print, if not given, default are printed
    '''

    print('-'*90)
    if not percentiles:
        percentiles = list(range(0, 80, 25)) + list(range(90, 101, 2))
    for i in percentiles:
        print(
            f'The {i}th percentile value of {column_name} is {np.percentile(data[column_name].dropna(), i)}')
    print("-"*90)


def defaulter_percentage_count_per_cat(df, col):
    '''
    Function to calculate percentage of defaulters per category in a column

    Inputs:
        df: DataFrame
            The DataFrame from which to calculate percentage
        col: str
            Column's name whose percentage of defaulters are to be calculated

    Returns:
        DataFrame of percentage of defaulters per category in a column
    '''
    summary = []
    for cat in df[col].unique():
        default_count = df[(df[col] == cat) & (df.TARGET == 1)].shape[0]
        total_count = df[df[col] == cat].shape[0]
        if total_count == 0:
            pass
        else:
            summary.append([cat, default_count * 100 / total_count])

    report_df = pd.DataFrame(summary)
    report_df.columns = ["Categories", "Percentage_Of_Default"]
    return report_df.sort_values(by='Percentage_Of_Default', ascending=False)

'''
This file contains functions to check for missing values in a dataframe 
    and plot the percentage of missing values for each column.

Functions:
    1. nan_percent: function
        Function to create a dataframe of percentage of NaN values for each column of the dataframe
    2. plot_nan_percent: function
        Function to plot Bar Plots of NaN percentages for each Column with missing values
'''


import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def nan_percent(data):
    '''
    Function to create a dataframe of percentage of NaN values for each column of the dataframe

    Inputs:
        data:
            DataFrame

    Returns:
        DataFrame of NaN percentages
    '''

    nan_percentages = data.isnull().sum() * 100 / len(data)
    df_nan = pd.DataFrame(
        {'Column': nan_percentages.index,
         'Percentage_of_NaN': nan_percentages.values})

    # sorting the dataframe by decreasing order of percentage of NaN values
    df_nan.sort_values(by='Percentage_of_NaN', ascending=False, inplace=True)

    return df_nan


def plot_nan_percent(df_nan, title_name, tight_layout=True, figsize=(20, 10), grid=False, rotation=90):
    '''
    Function to plot Bar Plots of NaN percentages for each Column with missing values

    Inputs:
        df_nan:
            DataFrame of NaN percentages
        title_name:
            Name of table to be displayed in title of plot
        tight_layout: bool, default = True
            Whether to keep tight layout or not
        figsize: tuple, default = (20,8)
            Figure size of plot
        grid: bool, default = False
            Whether to draw gridlines to plot or not
        rotation: int, default = 0
            Degree of rotation for x-tick labels

    '''

    # checking if there is any column with NaNs or not.
    if df_nan.Percentage_of_NaN.sum() != 0:
        print(
            f"Number of columns having NaN values: {df_nan[df_nan['Percentage_of_NaN'] != 0].shape[0]} columns")

        # plotting the Bar-Plot for NaN percentages (only for columns with Non-Zero percentage of NaN values)
        plt.figure(figsize=figsize, tight_layout=tight_layout)
        sns.barplot(x='Column', y='Percentage_of_NaN',
                    data=df_nan[df_nan['Percentage_of_NaN'] > 0], palette='Blues_r')
        plt.xticks(rotation=rotation)
        plt.xlabel(title_name, fontsize=13)
        plt.ylabel('Percentage', fontsize=13)
        plt.title(
            f'Percentage of NaN values in {title_name}', fontsize=22, weight='bold', pad=30)
        if grid:
            plt.grid()

        plt.tight_layout()
        plt.show()
    else:
        print(f"The dataframe {title_name} does not contain any NaN values.")

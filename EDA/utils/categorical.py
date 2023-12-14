'''
This file contains functions to perform EDA on categorical variables

Functions:
    get_category_column: Function to create a dataframe of category columns
    plot_category_column: Function to plot category columns
    plot_categorical_variables_bar: Function to plot Categorical Variables Bar Plots
    plot_categorical_variables_pie: Function to plot categorical variables Pie Plots
    categories_pie_plot: Function to plot pie chart for categorical variables
    print_unique_categories: Function to print unique categories
'''

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from plotly.subplots import make_subplots
import plotly.graph_objects as go

# pandas DataFrame column and row display limits
pd.set_option("display.max_columns", 100)
pd.set_option("display.max_rows", 100)


def get_category_column(data):
    '''
    Function to create a dataframe of category columns

    Inputs:
        data:
            DataFrame

    Returns:
        DataFrame of category columns
    '''

    # Select category columns
    category_columns = data.select_dtypes(include='object').columns

    # Create a DataFrame to store information
    column_info = pd.DataFrame(
        columns=['Feature', 'Nunique', 'Percentage of NaN'])

    # Loop through each category column
    for column in category_columns:
        # Count unique values
        nunique = data[column].nunique()

        # Calculate percentage of NaN values
        percentage_nan = (data[column].isnull().sum() / len(data)) * 100

        # Append information to the DataFrame
        column_info = pd.concat([column_info, pd.DataFrame(
            {'Feature': column,
             'Nunique': nunique,
             'Percentage of NaN': percentage_nan},
            index=[0])],
            ignore_index=True)

    return column_info


def plot_category_column(data, name):
    '''
    Function to plot category columns

    Inputs:
        data:
            DataFrame
        name:
            Name of the dataset
    '''

    plt.figure(figsize=(12, 8))
    data = data.sort_values(by='Nunique', ascending=False)
    sns.barplot(x='Nunique', y='Feature', data=data, palette='Blues_r')
    plt.title(
        f'Number of unique values of category columns in {name}',
        fontsize=22, weight='bold', pad=30)
    plt.xlabel('Number of unique values')
    plt.ylabel('Category columns')

    plt.tight_layout()
    plt.show()


def plot_categorical_variables_bar(data, column_name, figsize=(18, 6),
                                   percentage_display=True, plot_defaulter=True,
                                   rotation=0, horizontal_adjust=0, fontsize_percent='xx-small'):
    '''
    Function to plot Categorical Variables Bar Plots

    Inputs:
        data: DataFrame
            The DataFrame from which to plot
        column_name: str
            Column's name whose distribution is to be plotted
        figsize: tuple, default = (18,6)
            Size of the figure to be plotted
        percentage_display: bool, default = True
            Whether to display the percentages on top of Bars in Bar-Plot
        plot_defaulter: bool
            Whether to plot the Bar Plots for Defaulters or not
        rotation: int, default = 0
            Degree of rotation for x-tick labels
        horizontal_adjust: int, default = 0
            Horizontal adjustment parameter for percentages displayed on the top of Bars of Bar-Plot
        fontsize_percent: str, default = 'xx-small'
            Fontsize for percentage Display

    '''

    print(
        f"Total Number of unique categories of {column_name} = {len(data[column_name].unique())}")

    plt.figure(figsize=figsize, tight_layout=False)
    sns.set(style='whitegrid', font_scale=1.2)

    # plotting overall distribution of category
    plt.subplot(1, 2, 1)
    data_to_plot = data[column_name].value_counts(
    ).sort_values(ascending=False)
    ax = sns.barplot(x=data_to_plot.index, y=data_to_plot, palette='Blues_r')

    if percentage_display:
        total_datapoints = len(data[column_name].dropna())
        for p in ax.patches:
            ax.text(p.get_x() + horizontal_adjust, p.get_height() + 0.005 * total_datapoints,
                    '{:1.02f}%'.format(p.get_height() * 100 / total_datapoints), fontsize=fontsize_percent)

    plt.xlabel(column_name, labelpad=10)
    plt.title(f'Distribution of {column_name}', size=24, weight='bold', pad=25)
    plt.xticks(rotation=rotation)
    plt.ylabel('Counts')

    # plotting distribution of category for Defaulters
    if plot_defaulter:
        percentage_defaulter_per_category = (data[column_name][data.TARGET == 1].value_counts(
        ) * 100 / data[column_name].value_counts()).dropna().sort_values(ascending=False)

        plt.subplot(1, 2, 2)
        sns.barplot(x=percentage_defaulter_per_category.index,
                    y=percentage_defaulter_per_category, palette='Blues_r')
        plt.ylabel('Percentage of Defaulter per category')
        plt.xlabel(column_name, labelpad=10)
        plt.xticks(rotation=rotation)
        plt.title(
            f'Percentage of Defaulters for each category of {column_name}',
            size=22, weight='bold', pad=25)
    plt.tight_layout()
    plt.show()


def plot_categorical_variables_pie(data, column_name, plot_defaulter=True, hole=0):
    '''
    Function to plot categorical variables Pie Plots

    Inputs:
        data: DataFrame
            The DataFrame from which to plot
        column_name: str
            Column's name whose distribution is to be plotted
        plot_defaulter: bool
            Whether to plot the Pie Plot for Defaulters or not
        hole: int, default = 0
            Radius of hole to be cut out from Pie Chart
    '''

    if plot_defaulter:
        cols = 2
        specs = [[{'type': 'domain'}, {'type': 'domain'}]]
        titles = [f'Distribution of {column_name} for all Targets',
                  f'Percentage of Defaulters for each category of {column_name}']
    else:
        cols = 1
        specs = [[{'type': 'domain'}]]
        titles = [f'Distribution of {column_name} for all Targets']

    values_categorical = data[column_name].value_counts()
    labels_categorical = values_categorical.index

    fig = make_subplots(rows=1, cols=cols,
                        specs=specs,
                        subplot_titles=titles)

    fig.add_trace(go.Pie(values=values_categorical, labels=labels_categorical, hole=hole,
                         textinfo='label+percent', textposition='inside'), row=1, col=1)

    if plot_defaulter:
        percentage_defaulter_per_category = data[column_name][data.TARGET == 1].value_counts(
        ) * 100 / data[column_name].value_counts()
        percentage_defaulter_per_category.dropna(inplace=True)
        percentage_defaulter_per_category = percentage_defaulter_per_category.round(
            2)

        fig.add_trace(go.Pie(values=percentage_defaulter_per_category,
                             labels=percentage_defaulter_per_category.index,
                             hole=hole, textinfo='label+value', hoverinfo='label+value'),
                      row=1, col=2)

    fig.update_layout(
        title=f'Distribution of {column_name}', size=22, weight='bold', pad=25, palette='Blues_r')

    fig.tight_layout()
    plt.tight_layout()
    plt.show()


def categories_pie_plot(data, x):
    '''
    Function to plot pie chart for categorical variables

    Inputs:
        data: DataFrame
            The DataFrame from which to plot
        x: str
            Column's name whose distribution is to be plotted
    '''
    fig, ax = plt.subplots(1, 2, figsize=(12, 6))

    x1 = data[data["TARGET"] == 0][x].value_counts(
        normalize=True).sort_values(ascending=False)
    ax[0].pie(x1, labels=x1.index, autopct='%1.1f%%')
    ax[0].title.set_text("Non-defaulter")

    x2 = data[data["TARGET"] == 1][x].value_counts(
        normalize=True).sort_values(ascending=False)
    ax[1].pie(x2, labels=x2.index, autopct='%1.1f%%')
    ax[1].title.set_text("Defaulter")

    ax[1].legend(loc='upper right', bbox_to_anchor=(1.5, 1), title=x)

    for i in range(2):
        for text in ax[i].texts[::2]:
            text.set_visible(False)

    fig.suptitle(f"Distribution of {x}\nwith TARGET", fontsize=20)

    fig.tight_layout()
    plt.tight_layout()
    plt.show()


def print_unique_categories(data, column_name, show_counts=False):
    '''
    Function to print unique categories
    Inputs:
        data: DataFrame
            The DataFrame from which to print.
        column_name: str
            Column's name whose nique_categories tp printed.
        show_counts = False
            Display all counts in a rectangular format
    '''

    print('-'*100)
    print(
        f"The unique categories of '{column_name}' are:\n{data[column_name].unique()}")
    print('-'*100)

    if show_counts:
        print(
            f"Counts of each category are:\n{data[column_name].value_counts()}")
        print('-'*100)

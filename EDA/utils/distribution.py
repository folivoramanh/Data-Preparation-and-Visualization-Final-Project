'''
This file contains functions to plot distribution of a variable

Functions:
    plot_cdf: Function to plot CDF of a continuour variable
    draw_distribution: Function to draw distribution of a variable
    plot_distribution: Function to plot distribution of a variable related to target variable
    plot_stats: Function to plot distribution of a variable
'''
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
warnings.simplefilter(action='ignore', category=UserWarning)


def plot_cdf(data, column_name, log_scale=False, figsize=(12, 8)):
    '''
    Function to plot CDF of a continuour variable

    Inputs:
        data: DataFrame
            The DataFrame from which to plot
        column_name: str
            Column's name whose CDF is to be plotted
        log_scale: bool, default = True
            Whether to use log-scale (for widely varying values) or not
        figsize: tuple, default = (12,8)
            The size of figure to be plotted
    '''

    percentile_values = data[[column_name]
                             ].dropna().sort_values(by=column_name)
    percentile_values['Percentile'] = [
        ele / (len(percentile_values) - 1) for ele in range(len(percentile_values))]

    plt.figure(figsize=figsize)
    if log_scale:
        plt.xscale('log')
        plt.xlabel(column_name + ' - (log-scale)')
    else:
        plt.xlabel(column_name)
    plt.plot(percentile_values[column_name],
             percentile_values['Percentile'], color='red')
    plt.ylabel('Probability')
    plt.title(f'CDF of {column_name}')

    plt.tight_layout()
    plt.show()


def draw_distribution(x, title):
    '''
    Function to draw distribution of a variable

    Inputs:
        x: Series
            The Series whose distribution is to be drawn
        title: str
            The title of the plot
        c: str
            The color of the plot
    '''
    fig, ax = plt.subplots(2, 1, figsize=(20, 10))

    sns.distplot(x, ax=ax[0])
    ax[0].set(xlabel=None)
    ax[0].set_title('Histogram + KDE')

    sns.boxplot(x, ax=ax[1])
    ax[1].set(xlabel=None)
    ax[1].set_title('Boxplot')

    fig.suptitle(title, fontsize=20)

    plt.tight_layout()
    plt.show()


def plot_distribution(data, column_name, column_name2=None,
                      plot_type='dist', nrows=1, ncols=2,
                      figsize=(12, 6), dropna=False,
                      sort_values=False, bins='auto', palette='Blues_r'):
    '''
    Function to plot distribution of a variable related to target variable

    Inputs:
        data: DataFrame
            The DataFrame from which to plot
        column_name: str
            Column's name whose distribution is to be plotted
        column_name2: str, default = None
            Column's name whose distribution is to be plotted, used only for scatter plot
        plot_type: str, default = 'dist'
            The type of plot to be plotted, supported types are:
                1. dist: Distribution plot
                2. hist: Histogram plot
                3. count: Count plot
                4. box: Box plot
                5. scatter: Scatter plot
        nrows: int, default = 1
            The number of rows in the figure
        ncols: int, default = 2
            The number of columns in the figure
        figsize: tuple, default = (12,6)
            The size of figure to be plotted
        dropna: bool, default = False   
            Whether to drop NaN values or not
        sort_values: bool, default = False
            Whether to sort values or not
        bins: int, default = 'auto' 
            The number of bins to be used
        palette: str, default = 'Blues_r'
            The color palette to be used
    '''
    fig, ax = plt.subplots(nrows, ncols, figsize=figsize)
    if plot_type == 'dist':
        if dropna:
            sns.distplot(data[data["TARGET"] == 0][column_name].dropna(),
                         ax=ax[0], bins=bins).set(title="Non-defaulter")
            sns.distplot(data[data["TARGET"] == 1][column_name].dropna(),
                         ax=ax[1], bins=bins).set(title="Defaulter")
        elif sort_values:
            sns.distplot(x = data[data["TARGET"] == 0][column_name].sort_values(),
                         ax=ax[0], bins=bins).set(title="Non-defaulter")
            sns.distplot(x = data[data["TARGET"] == 1][column_name].sort_values(),
                         ax=ax[1], bins=bins).set(title="Defaulter")
        else:
            sns.distplot(data[data["TARGET"] == 0][column_name],
                         ax=ax[0], bins=bins).set(title="Non-defaulter")
            sns.distplot(data[data["TARGET"] == 1][column_name],
                         ax=ax[1], bins=bins).set(title="Defaulter")
        ax[0].set_xticklabels(ax[0].get_xticklabels(), rotation=45)
        ax[1].set_xticklabels(ax[1].get_xticklabels(), rotation=45)

    elif plot_type == 'hist':
        if dropna:
            sns.histplot(data[data["TARGET"] == 0][column_name].dropna(),
                         ax=ax[0], bins=bins).set(title="Non-defaulter")
            sns.histplot(data[data["TARGET"] == 1][column_name].dropna(),
                         ax=ax[1], bins=bins).set(title="Defaulter")
        elif sort_values:
            sns.histplot(data[data["TARGET"] == 0][column_name].sort_values(),
                         ax=ax[0], bins=bins).set(title="Non-defaulter")
            sns.histplot(data[data["TARGET"] == 1][column_name].sort_values(),
                         ax=ax[1], bins=bins).set(title="Defaulter")
        else:
            sns.histplot(data[data["TARGET"] == 0][column_name],
                         ax=ax[0], bins=bins).set(title="Non-defaulter")
            sns.histplot(data[data["TARGET"] == 1][column_name],
                         ax=ax[1], bins=bins).set(title="Defaulter")

    elif plot_type == 'count':
        if dropna:
            sns.countplot(x=data[data["TARGET"] == 0][column_name].dropna(),
                          ax=ax[0], palette=palette).set(title="Non-defaulter")
            sns.countplot(x=data[data["TARGET"] == 1][column_name].dropna(),
                          ax=ax[1], palette=palette).set(title="Defaulter")

        elif sort_values:
            sns.countplot(x=data[data["TARGET"] == 0][column_name].sort_values(),
                          ax=ax[0], palette=palette).set(title="Non-defaulter")
            sns.countplot(x=data[data["TARGET"] == 1][column_name].sort_values(),
                          ax=ax[1], palette=palette).set(title="Defaulter")
        else:
            sns.countplot(x=data[data["TARGET"] == 0][column_name],
                          ax=ax[0], palette=palette).set(title="Non-defaulter")
            sns.countplot(x=data[data["TARGET"] == 1][column_name],
                          ax=ax[1], palette=palette).set(title="Defaulter")
        ax[0].set_xticklabels(ax[0].get_xticklabels(), rotation=45)
        ax[1].set_xticklabels(ax[1].get_xticklabels(), rotation=45)

    elif plot_type == 'box':
        sns.boxplot(data[data["TARGET"] == 0][column_name],
                    ax=ax[0], orient='h').set(title="Non-defaulter")
        sns.boxplot(data[data["TARGET"] == 1][column_name],
                    ax=ax[1], orient='h').set(title="Defaulter")

    elif plot_type == 'scatter' and column_name2 is not None:
        sns.scatterplot(x=data[data["TARGET"] == 0][column_name],
                        y=data[data["TARGET"] == 0][column_name2],
                        ax=ax[0]).set(title="Non-defaulter")
        sns.scatterplot(x=data[data["TARGET"] == 1][column_name],
                        y=data[data["TARGET"] == 1][column_name2],
                        ax=ax[1], color="orange").set(title="Defaulter")

    fig.tight_layout()
    plt.tight_layout()
    plt.show()


def plot_stats(df, feature, label_rotation=False, horizontal_layout=True):
    '''
    Function to plot distribution of a variable related to target variable

    Inputs:
        df: DataFrame
            The DataFrame from which to plot
        feature: str
            Column's name whose distribution is to be plotted
        label_rotation: bool, default = False
            Whether to rotate the labels or not
        horizontal_layout: bool, default = True
            Whether to plot horizontally or not
    '''
    temp = df[feature].value_counts()
    df1 = pd.DataFrame(
        {feature: temp.index, 'Number of contracts': temp.values})

    # Calculate the percentage of target=1 per category value
    cat_perc = df[[feature, 'TARGET']].groupby(
        [feature], as_index=False).mean()
    cat_perc.sort_values(by='TARGET', ascending=False, inplace=True)

    if (horizontal_layout):
        fig, (ax1, ax2) = plt.subplots(ncols=2, figsize=(12, 6))
    else:
        fig, (ax1, ax2) = plt.subplots(nrows=2, figsize=(12, 14))
    s = sns.barplot(ax=ax1, x=feature, y="Number of contracts",
                    data=df1, palette='Blues_d', order=df1[feature])
    if (label_rotation):
        s.set_xticklabels(s.get_xticklabels(), rotation=90)

    s = sns.barplot(ax=ax2, x=feature, y='TARGET',
                    order=df1[feature], data=cat_perc, palette='Blues_d')
    if (label_rotation):
        s.set_xticklabels(s.get_xticklabels(), rotation=90)

    vals = ax2.get_yticks()
    ax2.set_yticklabels(['{:,.00%}'.format(x) for x in vals])

    plt.ylabel('Percent of contracts', fontsize=10)
    plt.tick_params(axis='both', which='major', labelsize=10)

    fig.tight_layout()
    plt.tight_layout()
    plt.show()

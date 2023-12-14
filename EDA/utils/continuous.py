'''
This file contains the functions to plot continuous variables distribution.

Functions:
    plot_continuous_variables: Function to plot continuous variables distribution
'''

import matplotlib.pyplot as plt
import seaborn as sns


def plot_continuous_variables(data, column_name, plots=['distplot', 'CDF', 'box', 'violin'],
                              scale_limits=None, figsize=(20, 8), hist=False, log_scale=False):
    '''
    Function to plot continuous variables distribution

    Inputs:
        data: DataFrame
            The DataFrame from which to plot.
        column_name: str
            Column's name whose distribution is to be plotted.
        plots: list, default = ['distplot', 'CDF', box', 'violin']
            List of plots to plot for Continuous Variable.
        scale_limits: tuple (left, right), default = None
            To control the limits of values to be plotted in case of outliers.
        figsize: tuple, default = (20,8)
            Size of the figure to be plotted.
        hist: bool, default = False
            Whether to plot histogram along with distplot or not.
        log_scale: bool, default = False
            Whether to use log-scale for variables with outlying points.
    '''

    data_to_plot = data.copy()
    if scale_limits:
        # taking only the data within the specified limits
        data_to_plot[column_name] = data[column_name][(
            data[column_name] > scale_limits[0]) & (data[column_name] < scale_limits[1])]

    number_of_subplots = len(plots)
    plt.figure(figsize=figsize)
    # sns.set_style('whitegrid')

    for i, ele in enumerate(plots):
        plt.subplot(1, number_of_subplots, i + 1)
        plt.subplots_adjust(wspace=0.25)

        if ele == 'CDF':
            # making the percentile DataFrame for both positive and negative Class Labels
            percentile_values_0 = data_to_plot[data_to_plot.TARGET == 0][[
                column_name]].dropna().sort_values(by=column_name)
            percentile_values_0['Percentile'] = [
                ele / (len(percentile_values_0)-1) for ele in range(len(percentile_values_0))]

            percentile_values_1 = data_to_plot[data_to_plot.TARGET == 1][[
                column_name]].dropna().sort_values(by=column_name)
            percentile_values_1['Percentile'] = [
                ele / (len(percentile_values_1)-1) for ele in range(len(percentile_values_1))]

            plt.plot(percentile_values_0[column_name],
                     percentile_values_0['Percentile'], color='red', label='Non-Defaulters')
            plt.plot(percentile_values_1[column_name],
                     percentile_values_1['Percentile'], color='black', label='Defaulters')
            plt.xlabel(column_name)
            plt.ylabel('Probability')
            plt.title(f'CDF of {column_name}',
                      size=25, weight='bold', pad=28)
            plt.legend(fontsize='medium')
            if log_scale:
                plt.xscale('log')
                plt.xlabel(column_name + ' - (log-scale)')

        if ele == 'distplot':
            sns.distplot(data_to_plot[column_name][data['TARGET'] == 0].dropna(),
                         label='Non-Defaulters', hist=hist, color='red')
            sns.distplot(data_to_plot[column_name][data['TARGET'] == 1].dropna(),
                         label='Defaulters', hist=hist, color='black')
            plt.xlabel(column_name)
            plt.ylabel('Probability Density')
            plt.legend(fontsize='medium')
            plt.title(f"Dist-Plot of {column_name}",
                      size=25, weight='bold', pad=28)
            if log_scale:
                plt.xscale('log')
                plt.xlabel(f'{column_name} (Log Scale)')

        if ele == 'violin':
            sns.violinplot(x='TARGET', y=column_name, data=data_to_plot)
            plt.title(f"Violin-Plot of {column_name}",
                      size=25, weight='bold', pad=28)
            if log_scale:
                plt.yscale('log')
                plt.ylabel(f'{column_name} (Log Scale)')

        if ele == 'box':
            sns.boxplot(x='TARGET', y=column_name, data=data_to_plot)
            plt.title(f"Box-Plot of {column_name}",
                      size=25, weight='bold', pad=28)
            if log_scale:
                plt.yscale('log')
                plt.ylabel(f'{column_name} (Log Scale)')

    plt.tight_layout()
    plt.show()

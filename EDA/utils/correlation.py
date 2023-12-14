'''
This file contains the functions to plot the correlation matrix and PhiK matrix.

Functions:
    1. correlation_matrix: Class
        Contains three methods:
            1. init method
            2. plot_correlation_matrix method:
                Function to plot the Correlation Matrix Heatmap
            3. target_top_corr method:
                Function to return the Top Correlated features with the Target
    2. numeric_cor: function
        Function to plot the correlation of numerical features
    3. plot_phik_matrix: function
        Function to Phi_k matrix for categorical features
'''
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from IPython.display import display
import phik


class correlation_matrix:
    '''
    Class to plot heatmap of Correlation Matrix and print Top Correlated Features with Target.
    Contains three methods:
        1. init method
        2. plot_correlation_matrix method
        3. target_top_corr method
    '''

    def __init__(self, data, columns_to_drop, figsize=(25, 23), mask_upper=True, tight_layout=True,
                 linewidth=0.5, fontsize=10, cmap='Blues'):
        '''
        Function to initialize the class members.

        Inputs:
            data: DataFrame
                The DataFrame from which to build correlation matrix
            columns_to_drop: list
                Columns which have to be dropped while building the correlation matrix (for example the Loan ID)
            figsize: tuple, default = (25,23)
                Size of the figure to be plotted
            mask_upper: bool, default = True
                Whether to plot only the lower triangle of heatmap or plot full.
            tight_layout: bool, default = True
                Whether to keep tight layout or not
            linewidth: float/int, default = 0.1
                The linewidth to use for heatmap
            fontsize: int, default = 10
                The font size for the X and Y tick labels
            cmap: str, default = 'Blues'
                The colormap to be used for heatmap

        Returns:
            None
        '''

        self.data = data
        self.columns_to_drop = columns_to_drop
        self.figsize = figsize
        self.mask_upper = mask_upper
        self.tight_layout = tight_layout
        self.linewidth = linewidth
        self.fontsize = fontsize
        self.cmap = cmap
        self.corr_data = None

    def plot_correlation_matrix(self, round = 2):
        '''
        Function to plot the Correlation Matrix Heatmap

        Inputs:
            self

        Returns:
            None
        '''

        print('-' * 90)
        # building the correlation dataframe
        data = self.data.drop(self.columns_to_drop + ['TARGET'], axis=1)
        self.corr_data = data.corr(numeric_only=True)

        if self.mask_upper:
            # masking the heatmap to show only lower triangle. This is to save the RAM.
            mask_array = np.ones(self.corr_data.shape)
            mask_array = np.triu(mask_array)
        else:
            mask_array = np.zeros(self.corr_data.shape)

        plt.figure(figsize=self.figsize, tight_layout=self.tight_layout)
        annot = abs(self.corr_data.round(2)).astype(str)
        sns.heatmap(self.corr_data, annot=annot, fmt='', mask=mask_array,
                    linewidth=self.linewidth, cmap=self.cmap)
        plt.xticks(rotation=90, fontsize=self.fontsize)
        plt.yticks(fontsize=self.fontsize)
        plt.title("Correlation Heatmap for Numerical features",
                  size=23, weight='bold', pad=25)

        plt.tight_layout()
        plt.show()
        print("-"*90)

    def target_top_corr(self, target_top_columns=10):
        '''
        Function to return the Top Correlated features with the Target

        Inputs:
            self
            target_top_columns: int, default = 10
                The number of top correlated features with target to display

        Returns:
            Top correlated features DataFrame.
        '''

        phik_target_arr = np.zeros(self.corr_data.shape[1])
        # calculating the Phik-Correlation with Target
        for index, column in enumerate(self.corr_data.columns):
            phik_target_arr[index] = self.data[[
                'TARGET', column]].phik_matrix().iloc[0, 1]
        # getting the top correlated columns and their values
        top_corr_target_df = pd.DataFrame(
            {'Column Name': self.corr_data.columns, 'Phik-Correlation': phik_target_arr})
        top_corr_target_df = top_corr_target_df.sort_values(
            by='Phik-Correlation', ascending=False)

        if target_top_columns > top_corr_target_df.shape[0]:
            target_top_columns = top_corr_target_df.shape[0]

        return top_corr_target_df.iloc[:target_top_columns]


def numeric_cor(data, round = 2):
    '''
    Function to plot the correlation of numerical features

    Inputs:
        data: DataFrame
            The DataFrame from which to build correlation matrix
    '''

    numeric_df = data.select_dtypes(include='number')
    numeric_df_corr = numeric_df.corr()

    plt.figure(figsize=(10, 10))
    plt.title('Correlation of Numerical feature',
              fontsize=23, weight='bold', pad=30)
    mask = np.zeros_like(numeric_df_corr, dtype=bool)
    mask[np.triu_indices_from(mask)] = True
    mask[np.diag_indices_from(mask)] = False
    annot = abs(numeric_df_corr.round(2)).astype(str)
    sns.heatmap(numeric_df_corr, mask=mask, cmap='Blues',
                annot=annot, fmt="", linewidth=.5)

    plt.tight_layout()
    plt.show()


def plot_phik_matrix(data, categorical_columns, figsize=(20, 20), mask_upper=True, tight_layout=True,
                     linewidth=0.1, fontsize=10, cmap='Blues', show_target_top_corr=True, target_top_columns=10, round = 2):
    '''
    Function to Phi_k matrix for categorical features

    Inputs:
        data: DataFrame
            The DataFrame from which to build correlation matrix
        categorical_columns: list
            List of categorical columns whose PhiK values are to be plotted
        figsize: tuple, default = (25,23)
            Size of the figure to be plotted
        mask_upper: bool, default = True
            Whether to plot only the lower triangle of heatmap or plot full.
        tight_layout: bool, default = True
            Whether to keep tight layout or not
        linewidth: float/int, default = 0.1
            The linewidth to use for heatmap
        fontsize: int, default = 10
            The font size for the X and Y tick labels
        cmap: str, default = 'Blues'
            The colormap to be used for heatmap
        show_target_top_corr: bool, default = True
            Whether to show top/highly correlated features with Target.
        target_top_columns: int, default = 10
            The number of top correlated features with target to display
    '''

    # first fetching only the categorical features
    data_for_phik = data[categorical_columns].astype('object')
    phik_matrix = data_for_phik.phik_matrix()

    print('-'*100)

    if mask_upper:
        mask_array = np.ones(phik_matrix.shape)
        mask_array = np.triu(mask_array)
    else:
        mask_array = np.zeros(phik_matrix.shape)

    plt.figure(figsize=figsize, tight_layout=tight_layout)
    annot = abs(phik_matrix.round(2)).astype(str)
    sns.heatmap(phik_matrix, annot=annot,fmt=f"", mask=mask_array,
                linewidth=linewidth, cmap=cmap)
    plt.xticks(rotation=90, fontsize=fontsize)
    plt.yticks(rotation=0, fontsize=fontsize)
    plt.title("Phi-K Correlation Heatmap for Categorical Features",
              size=23, weight='bold', pad=25)

    plt.tight_layout()
    plt.show()
    print("-"*100)

    if show_target_top_corr:
        # Seeing columns have highest correlation with the target variable in application_train
        print("Categories with highest values of Phi-K Correlation value with Target Variable are:")
        phik_df = pd.DataFrame(
            {'Column Name': phik_matrix.TARGET.index[1:],
             'Phik-Correlation': phik_matrix.TARGET.values[1:]})
        phik_df = phik_df.sort_values(by='Phik-Correlation', ascending=False)
        display(phik_df.head(target_top_columns))
        print("-"*100)

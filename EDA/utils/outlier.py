''' Function to create a dataframe of outlier for each column 

Functions:
    1. outlier: function
        Function to filter a dataframe of outlier for each column
'''
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

# pandas DataFrame column and row display limits
pd.set_option("display.max_columns", 100)
pd.set_option("display.max_rows", 100)


def outlier(data):
    '''
    Function to filter a dataframe of outlier for each column from the dataset

    Inputs:
        data:
            DataFrame

    Returns:
        Print DataFrame of outlier for each column
    '''

    numerical_columns = data.select_dtypes(include='number').columns
    numerical_columns = [col for col in numerical_columns if "_ID_"not in col]

    # Create a box plot for each numerical column to identify outliers
    plt.figure(figsize=(5, 2))
    for column in numerical_columns:
        sns.boxplot(x=data[column])
        plt.title(f'Boxplot for {column}')
        plt.show()
    q1 = data[numerical_columns].quantile(0.25)
    q3 = data[numerical_columns].quantile(0.75)
    iqr = q3 - q1

    # Define a criterion for identifying outliers
    outlier_threshold = 1.5

    # Filter outliers based on the iqr criterion
    outliers = ((data[numerical_columns] < (q1 - outlier_threshold * iqr))
                | (data[numerical_columns] > (q3 + outlier_threshold * iqr)))

    # Display the rows with outliers
    data = data[numerical_columns]
    rows_with_outliers = data[outliers.any(axis=1)]
    print("Rows with outliers:")
    print(rows_with_outliers)

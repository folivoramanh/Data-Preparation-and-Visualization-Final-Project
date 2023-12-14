'''
This file contains functions to calculate imbalance ratio of a dataset

Functions:
    1. imbalance_col: function
        Function to create a dataframe of imbalance columns
'''


def imbalance_col(data):
    '''
    Function to create a dataframe of imbalance columns

    Inputs:
        data:
            DataFrame

    Returns:
        DataFrame of imbalance columns
    '''

    imbalance_ratios = {}
    column = [col for col in data.columns if '_ID_' not in col]
    data = data[column]
    
    for column in data.columns:
        if data[column].dtype == 'object':
            # If the column is categorical, calculate the imbalance ratio for each category
            value_counts = data[column].value_counts()
            imbalance_ratios[column] = value_counts.min(
            ) / value_counts.max() if len(value_counts) > 1 else None
        else:
            # If the column is numerical, calculate the imbalance ratio for 0 and 1 (or similar values)
            value_counts = data[column].value_counts()
            imbalance_ratios[column] = value_counts[1] / \
                value_counts[0] if 0 in value_counts.index and 1 in value_counts.index else None

    for column, ratio in imbalance_ratios.items():
        if ratio is not None:
            print(f"Imbalance Ratio for column '{column}': {ratio:.4f}")
        else:
            print(f"Imbalance Ratio for column '{column}': None")

    # Remove columns that cannot be calculated from the search process
    valid_imbalance_ratios = {k: v for k,
                              v in imbalance_ratios.items() if v is not None}
    print('-'*90)

    # Check if there is any column that cannot be calculated
    if not valid_imbalance_ratios:
        print("All columns do not have data to calculate the imbalance ratio.")
    else:
        # Find the column with the heaviest imbalance ratio
        max_imbalance_column = max(
            valid_imbalance_ratios, key=valid_imbalance_ratios.get)
        # Print the information of the column with the heaviest imbalance ratio
        max_imbalance_ratio = valid_imbalance_ratios[max_imbalance_column]
        print(
            f"The column with the heaviest imbalance ratio is '{max_imbalance_column}' with ratio {max_imbalance_ratio:.4f}")

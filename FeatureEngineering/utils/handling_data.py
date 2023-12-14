import numpy as np
import pandas as pd


def replace_infinite(df):
    # Check for infinite values
    mask_inf = df.isin([np.inf, -np.inf])
    if mask_inf.any().any():
        # Replace infinite values with np.nan
        df.replace([np.inf, -np.inf], np.nan, inplace=True)
        print("Infinite values replaced with np.nan.")
    else:
        print("No infinite values found.")
    return df


def drop_highNaN(df, percentage_remove=90):
    #     Split features (X) and Target (Y) for not having mistake in drop
    target = None
    if 'TARGET' in df.columns:
        target = df['TARGET']
        df = df.drop(columns=['TARGET'])
#     Calculate NaN in percentage of each feature in DataFrame
    nan_percentages = (df.isna().mean() * 100)

#     Select only columns with <= 90% NaN values
    filtered_columns = nan_percentages[nan_percentages <=
                                       percentage_remove].index

#     Create a new DataFrame with only the selected columns
    df = df[filtered_columns]

#     Merge TARGET columns back to DataFrame if exist
    if target is not None:
        df['TARGET'] = target
    return df


def drop_multicollinearity(df, correlation_threshold=0.9):
    target = None
    if 'TARGET' in df.columns:
        target = df['TARGET']
        df = df.drop(columns=['TARGET'])
    correlation_matrix = df.corr()

    # Find highly correlated features
    highly_correlated_features = set()
    for i in range(len(correlation_matrix.columns)):
        for j in range(i):
            if abs(correlation_matrix.iloc[i, j]) > correlation_threshold:
                colname = correlation_matrix.columns[i]
                highly_correlated_features.add(colname)
    # Drop highly correlated features
    df = df.drop(columns=highly_correlated_features)
    if target is not None:
        df['TARGET'] = target

    return df

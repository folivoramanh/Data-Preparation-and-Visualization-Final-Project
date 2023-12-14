import pandas as pd


def one_hot_encoder(df, categorical_columns=None, nan_as_category=True):
    """Create a new column for each categorical value in categorical columns using get dummies. """
    original_columns = list(df.columns)
    if not categorical_columns:
        categorical_columns = [
            col for col in df.columns if df[col].dtype == 'object']
    df = pd.get_dummies(df, columns=categorical_columns,
                        dummy_na=nan_as_category)
    categorical_columns = [c for c in df.columns if c not in original_columns]
    return df, categorical_columns


def label_encoder(df, categorical_columns=None):
    """Encode categorical values as integers (0,1,2,3...) with pandas.factorize. """
    if not categorical_columns:
        categorical_columns = [
            col for col in df.columns if df[col].dtype == 'object']
    for col in categorical_columns:
        df[col], uniques = pd.factorize(df[col])
    return df, categorical_columns


def get_age_label(days_birth):
    """ Return the age group label (int).  - a type of label encoder"""
    age_years = -days_birth / 365
    if age_years < 27:
        return 1
    elif age_years < 40:
        return 2
    elif age_years < 50:
        return 3
    elif age_years < 65:
        return 4
    elif age_years < 99:
        return 5
    else:
        return 0

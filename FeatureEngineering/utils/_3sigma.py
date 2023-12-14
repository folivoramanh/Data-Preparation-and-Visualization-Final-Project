import pandas as pd


def zoom_3sigma(col, dataset, dataset_apl, verbose=True):
    '''
    Use the 3-sigma method to adjust values that 
    fall outside the range [μ - 3σ, μ + 3σ] back into that range. 
    For values greater than μ + 3σ, they will be assigned as μ + 3σ, 
    and similarly for values smaller than μ - 3σ. 
    This method helps adjust outliers within the allowable range of variation 
    and reduces the impact of bias caused by them
    Zoom in the values of a column in a dataset to 3 sigma range.

    Input:
        col : str
            Column name.
        dataset : pandas.DataFrame
            Dataset to zoom in.
        dataset_apl : pandas.DataFrame
            Dataset to apply the zoomed values.
        verbose: boolean
            Print information of high and low values or not
            default = True
    Output:
        xnew : list
            List of zoomed values.
    '''
    xs = dataset[col]
    mu = xs.mean()
    sigma = xs.std()
    low = mu - 3*sigma
    high = mu + 3*sigma

    def _value(x):
        if x < low:
            return low
        elif x > high:
            return high
        else:
            return x
    xapl = dataset_apl[col]
    xnew = list(map(lambda x: _value(x), xapl))
    n_low = len([i for i in xnew if i == low])
    n_high = len([i for i in xnew if i == high])
    n = len(xapl)
    if verbose:
        print(col)
        print('Percentage of low: {:.2f}{}'.format(100*n_low/n, '%'))
        print('Percentage of high: {:.2f}{}'.format(100*n_high/n, '%'))
        print('Low value: {:.2f}'.format(low))
        print('High value: {:.2f}'.format(high))
        print('*'*20)
    return xnew


def _count_unique(x):
    '''
    Count unique values of a pandas.Series. 
        Input:
            x : pandas.Series
                Series to count unique values.
        Output:
                Number of unique values.
    '''
    return pd.Series.nunique(x)


def find_features(df):
    ''' Find features that have more than 500 unique values.
        Input:
            df : pandas.DataFrame
                Dataset to find features.
        Output:
            cols_3sigma : list
                List of features that have more than 500 unique values.
    '''
    tbl_dis_val = df.apply(_count_unique).sort_values(ascending=False)
    cols_3sigma = tbl_dis_val[tbl_dis_val > 500].index.tolist()
    cols_3sigma = [c for c in cols_3sigma if c != 'SK_ID_CURR']
    return cols_3sigma

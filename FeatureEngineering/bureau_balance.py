from utils import one_hot_encoder, group_and_merge
import pandas as pd
import os
import gc


def bureau_balance(path_to_data):
    ''' Process dseb63_bureau_balance.csv and return a pandas dataframe. '''
    bb = pd.read_csv(os.path.join(path_to_data, 'dseb63_bureau_balance.csv'))

    # Credit duration and credit/account end date difference
    bb, cat_cols = one_hot_encoder(bb, nan_as_category=False)

    # Calculate rate for each category with decay
    bb_processed = bb.groupby('SK_ID_BUREAU')[cat_cols].mean().reset_index()

    # Min, Max, Count and mean duration of payments (months)
    agg = {'MONTHS_BALANCE': ['min', 'max', 'mean', 'size']}
    bb_processed = group_and_merge(bb, bb_processed, '', agg, 'SK_ID_BUREAU')

    del bb
    gc.collect()
    return bb_processed

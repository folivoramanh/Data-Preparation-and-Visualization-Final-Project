from utils import *
from application_train_test import application
from bureau import bureau
import pandas as pd
from credit_card_balance import credit_card
from installment_payment import installment
from previous_application import previous_application
from pos_cash import pos_cash
import gc
import re

path_to_data = r'<replace it by your own path to data>'

with timer('Loading application_train and application_test'):
    df = application(path_to_data)
    print('--=> df after loading application:', df.shape)
    gc.collect()

with timer('Loading bureau data and merge with train/test data'):
    df = df.merge(bureau(path_to_data=path_to_data),
                  how='left', on='SK_ID_CURR')
    print('--=> df after merge with bureau:', df.shape)
    gc.collect()

with timer('Loading previous application data and merge with train/test data'):
    df = df.merge(previous_application(path_to_data=path_to_data),
                  how='left', on='SK_ID_CURR')
    print('--=> df after merge with previous application:', df.shape)
    gc.collect()

with timer('Loading POS_CASH_balance data and merge with train/test data'):
    df = df.merge(pos_cash(path_to_data=path_to_data),
                  how='left', on='SK_ID_CURR')
    print('--=> df after merge with pos cash:', df.shape)
    gc.collect()

with timer('Loading installments_payments data and merge with train/test data'):
    df = df.merge(installment(path_to_data=path_to_data),
                  how='left', on='SK_ID_CURR')
    print('--=> df after merge with installments:', df.shape)
    gc.collect()

with timer('Loading credit_card_balance data and merge with train/test data'):
    df = df.merge(credit_card(path_to_data=path_to_data),
                  how='left', on='SK_ID_CURR')
    print('--=> df after merge with credit card:', df.shape)
    gc.collect()

with timer('Adding ratios features'):
    df = add_ratios_features(df)
    print('--=> df after adding ratios features:', df.shape)
    gc.collect()

with timer('Adding 3 sigma features'):
    cols = find_features(df)
    for col in cols:
        df[col] = zoom_3sigma(col, df, df, verbose=False)
    print('--=> df after adding 3sigma columns: ', df.shape)
    gc.collect()

with timer('Reducing memory usage'):
    df = reduce_mem_usage(df, verbose=True)
    gc.collect()

with timer('Rename columns'):
    df = df.rename(columns=lambda x: re.sub('[^A-Za-z0-9_]+', '_', x))
    print('names of feature are renamed')
    gc.collect()

with timer('Save data'):
    df.to_csv('FeatEng.csv', index=False)
    print('data is saved')
    gc.collect()

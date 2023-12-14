import pandas as pd
import numpy as np
import gc
import os
from utils import one_hot_encoder, group, group_and_merge
from utils import PREVIOUS_AGG, PREVIOUS_ACTIVE_AGG, PREVIOUS_APPROVED_AGG, PREVIOUS_REFUSED_AGG, \
    PREVIOUS_LATE_PAYMENTS_AGG, PREVIOUS_TIME_AGG, PREVIOUS_LOAN_TYPE_AGG


def previous_application(path_to_data):
    """ Process mainly on dseb63_previous_application.csv and and merge with 
    some solumns of dseb63_installments_payments.csv for insights return a pandas dataframe. """
    # Read data dseb63_previous_application.csv and dseb63_installments_payments.csv
    prev = pd.read_csv(os.path.join(
        path_to_data, 'dseb63_previous_application.csv'))
    pay = pd.read_csv(os.path.join(
        path_to_data, 'dseb63_installments_payments.csv'))

    # One-hot encode most important categorical features
    enc_columns = [
        'NAME_CONTRACT_STATUS', 'NAME_CONTRACT_TYPE', 'CHANNEL_TYPE',
        'NAME_TYPE_SUITE', 'NAME_YIELD_GROUP', 'PRODUCT_COMBINATION',
        'NAME_PRODUCT_TYPE', 'NAME_CLIENT_TYPE']
    prev, categorical_cols = one_hot_encoder(
        prev, enc_columns, nan_as_category=False)

    new_coding = {"0": "Yes", "1": "No"}
    # Calculate ratios and difference for some columns
    prev['APPLICATION_CREDIT_DIFF'] = prev['AMT_APPLICATION'] - prev['AMT_CREDIT']
    prev['APPLICATION_CREDIT_RATIO'] = prev['AMT_APPLICATION'] / prev['AMT_CREDIT']

    prev['CREDIT_TO_ANNUITY_RATIO'] = prev['AMT_CREDIT']/prev['AMT_ANNUITY']

    prev['DOWN_PAYMENT_TO_CREDIT'] = prev['AMT_DOWN_PAYMENT'] / prev['AMT_CREDIT']
    prev["NEW_APP_CREDIT_RATE_RATIO"] = prev["APPLICATION_CREDIT_RATIO"].apply(
        lambda x: 1 if (x <= 1) else 0)
    prev['NEW_APP_CREDIT_RATE_RATIO'] = prev['NEW_APP_CREDIT_RATE_RATIO'].astype(
        'O')
    prev['NEW_APP_CREDIT_RATE_RATIO'] = prev['NEW_APP_CREDIT_RATE_RATIO'].replace(
        new_coding)

    prev["NEW_CNT_PAYMENT"] = pd.cut(x=prev['CNT_PAYMENT'], bins=[
                                     0, 12, 60, 120], labels=["Short", "Middle", "Long"])
    prev['NEW_CREDIT_GOODS_RATE'] = prev['AMT_CREDIT'] / prev['AMT_GOODS_PRICE']

    prev["NEW_END_DIFF"] = prev["DAYS_TERMINATION"] - prev["DAYS_LAST_DUE"]
    prev['NEW_DAYS_DUE_DIFF'] = prev['DAYS_LAST_DUE_1ST_VERSION'] - \
        prev['DAYS_FIRST_DUE']
    prev['NEW_RETURN_DAY'] = prev['DAYS_DECISION'] + prev['CNT_PAYMENT'] * 30
    prev['NEW_DAYS_TERMINATION_DIFF'] = prev['DAYS_TERMINATION'] - \
        prev['NEW_RETURN_DAY']

    prev['NFLAG_LAST_APPL_IN_DAY'] = prev['NFLAG_LAST_APPL_IN_DAY'].astype("O")

    # Interest ratio on previous application
    total_payment = prev['AMT_ANNUITY'] * prev['CNT_PAYMENT']
    prev['SIMPLE_INTERESTS'] = (
        total_payment/prev['AMT_CREDIT'] - 1)/prev['CNT_PAYMENT']
    prev['AMT_INTEREST'] = prev['CNT_PAYMENT'] * \
        prev['AMT_ANNUITY'] - prev['AMT_CREDIT']
    prev['INTEREST_SHARE'] = prev['AMT_INTEREST'] / \
        (prev['AMT_CREDIT'] + 0.00001)  # smoothing to avoid division by zero
    prev['INTEREST_RATE'] = 2 * 12 * prev['AMT_INTEREST'] / \
        (prev['AMT_CREDIT'] * (prev['CNT_PAYMENT'] + 1))

    # Active loans - approved and not complete yet (last_due 365243)
    approved = prev[prev['NAME_CONTRACT_STATUS_Approved'] == 1]
    active_df = approved[approved['DAYS_LAST_DUE'] == 365243]

    # Find how much was already payed in active loans (using installments csv)
    active_pay = pay[pay['SK_ID_PREV'].isin(active_df['SK_ID_PREV'])]
    active_pay_agg = active_pay.groupby(
        'SK_ID_PREV')[['AMT_INSTALMENT', 'AMT_PAYMENT']].sum()
    active_pay_agg.reset_index(inplace=True)

    # Active loans: difference of what was payed and installments
    active_pay_agg['INSTALMENT_PAYMENT_DIFF'] = active_pay_agg['AMT_INSTALMENT'] - \
        active_pay_agg['AMT_PAYMENT']

    # Merge with active_df
    active_df = active_df.merge(active_pay_agg, on='SK_ID_PREV', how='left')
    active_df['REMAINING_DEBT'] = active_df['AMT_CREDIT'] - \
        active_df['AMT_PAYMENT']
    active_df['REPAYMENT_RATIO'] = active_df['AMT_PAYMENT'] / \
        active_df['AMT_CREDIT']

    # Perform aggregations for active applications
    active_agg_df = group(active_df, 'PREV_ACTIVE_', PREVIOUS_ACTIVE_AGG)
    active_agg_df['TOTAL_REPAYMENT_RATIO'] = active_agg_df['PREV_ACTIVE_AMT_PAYMENT_SUM'] /\
        active_agg_df['PREV_ACTIVE_AMT_CREDIT_SUM']
    del active_pay, active_pay_agg, active_df

    # Change 365.243 values to nan (missing)
    prev['DAYS_FIRST_DRAWING'].replace(365243, np.nan, inplace=True)
    prev['DAYS_FIRST_DUE'].replace(365243, np.nan, inplace=True)
    prev['DAYS_LAST_DUE_1ST_VERSION'].replace(365243, np.nan, inplace=True)
    prev['DAYS_LAST_DUE'].replace(365243, np.nan, inplace=True)
    prev['DAYS_TERMINATION'].replace(365243, np.nan, inplace=True)

    # Days last due difference (scheduled x done)
    prev['DAYS_LAST_DUE_DIFF'] = prev['DAYS_LAST_DUE_1ST_VERSION'] - \
        prev['DAYS_LAST_DUE']
    approved['DAYS_LAST_DUE_DIFF'] = approved['DAYS_LAST_DUE_1ST_VERSION'] - \
        approved['DAYS_LAST_DUE']

    # Categorical features
    categorical_agg = {key: ['mean'] for key in categorical_cols}

    # Perform general aggregations
    agg_prev = group(prev, 'PREV_', {**PREVIOUS_AGG, **categorical_agg})

    # Merge active loans dataframe on agg_prev
    agg_prev = agg_prev.merge(active_agg_df, how='left', on='SK_ID_CURR')
    del active_agg_df

    # Aggregations for approved and refused loans
    agg_prev = group_and_merge(
        approved, agg_prev, 'APPROVED_', PREVIOUS_APPROVED_AGG)
    refused = prev[prev['NAME_CONTRACT_STATUS_Refused'] == 1]
    agg_prev = group_and_merge(
        refused, agg_prev, 'REFUSED_', PREVIOUS_REFUSED_AGG)
    del approved, refused

    # Aggregations for Consumer loans and Cash loans
    for loan_type in ['Consumer loans', 'Cash loans']:
        type_df = prev[prev['NAME_CONTRACT_TYPE_{}'.format(loan_type)] == 1]
        prefix = 'PREV_' + loan_type.split(" ")[0] + '_'
        agg_prev = group_and_merge(
            type_df, agg_prev, prefix, PREVIOUS_LOAN_TYPE_AGG)
    del type_df

    # Get the SK_ID_PREV for loans with late payments (days past due)
    pay['LATE_PAYMENT'] = pay['DAYS_ENTRY_PAYMENT'] - pay['DAYS_INSTALMENT']
    pay['LATE_PAYMENT'] = pay['LATE_PAYMENT'].apply(
        lambda x: 1 if x > 0 else 0)
    dpd_id = pay[pay['LATE_PAYMENT'] > 0]['SK_ID_PREV'].unique()

    # Aggregations for loans with late payments
    agg_dpd = group_and_merge(prev[prev['SK_ID_PREV'].isin(dpd_id)], agg_prev,
                              'PREV_LATE_', PREVIOUS_LATE_PAYMENTS_AGG)
    del agg_dpd, dpd_id

    # Aggregations for loans in the last x months
    for time_frame in [12, 24]:
        time_frame_df = prev[prev['DAYS_DECISION'] >= -30*time_frame]
        prefix = 'PREV_LAST{}M_'.format(time_frame)
        agg_prev = group_and_merge(
            time_frame_df, agg_prev, prefix, PREVIOUS_TIME_AGG)
        del time_frame_df

    del prev
    gc.collect()
    return agg_prev

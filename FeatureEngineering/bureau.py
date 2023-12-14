from utils import one_hot_encoder, group, group_and_merge
from utils import BUREAU_ACTIVE_AGG, BUREAU_AGG, BUREAU_CLOSED_AGG, BUREAU_LOAN_TYPE_AGG, BUREAU_TIME_AGG
from bureau_balance import bureau_balance
import pandas as pd
import os
import gc


def bureau(path_to_data):
    """ Process dseb63_bureau.csv and dseb63_bureau_balance.csv and return a pandas dataframe. """
    bureau = pd.read_csv(os.path.join(path_to_data, 'dseb63_bureau.csv'))

    # Credit duration and credit/account end date difference
    bureau['CREDIT_DURATION'] = -bureau['DAYS_CREDIT'] + \
        bureau['DAYS_CREDIT_ENDDATE']
    bureau['ENDDATE_DIF'] = bureau['DAYS_CREDIT_ENDDATE'] - \
        bureau['DAYS_ENDDATE_FACT']
    bureau['DCREDIT_DOVERDUE_DIFF'] = bureau['DAYS_CREDIT'] - \
        bureau['CREDIT_DAY_OVERDUE']  # days credit overdue diff
    bureau['DCREDIT_DENDFACT_DIFF'] = bureau['DAYS_CREDIT'] - \
        bureau['DAYS_ENDDATE_FACT']  # days credit endfact diff
    bureau['DUPDATE_DENDATE_DIFF'] = bureau['DAYS_CREDIT_UPDATE'] - \
        bureau['DAYS_CREDIT_ENDDATE']  # days update enddate diff

    # Credit to debt ratio and difference
    bureau['DEBT_PERCENTAGE'] = bureau['AMT_CREDIT_SUM'] / \
        bureau['AMT_CREDIT_SUM_DEBT']
    bureau['DEBT_CREDIT_DIFF'] = bureau['AMT_CREDIT_SUM'] - \
        bureau['AMT_CREDIT_SUM_DEBT']
    bureau['CREDIT_TO_ANNUITY_RATIO'] = bureau['AMT_CREDIT_SUM'] / \
        bureau['AMT_ANNUITY']
    bureau['BUREAU_CREDIT_FACT_DIFF'] = bureau['DAYS_CREDIT'] - \
        bureau['DAYS_ENDDATE_FACT']
    bureau['BUREAU_CREDIT_ENDDATE_DIFF'] = bureau['DAYS_CREDIT'] - \
        bureau['DAYS_CREDIT_ENDDATE']
    bureau['BUREAU_CREDIT_DEBT_RATIO'] = bureau['AMT_CREDIT_SUM_DEBT'] / \
        bureau['AMT_CREDIT_SUM']
    bureau['DEBT_CREDIT_LIMIT_DIFF'] = bureau['AMT_CREDIT_SUM'] - \
        bureau['AMT_CREDIT_SUM_LIMIT']
    bureau['DEBT_CREDIT_OVERDUE_DIFF'] = bureau['AMT_CREDIT_SUM'] - \
        bureau['AMT_CREDIT_SUM_OVERDUE']

    # CREDIT_DAY_OVERDUE :
    bureau['BUREAU_IS_DPD'] = bureau['CREDIT_DAY_OVERDUE'].apply(
        lambda x: 1 if x > 0 else 0)
    bureau['BUREAU_IS_DPD_OVER120'] = bureau['CREDIT_DAY_OVERDUE'].apply(
        lambda x: 1 if x > 120 else 0)

    # One-hot encoder
    bureau, _ = one_hot_encoder(bureau, nan_as_category=False)

    # Join bureau balance features
    bureau = bureau.merge(bureau_balance(path_to_data),
                          how='left', on='SK_ID_BUREAU')

    # Flag months with late payments (days past due)
    bureau['STATUS_12345'] = 0
    for i in range(1, 6):
        bureau['STATUS_12345'] += bureau[f'STATUS_{i}']

    # Aggregate by number of months in balance and merge with bureau (loan length agg)
    features = ['AMT_CREDIT_MAX_OVERDUE', 'AMT_CREDIT_SUM_OVERDUE', 'AMT_CREDIT_SUM',
                'AMT_CREDIT_SUM_DEBT', 'DEBT_PERCENTAGE',
                'DEBT_CREDIT_DIFF', 'STATUS_0', 'STATUS_12345']
    agg_length = bureau.groupby('MONTHS_BALANCE_SIZE')[
        features].mean().reset_index()
    agg_length.rename(
        {feat: 'LL_' + feat for feat in features}, axis=1, inplace=True)
    bureau = bureau.merge(agg_length, how='left', on='MONTHS_BALANCE_SIZE')
    del agg_length

    # General loans aggregations
    bureau_agg = group(bureau, 'BUREAU_', BUREAU_AGG)

    # Active and closed loans aggregations
    active = bureau[bureau['CREDIT_ACTIVE_Active'] == 1]
    bureau_agg = group_and_merge(
        active, bureau_agg, 'BUREAU_ACTIVE_', BUREAU_ACTIVE_AGG)
    closed = bureau[bureau['CREDIT_ACTIVE_Closed'] == 1]
    bureau_agg = group_and_merge(
        closed, bureau_agg, 'BUREAU_CLOSED_', BUREAU_CLOSED_AGG)
    del active, closed

    # Aggregations for the main loan types
    for credit_type in ['Consumer credit', 'Credit card', 'Mortgage', 'Car loan', 'Microloan']:
        type_df = bureau[bureau['CREDIT_TYPE_' + credit_type] == 1]
        prefix = 'BUREAU_' + \
            credit_type.split(' ', maxsplit=1)[0].upper() + '_'
        bureau_agg = group_and_merge(
            type_df, bureau_agg, prefix, BUREAU_LOAN_TYPE_AGG)
        del type_df

    # Time based aggregations: last x months
    for time_frame in [6, 12]:
        prefix = f"BUREAU_LAST{time_frame}M_"
        time_frame_df = bureau[bureau['DAYS_CREDIT'] >= -30*time_frame]
        bureau_agg = group_and_merge(
            time_frame_df, bureau_agg, prefix, BUREAU_TIME_AGG)
        del time_frame_df

    # Last loan max overdue
    sort_bureau = bureau.sort_values(by=['DAYS_CREDIT'])
    del bureau
    gr = sort_bureau.groupby('SK_ID_CURR')[
        'AMT_CREDIT_MAX_OVERDUE'].last().reset_index()
    gr.rename(
        {'AMT_CREDIT_MAX_OVERDUE': 'BUREAU_LAST_LOAN_MAX_OVERDUE'}, inplace=True)
    bureau_agg = bureau_agg.merge(gr, on='SK_ID_CURR', how='left')
    del gr, sort_bureau

    # Ratios: total debt/total credit and active loans debt/ active loans credit
    bureau_agg['BUREAU_DEBT_OVER_CREDIT'] = \
        bureau_agg['BUREAU_AMT_CREDIT_SUM_DEBT_SUM'] / \
        bureau_agg['BUREAU_AMT_CREDIT_SUM_SUM']
    bureau_agg['BUREAU_ACTIVE_DEBT_OVER_CREDIT'] = \
        bureau_agg['BUREAU_ACTIVE_AMT_CREDIT_SUM_DEBT_SUM'] / \
        bureau_agg['BUREAU_ACTIVE_AMT_CREDIT_SUM_SUM']

    gc.collect()
    return bureau_agg

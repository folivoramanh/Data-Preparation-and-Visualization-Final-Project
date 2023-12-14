from utils import one_hot_encoder, group, do_sum
from utils import POS_CASH_AGG
import pandas as pd
import os
import gc


def pos_cash(path_to_data):
    """ Process dseb63_POS_CASH_balance.csv and return a pandas dataframe. """
    pos = pd.read_csv(os.path.join(
        path_to_data, 'dseb63_POS_CASH_balance.csv'))

    # computing Exponential Moving Average for some features based on MONTHS_BALANCE
    columns_for_ema = ['CNT_INSTALMENT', 'CNT_INSTALMENT_FUTURE']
    exp_columns = ['EXP_'+ele for ele in columns_for_ema]
    pos[exp_columns] = pos.groupby('SK_ID_PREV')[columns_for_ema].transform(
        lambda x: x.ewm(alpha=0.6).mean())

    # One-hot encode categorical features
    pos, categorical_cols = one_hot_encoder(pos, nan_as_category=False)

    # Flag months with late payment
    pos['LATE_PAYMENT'] = pos['SK_DPD'].apply(lambda x: 1 if x > 0 else 0)

    # Flag days past due
    pos['POS_IS_DPD'] = pos['SK_DPD'].apply(lambda x: 1 if x > 0 else 0)

    # Flag days past due less than 120 days
    pos['POS_IS_DPD_UNDER_120'] = pos['SK_DPD'].apply(
        lambda x: 1 if (x > 0) & (x < 120) else 0)

    # Flag days past due over 120 days
    pos['POS_IS_DPD_OVER_120'] = pos['SK_DPD'].apply(
        lambda x: 1 if x >= 120 else 0)

    # Aggregate by SK_ID_CURR
    categorical_agg = {key: ['mean'] for key in categorical_cols}
    pos_agg = group(pos, 'POS_', {**POS_CASH_AGG, **categorical_agg})

    # Sort and group by SK_ID_PREV
    sort_pos = pos.sort_values(by=['SK_ID_PREV', 'MONTHS_BALANCE'])
    gp = sort_pos.groupby('SK_ID_PREV')

    # Create new dataframe to store features calculated from gp
    df = pd.DataFrame()

    df['SK_ID_CURR'] = gp['SK_ID_CURR'].first()
    df['MONTHS_BALANCE_MAX'] = gp['MONTHS_BALANCE'].max()

    # Percentage of previous loans completed and completed before initial term
    df['POS_LOAN_COMPLETED_MEAN'] = gp['NAME_CONTRACT_STATUS_Completed'].mean()
    df['POS_COMPLETED_BEFORE_MEAN'] = gp['CNT_INSTALMENT'].first() - \
        gp['CNT_INSTALMENT'].last()
    df['POS_COMPLETED_BEFORE_MEAN'] = df.apply(lambda x: 1 if x['POS_COMPLETED_BEFORE_MEAN'] > 0
                                               and x['POS_LOAN_COMPLETED_MEAN'] > 0 else 0, axis=1)

    # Number of remaining installments (future installments) and percentage from total
    df['POS_REMAINING_INSTALMENTS'] = gp['CNT_INSTALMENT_FUTURE'].last()
    df['POS_REMAINING_INSTALMENTS_RATIO'] = gp['CNT_INSTALMENT_FUTURE'].last() / \
        gp['CNT_INSTALMENT'].last()

    # Group by SK_ID_CURR and merge
    df_gp = df.groupby('SK_ID_CURR').sum().reset_index()
    df_gp.drop(['MONTHS_BALANCE_MAX'], axis=1, inplace=True)
    pos_agg = pd.merge(pos_agg, df_gp, on='SK_ID_CURR', how='left')
    del df, gp, df_gp, sort_pos

    # Percentage of late payments for the 3 most recent applications
    pos = do_sum(pos, ['SK_ID_PREV'], 'LATE_PAYMENT', 'LATE_PAYMENT_SUM')

    # Last month of each application
    last_month_df = pos.groupby('SK_ID_PREV')['MONTHS_BALANCE'].idxmax()

    # Most recent applications (last 3)
    sort_pos = pos.sort_values(by=['SK_ID_PREV', 'MONTHS_BALANCE'])
    gp = sort_pos.iloc[last_month_df].groupby('SK_ID_CURR').tail(3)

    # Average application features over the last 3 applications
    gp_mean = gp.groupby('SK_ID_CURR').mean().reset_index()
    pos_agg = pd.merge(
        pos_agg, gp_mean[['SK_ID_CURR', 'LATE_PAYMENT_SUM']], on='SK_ID_CURR', how='left')

    # Drop some useless categorical features, which were created to calculate to other features
    drop_features = [
        'POS_NAME_CONTRACT_STATUS_Canceled_MEAN', 'POS_NAME_CONTRACT_STATUS_Amortized debt_MEAN',
        'POS_NAME_CONTRACT_STATUS_XNA_MEAN']
    pos_agg.drop(drop_features, axis=1, inplace=True)
    del gp, gp_mean, sort_pos, pos
    gc.collect()
    return pos_agg

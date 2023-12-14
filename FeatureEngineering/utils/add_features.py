from scipy.stats import kurtosis, iqr, skew


def add_features_in_group(features, gr_, feature_name, aggs, prefix):
    '''
    Add new features to a dataframe groupby object.
        Input:
            features : dict
                Dictionary to store new features.
            gr_ : pandas.DataFrame
                Dataframe groupby object.
            feature_name : str
                Column name to calculate statistics.
            aggs : list
                List of method to calculate statistics.
            prefix : str
                Prefix of column names.
        Output:
            features : dict
                Dictionary with new features.
        '''
    for agg in aggs:
        if agg == 'sum':
            features[f'{prefix}{feature_name}_sum'] = gr_[
                feature_name].sum()
        elif agg == 'mean':
            features[f'{prefix}{feature_name}_mean'] = gr_[
                feature_name].mean()
        elif agg == 'max':
            features[f'{prefix}{feature_name}_max'] = gr_[
                feature_name].max()
        elif agg == 'min':
            features[f'{prefix}{feature_name}_min'] = gr_[
                feature_name].min()
        elif agg == 'std':
            features[f'{prefix}{feature_name}_std'] = gr_[
                feature_name].std()
        elif agg == 'count':
            features[f'{prefix}{feature_name}_count'] = gr_[
                feature_name].count()
        elif agg == 'skew':
            features[f'{prefix}{feature_name}_skew'] = skew(
                gr_[feature_name])
        elif agg == 'kurt':
            features[f'{prefix}{feature_name}_kurt'] = kurtosis(
                gr_[feature_name])
        elif agg == 'iqr':
            features[f'{prefix}{feature_name}_iqr'] = iqr(
                gr_[feature_name])
        elif agg == 'median':
            features[f'{prefix}{feature_name}_median'] = gr_[
                feature_name].median()
    return features


def installments_last_loan_features(gr):
    '''
    Calculate features for the last loan in installments_payments.csv.
        Input:
            gr : pandas.DataFrame
                DataFrame groupby object.
        Output:
            features : dict
                Dictionary with new features.
    '''
    gr_ = gr.copy()
    gr_.sort_values(['DAYS_INSTALMENT'], ascending=False, inplace=True)
    last_installment_id = gr_['SK_ID_PREV'].iloc[0]
    gr_ = gr_[gr_['SK_ID_PREV'] == last_installment_id]

    features = {}
    features = add_features_in_group(features, gr_, 'DPD',
                                     ['sum', 'mean', 'max', 'std'],
                                     'LAST_LOAN_')
    features = add_features_in_group(features, gr_, 'LATE_PAYMENT',
                                     ['count', 'mean'],
                                     'LAST_LOAN_')
    features = add_features_in_group(features, gr_, 'PAID_OVER_AMOUNT',
                                     ['sum', 'mean', 'max', 'min', 'std'],
                                     'LAST_LOAN_')
    features = add_features_in_group(features, gr_, 'PAID_OVER',
                                     ['count', 'mean'],
                                     'LAST_LOAN_')
    return features


def add_ratios_features(df):
    '''
    Calculate several ratios for the main dataset.
        Input:
            df : pandas.DataFrame
                Dataframe after merge with all other dataframes.
        Output:
            df : pandas.DataFrame
                Final ataframe with ratios added.
    '''

    # CREDIT TO INCOME RATIO
    df['BUREAU_INCOME_CREDIT_RATIO'] = df['BUREAU_AMT_CREDIT_SUM_MEAN'] / \
        df['AMT_INCOME_TOTAL']
    df['BUREAU_ACTIVE_CREDIT_TO_INCOME_RATIO'] = df['BUREAU_ACTIVE_AMT_CREDIT_SUM_SUM'] / \
        df['AMT_INCOME_TOTAL']

    # PREVIOUS TO CURRENT CREDIT RATIO
    df['CURRENT_TO_APPROVED_CREDIT_MIN_RATIO'] = df['APPROVED_AMT_CREDIT_MIN'] / \
        df['AMT_CREDIT']
    df['CURRENT_TO_APPROVED_CREDIT_MAX_RATIO'] = df['APPROVED_AMT_CREDIT_MAX'] / \
        df['AMT_CREDIT']
    df['CURRENT_TO_APPROVED_CREDIT_MEAN_RATIO'] = df['APPROVED_AMT_CREDIT_MEAN'] / df['AMT_CREDIT']

    # PREVIOUS TO CURRENT ANNUITY RATIO
    df['CURRENT_TO_APPROVED_ANNUITY_MAX_RATIO'] = df['APPROVED_AMT_ANNUITY_MAX'] / \
        df['AMT_ANNUITY']
    df['CURRENT_TO_APPROVED_ANNUITY_MEAN_RATIO'] = df['APPROVED_AMT_ANNUITY_MEAN'] / \
        df['AMT_ANNUITY']
    df['PAYMENT_MIN_TO_ANNUITY_RATIO'] = df['INS_AMT_PAYMENT_MIN'] / df['AMT_ANNUITY']
    df['PAYMENT_MAX_TO_ANNUITY_RATIO'] = df['INS_AMT_PAYMENT_MAX'] / df['AMT_ANNUITY']
    df['PAYMENT_MEAN_TO_ANNUITY_RATIO'] = df['INS_AMT_PAYMENT_MEAN'] / df['AMT_ANNUITY']

    # PREVIOUS TO CURRENT CREDIT TO ANNUITY RATIO
    df['CTA_CREDIT_TO_ANNUITY_MAX_RATIO'] = df['APPROVED_CREDIT_TO_ANNUITY_RATIO_MAX'] / \
        df['CREDIT_TO_ANNUITY_RATIO']
    df['CTA_CREDIT_TO_ANNUITY_MEAN_RATIO'] = df['APPROVED_CREDIT_TO_ANNUITY_RATIO_MEAN'] / \
        df['CREDIT_TO_ANNUITY_RATIO']

    # DAYS DIFFERENCES AND RATIOS
    df['DAYS_DECISION_MEAN_TO_BIRTH'] = df['APPROVED_DAYS_DECISION_MEAN'] / \
        df['DAYS_BIRTH']
    df['DAYS_CREDIT_MEAN_TO_BIRTH'] = df['BUREAU_DAYS_CREDIT_MEAN'] / df['DAYS_BIRTH']
    df['DAYS_DECISION_MEAN_TO_EMPLOYED'] = df['APPROVED_DAYS_DECISION_MEAN'] / \
        df['DAYS_EMPLOYED']
    df['DAYS_CREDIT_MEAN_TO_EMPLOYED'] = df['BUREAU_DAYS_CREDIT_MEAN'] / \
        df['DAYS_EMPLOYED']
    return df

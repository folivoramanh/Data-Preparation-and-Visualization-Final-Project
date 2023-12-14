import pandas as pd
import numpy as np
import os
import gc
from utils import do_median, do_std, do_mean
from utils import get_age_label
from category_encoders import WOEEncoder


def application(path_to_data):
    """ Process dseb63_application_train.csv and dseb63_application_test.csv and return a pandas dataframe. """
    # Read data
    df = pd.read_csv(os.path.join(
        path_to_data, 'dseb63_application_train.csv'), index_col=0)
    test_df = pd.read_csv(os.path.join(
        path_to_data, 'dseb63_application_test.csv'), index_col=0)

    # WOE encoding for train and test
    feats = [f for f in df.columns if f not in ['TARGET', 'SK_ID_CURR']]
    target = df['TARGET']
    enc = WOEEncoder(return_df=True)
    df_encode = enc.fit_transform(df[feats], target)
    df_encode['SK_ID_CURR'] = df['SK_ID_CURR']
    df_encode['TARGET'] = target
    df_test_enc = enc.transform(test_df[feats])
    df_test_enc['SK_ID_CURR'] = test_df['SK_ID_CURR']

    # Merge train and test data for feature engineering
    df = pd.concat([df_encode, df_test_enc]).reset_index(drop=True)
    del df_encode, df_test_enc, test_df

    # NaN values for DAYS_EMPLOYED: 365.243 -> nan
    df['DAYS_EMPLOYED'].replace(365243, np.nan, inplace=True)  # set null value
    df['DAYS_LAST_PHONE_CHANGE'].replace(
        0, np.nan, inplace=True)  # set null value
    df['DAYS_BIRTH'] = df['DAYS_BIRTH'] * -1 / 365

    # Income by origin
    inc_by_org = df[['AMT_INCOME_TOTAL', 'ORGANIZATION_TYPE']].groupby(
        'ORGANIZATION_TYPE').median()['AMT_INCOME_TOTAL']
    df['NEW_INC_BY_ORG'] = df['ORGANIZATION_TYPE'].map(inc_by_org)

    # Categorical features with Binary encode (0 or 1; two categories)
    for bin_feature in ['CODE_GENDER', 'FLAG_OWN_CAR', 'FLAG_OWN_REALTY']:
        df[bin_feature], _ = pd.factorize(df[bin_feature])

    # Flag_document features - count and kurtosis
    docs = [f for f in df.columns if 'FLAG_DOC' in f]
    df['DOCUMENT_COUNT'] = df[docs].sum(axis=1)
    df['NEW_DOC_KURT'] = df[docs].kurtosis(axis=1)

    # Categorical age - based on target=1 plot
    df['AGE_RANGE'] = df['DAYS_BIRTH'].apply(lambda x: get_age_label(x))

    # Some simple new features (percentages)
    df['PAYMENT_RATE'] = df['AMT_ANNUITY'] / df['AMT_CREDIT']

    # Credit ratios
    df['CREDIT_TO_ANNUITY_RATIO'] = df['AMT_CREDIT'] / df['AMT_ANNUITY']
    df['CREDIT_TO_GOODS_RATIO'] = df['AMT_CREDIT'] / df['AMT_GOODS_PRICE']
    df['GOODS_INCOME_RATIO'] = df['AMT_GOODS_PRICE'] / df['AMT_INCOME_TOTAL']

    # Income ratios
    df['ANNUITY_TO_INCOME_RATIO'] = df['AMT_ANNUITY'] / df['AMT_INCOME_TOTAL']
    df['CREDIT_TO_INCOME_RATIO'] = df['AMT_CREDIT'] / df['AMT_INCOME_TOTAL']
    df['INCOME_TO_EMPLOYED_RATIO'] = df['AMT_INCOME_TOTAL'] / df['DAYS_EMPLOYED']
    df['INCOME_TO_BIRTH_RATIO'] = df['AMT_INCOME_TOTAL'] / df['DAYS_BIRTH']
    df['INCOME_ANNUITY_DIFF'] = df['AMT_INCOME_TOTAL'] - df['AMT_ANNUITY']
    df['INCOME_EXT_RATIO'] = df['AMT_INCOME_TOTAL'] / df['EXT_SOURCE_3']
    df['CREDIT_EXT_RATIO'] = df['AMT_CREDIT'] / df['EXT_SOURCE_3']
    df['APP_AMT_INCOME_TOTAL_12_AMT_ANNUITY_ratio'] = df['AMT_INCOME_TOTAL'] / \
        12. - df['AMT_ANNUITY']  # Income per month - Annuity

    # Time ratios
    df['EMPLOYED_TO_BIRTH_RATIO'] = df['DAYS_EMPLOYED'] / df['DAYS_BIRTH']
    df['ID_TO_BIRTH_RATIO'] = df['DAYS_ID_PUBLISH'] / df['DAYS_BIRTH']
    df['CAR_TO_BIRTH_RATIO'] = df['OWN_CAR_AGE'] / df['DAYS_BIRTH']
    df['CAR_TO_EMPLOYED_RATIO'] = df['OWN_CAR_AGE'] / df['DAYS_EMPLOYED']
    df['PHONE_TO_BIRTH_RATIO'] = df['DAYS_LAST_PHONE_CHANGE'] / df['DAYS_BIRTH']

    # EXT_SOURCE_X FEATURE (External source)
    for function_name in ['min', 'max', 'mean', 'nanmedian']:
        feature_name = 'EXT_SOURCES_{}'.format(function_name.upper())
        df[feature_name] = eval('np.{}'.format(function_name))(
            df[['EXT_SOURCE_1', 'EXT_SOURCE_2', 'EXT_SOURCE_3']], axis=1)
    # df['APPS_EXT_SOURCE_MEAN'] = df[['EXT_SOURCE_1', 'EXT_SOURCE_2', 'EXT_SOURCE_3']].mean(axis=1)
    df['APPS_EXT_SOURCE_STD'] = df[['EXT_SOURCE_1',
                                    'EXT_SOURCE_2', 'EXT_SOURCE_3']].std(axis=1)
    df['APPS_EXT_SOURCE_STD'] = df['APPS_EXT_SOURCE_STD'].fillna(
        df['APPS_EXT_SOURCE_STD'].mean())
    # df['APP_SCORE1_TO_BIRTH_RATIO'] = df['EXT_SOURCE_1'] / (df['DAYS_BIRTH'] / 365.25)
    # df['APP_SCORE2_TO_BIRTH_RATIO'] = df['EXT_SOURCE_2'] / (df['DAYS_BIRTH'] / 365.25)
    # df['APP_SCORE3_TO_BIRTH_RATIO'] = df['EXT_SOURCE_3'] / (df['DAYS_BIRTH'] / 365.25)
    df['APP_SCORE1_TO_EMPLOY_RATIO'] = df['EXT_SOURCE_1'] / \
        (df['DAYS_EMPLOYED'] / 365.25)
    df['EXT_SOURCES_PROD'] = df['EXT_SOURCE_1'] * \
        df['EXT_SOURCE_2'] * df['EXT_SOURCE_3']
    df['EXT_SOURCES_WEIGHTED'] = df.EXT_SOURCE_1 * \
        2 + df.EXT_SOURCE_2 * 1 + df.EXT_SOURCE_3 * 3
    df['APP_EXT_SOURCE_2*EXT_SOURCE_3*DAYS_BIRTH'] = df['EXT_SOURCE_1'] * \
        df['EXT_SOURCE_2'] * df['DAYS_BIRTH']
    df['APP_SCORE1_TO_FAM_CNT_RATIO'] = df['EXT_SOURCE_1'] / df['CNT_FAM_MEMBERS']
    df['APP_SCORE1_TO_GOODS_RATIO'] = df['EXT_SOURCE_1'] / df['AMT_GOODS_PRICE']
    df['APP_SCORE1_TO_CREDIT_RATIO'] = df['EXT_SOURCE_1'] / df['AMT_CREDIT']
    df['APP_SCORE1_TO_SCORE2_RATIO'] = df['EXT_SOURCE_1'] / df['EXT_SOURCE_2']
    df['APP_SCORE1_TO_SCORE3_RATIO'] = df['EXT_SOURCE_1'] / df['EXT_SOURCE_3']
    df['APP_SCORE2_TO_CREDIT_RATIO'] = df['EXT_SOURCE_2'] / df['AMT_CREDIT']
    df['APP_SCORE2_TO_REGION_RATING_RATIO'] = df['EXT_SOURCE_2'] / \
        df['REGION_RATING_CLIENT']
    df['APP_SCORE2_TO_CITY_RATING_RATIO'] = df['EXT_SOURCE_2'] / \
        df['REGION_RATING_CLIENT_W_CITY']
    df['APP_SCORE2_TO_POP_RATIO'] = df['EXT_SOURCE_2'] / \
        df['REGION_POPULATION_RELATIVE']
    df['APP_SCORE2_TO_PHONE_CHANGE_RATIO'] = df['EXT_SOURCE_2'] / \
        df['DAYS_LAST_PHONE_CHANGE']
    df['EXT_SOURCE_1^2'] = df['EXT_SOURCE_1']**2
    df['EXT_SOURCE_2^2'] = df['EXT_SOURCE_2']**2
    df['EXT_SOURCE_3^2'] = df['EXT_SOURCE_3']**2
    df['APP_EXT_SOURCE_1*EXT_SOURCE_2'] = df['EXT_SOURCE_1'] * df['EXT_SOURCE_2']
    df['APP_EXT_SOURCE_1*EXT_SOURCE_3'] = df['EXT_SOURCE_1'] * df['EXT_SOURCE_3']
    df['APP_EXT_SOURCE_2*EXT_SOURCE_3'] = df['EXT_SOURCE_2'] * df['EXT_SOURCE_3']
    df['EXT_SOURCE_1 * DAYS_EMPLOYED'] = df['EXT_SOURCE_1'] * df['DAYS_EMPLOYED']
    df['EXT_SOURCE_2 * DAYS_EMPLOYED'] = df['EXT_SOURCE_2'] * df['DAYS_EMPLOYED']
    df['EXT_SOURCE_3 * DAYS_EMPLOYED'] = df['EXT_SOURCE_3'] * df['DAYS_EMPLOYED']
    df['EXT_SOURCE_1 / DAYS_BIRTH'] = df['EXT_SOURCE_1'] / df['DAYS_BIRTH']
    df['EXT_SOURCE_2 / DAYS_BIRTH'] = df['EXT_SOURCE_2'] / df['DAYS_BIRTH']
    df['EXT_SOURCE_3 / DAYS_BIRTH'] = df['EXT_SOURCE_3'] / df['DAYS_BIRTH']

    # ratio feature
    df['APP_DAYS_EMPLOYED_DAYS_BIRTH_diff'] = df['DAYS_EMPLOYED'] - df['DAYS_BIRTH']

    # Feature based on average per person
    df['INCOME_PER_PERSON'] = df['AMT_INCOME_TOTAL'] / df['CNT_FAM_MEMBERS']
    df['CREDIT_PER_PERSON'] = df['AMT_CREDIT'] / df['CNT_FAM_MEMBERS']

    # percentage of income
    df['INCOME_CREDIT_PERCENTAGE'] = df['AMT_INCOME_TOTAL'] / df['AMT_CREDIT']

    df['PHONE_TO_EMPLOY_RATIO'] = df['DAYS_LAST_PHONE_CHANGE'] / df['DAYS_EMPLOYED']

    # Ratio and diff related to children
    df['CHILDREN_RATIO'] = df['CNT_CHILDREN'] / df['CNT_FAM_MEMBERS']
    df['CNT_NON_CHILD'] = df['CNT_FAM_MEMBERS'] - df['CNT_CHILDREN']
    df['CHILD_TO_NON_CHILD_RATIO'] = df['CNT_CHILDREN'] / df['CNT_NON_CHILD']
    df['CREDIT_PER_CHILD'] = df['AMT_CREDIT'] / (1 + df['CNT_CHILDREN'])
    df['CREDIT_PER_NON_CHILD'] = df['AMT_CREDIT'] / df['CNT_NON_CHILD']
    df['INCOME_PER_NON_CHILD'] = df['AMT_INCOME_TOTAL'] / df['CNT_NON_CHILD']
    df['INCOME_PER_CHILD'] = df['AMT_INCOME_TOTAL'] / (1 + df['CNT_CHILDREN'])

    # age bins
    df['RETIREMENT_AGE'] = (df['DAYS_BIRTH'] < -14000).astype(int)
    df['DAYS_BIRTH_QCUT'] = pd.qcut(df['DAYS_BIRTH'], q=5, labels=False)

    # long employemnt
    df['LONG_EMPLOYMENT'] = (df['DAYS_EMPLOYED'] < -2000).astype(int)

    bins = [0, 30000, 65000, 95000, 130000, 160000,
            190880, 220000, 275000, 325000, np.inf]
    labels = range(1, 11)
    df['INCOME_BAND'] = pd.cut(
        df['AMT_INCOME_TOTAL'], bins=bins, labels=labels, right=False)

    # details change
    df['DAYS_DETAILS_CHANGE_MUL'] = df['DAYS_LAST_PHONE_CHANGE'] * \
        df['DAYS_REGISTRATION'] * df['DAYS_ID_PUBLISH']
    df['DAYS_DETAILS_CHANGE_SUM'] = df['DAYS_LAST_PHONE_CHANGE'] + \
        df['DAYS_REGISTRATION'] + df['DAYS_ID_PUBLISH']

    # enquires
    df['AMT_ENQ_SUM'] = df['AMT_REQ_CREDIT_BUREAU_HOUR'] + df['AMT_REQ_CREDIT_BUREAU_DAY'] + df['AMT_REQ_CREDIT_BUREAU_WEEK'] + df[
        'AMT_REQ_CREDIT_BUREAU_MON'] + df['AMT_REQ_CREDIT_BUREAU_QRT'] + df['AMT_REQ_CREDIT_BUREAU_YEAR']
    df['ENQ_CREDIT_RATIO'] = df['AMT_ENQ_SUM'] / df['AMT_CREDIT']

    # flag asset
    df['FLAG_ASSET'] = np.nan
    filter_0 = (df['FLAG_OWN_CAR'] == 'N') & (df['FLAG_OWN_REALTY'] == 'N')
    filter_1 = (df['FLAG_OWN_CAR'] == 'Y') & (df['FLAG_OWN_REALTY'] == 'N')
    filter_2 = (df['FLAG_OWN_CAR'] == 'N') & (df['FLAG_OWN_REALTY'] == 'Y')
    filter_3 = (df['FLAG_OWN_CAR'] == 'Y') & (df['FLAG_OWN_REALTY'] == 'Y')

    df.loc[filter_0, 'FLAG_ASSET'] = 0
    df.loc[filter_1, 'FLAG_ASSET'] = 1
    df.loc[filter_2, 'FLAG_ASSET'] = 2
    df.loc[filter_3, 'FLAG_ASSET'] = 3

    group = ['ORGANIZATION_TYPE', 'NAME_EDUCATION_TYPE',
             'OCCUPATION_TYPE', 'AGE_RANGE', 'CODE_GENDER']
    df = do_median(df, group, 'EXT_SOURCES_MEAN', 'GROUP_EXT_SOURCES_MEDIAN')
    df = do_std(df, group, 'EXT_SOURCES_MEAN', 'GROUP_EXT_SOURCES_STD')
    df = do_mean(df, group, 'AMT_INCOME_TOTAL', 'GROUP_INCOME_MEAN')
    df = do_std(df, group, 'AMT_INCOME_TOTAL', 'GROUP_INCOME_STD')
    df = do_mean(df, group, 'CREDIT_TO_ANNUITY_RATIO',
                 'GROUP_CREDIT_TO_ANNUITY_MEAN')
    df = do_std(df, group, 'CREDIT_TO_ANNUITY_RATIO',
                'GROUP_CREDIT_TO_ANNUITY_STD')
    df = do_mean(df, group, 'AMT_CREDIT', 'GROUP_CREDIT_MEAN')
    df = do_mean(df, group, 'AMT_ANNUITY', 'GROUP_ANNUITY_MEAN')
    df = do_std(df, group, 'AMT_ANNUITY', 'GROUP_ANNUITY_STD')

    gc.collect()
    return df

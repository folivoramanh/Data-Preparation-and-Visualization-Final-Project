"""
This file is used to run the model and save the feature importance.

Author: Mai Anh Trinh
"""
import pandas as pd
from model import logistic_regression
from save_feature_importance import plot_feature_importance
from FeatureEngineering.utils import reduce_mem_usage

path_to_file = r'<replace your path to FeatEng here>'

df = pd.read_csv(path_to_file)
df = reduce_mem_usage(df, verbose=True)

# best parameter for woeencoder with k in range (0.867, 0.869)
best_params = {'tol': 0.000932217641215282, 'solver': 'liblinear',
               'max_iter': 172, 'C': 0.007069533932854347, 'penalty': 'l2',
               'fit_intercept': True, 'random_state': 555, 'class_weight': {0: 0.6187105361128231, 1: 4.101571905098737},
               'warm_start': True}

# best params for target encoder with k = 0.853
# best_params = {'tol': 0.0006286266445376868, 'solver': 'liblinear', 'max_iter': 176,
#                'C': 0.0006510378345745241, 'penalty': 'l2', 'fit_intercept': True, 'random_state': 1802,
#                'class_weight': {0: 0.8478248187345414, 1: 6.980630555705499}, 'warm_start': True}

feature_importance = logistic_regression(
    df=df, num_folds=5, feat_select="Kbest", tunning=None, best_params=best_params, k=0.867, filename='submit.csv')
plot_feature_importance(feature_importance=feature_importance)

import numpy as np
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import roc_auc_score
from lightgbm import LGBMClassifier
from sklearn.feature_selection import SelectKBest, f_regression


def feature_selection(train_data, target=None, method='Kbest', k=0.867):
    ''' Select features based on the method
    Parameters
    ----------
    train_data: DataFrame
        The training data
    target: Series
        The target variable - used for Kbest method
        Default: None
    method: str
            The method used to select features
            Default: 'Kbest'
    k: int
        The number of features to select
        Default: 0.867 - 86,7% of features are selected - base on best result from kaggle contest'''
    if method not in ['lgbm', 'Kbest']:
        raise ValueError('Method not supported')
    elif method == 'Kbest' and k is None:
        raise ValueError('Please specify the number of features to select')
    elif method == 'Kbest' and k < 0:
        raise ValueError(
            'Please specify a positive number of features to select')
    elif method == 'Kbest' and k > train_data.shape[1]:
        raise ValueError(
            'Please specify a number of features to select smaller than the number of features in the dataset')
    elif method == 'Kbest' and target is None:
        raise ValueError('Please specify the target variable')

    if method == 'lgbm':
        imp_cols = set()
        score = 1
        n = 1
        num_folds = 3
        while score > 0.8:
            select_train = train_data.drop(columns=imp_cols)
            fold = StratifiedKFold(n_splits=3, shuffle=True, random_state=1107)
            score = 0
            feature_importance = np.zeros_like(select_train.columns)
            for _, (train_i, val_i) in enumerate(fold.split(select_train, train_data['TARGET']), 1):
                x_train = select_train.iloc[train_i]
                x_val = select_train.iloc[val_i]
                y_train = train_data['TARGET'].iloc[train_i]
                y_val = train_data['TARGET'].iloc[val_i]
                lgbm = LGBMClassifier(nthread=-1,
                                      n_estimators=5000,
                                      learning_rate=0.01,
                                      max_depth=11,
                                      num_leaves=58,
                                      colsample_bytree=0.613,
                                      subsample=0.708,
                                      max_bin=407,
                                      reg_alpha=3.564,
                                      reg_lambda=4.930,
                                      min_child_weight=6,
                                      min_child_samples=165,
                                      silent=-1,
                                      verbose=-1)
                lgbm.fit(x_train, y_train, eval_metric='auc')
                feature_importance += lgbm.feature_importances_ / num_folds
                score += roc_auc_score(y_val,
                                       lgbm.predict_proba(x_val)[:, 1]) / num_folds
            imp_cols_i = np.where(np.abs(feature_importance) > 0)
            cols_imp = train_data.columns[imp_cols_i]

            if score > 0:
                imp_cols.update(cols_imp)
            n += 1

    elif method == 'Kbest' and k is not None and target is not None:
        if k < 1:
            k = int(float(k) * (train_data.shape[1]))
        else:
            k = int(k)
        selector = SelectKBest(f_regression, k=k)
        selector.fit_transform(train_data, target)
        imp_cols = selector.get_support()

    return list(imp_cols)

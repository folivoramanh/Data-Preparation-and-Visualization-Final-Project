import optuna
from tqdm import tqdm
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.model_selection import KFold
from FeatureEngineering.utils import replace_infinite
from FeatureEngineering import feature_selection


def logistic_regression(df, num_folds, feat_select="Kbest", tunning=None, best_params=None, k=100, filename=None, n_trials=20, debug=False):
    '''
    This function is used to train a logistic regression model on the data.

    Parameters
    ----------
    df : pandas.DataFrame
        The dataframe containing the data.
    num_folds : int
        The number of folds to use for cross validation.
    feat_select : str, default='Kbest'
        The feature selection method to use.
        Options are 'Kbest' and 'lgbm'.
    tunning : str, default=None
        The hyperparameter tunning method to use.
        Options are 'optuna' and None.
    best_params : dict, default=None
        The best hyperparameters to use.
        If None, the best hyperparameters will be found.
    k : int, default=100
        The number of features to select if feat_select='Kbest'.
        If in range(0, 1), the number of features will be selected based on the percentage of features to keep.
    filename : str, default=None
        The name of the file to save the predictions on the test set.
        If None, the predictions will not be saved.
    n_trials : int, default=20
        The number of trials to use for hyperparameter tunning.
    debug : bool, default=False
        Whether to run in debug mode or not.

    Returns
    -------
    feature_importance : pandas.DataFrame
        A dataframe containing the feature importance of the model.
    '''

    # Divide in training/validation and test data
    train_df = df[df['TARGET'].notnull()]
    test_df = df[df['TARGET'].isnull()]
    print(
        f"Starting Logistic Regression. Train shape: {train_df.shape}, test shape: {test_df.shape}")

    target = train_df['TARGET']

    imputer = SimpleImputer(strategy='median')
    scaler = StandardScaler()
    if feat_select == 'lgbm':
        not_select = train_df.select_dtypes('object').columns.to_list()
        not_select = ['SK_ID_CURR', 'SK_ID_BUREAU', 'SK_ID_PREV', 'index']
        feats = [f for f in train_df.columns if f not in not_select]
        feats = feature_selection(train_data=train_df[feats], method='lgbm')

        if 'TARGET' in feats:
            feats.remove('TARGET')

        train_df = replace_infinite(train_df)
        train_imputed = pd.DataFrame(imputer.fit_transform(
            train_df[feats]), columns=imputer.get_feature_names_out())
        train_scaled = scaler.fit_transform(train_imputed)
        if not debug:
            test_df = replace_infinite(test_df)
            test_imputed = pd.DataFrame(imputer.fit_transform(
                test_df[feats]), columns=imputer.get_feature_names_out())
            test_scaled = scaler.transform(test_imputed)

    elif feat_select == 'Kbest':
        not_select = ['TARGET', 'SK_ID_CURR',
                      'SK_ID_BUREAU', 'SK_ID_PREV', 'index']
        feats = [f for f in train_df.columns if f not in not_select]

        train_df = replace_infinite(train_df[feats])
        train_imputed = pd.DataFrame(imputer.fit_transform(
            train_df[feats]), columns=imputer.get_feature_names_out())

        selected_feats_mask = feature_selection(
            train_data=train_imputed, target=target, method='Kbest', k=k)
        selected_feats = np.array(imputer.get_feature_names_out())[
            selected_feats_mask]

        train_imputed = train_imputed.loc[:, selected_feats]
        train_scaled = scaler.fit_transform(train_imputed)
        if not debug:
            test_df = replace_infinite(test_df)
            test_imputed = pd.DataFrame(imputer.transform(
                test_df[feats]), columns=imputer.get_feature_names_out())
            test_imputed = test_imputed.loc[:, selected_feats]
            test_scaled = scaler.transform(test_imputed)

    X_train, X_test, y_train, y_test = train_test_split(
        train_scaled, target, test_size=0.25, random_state=123)

    num_folds = KFold(n_splits=num_folds, shuffle=True, random_state=1054)
    if tunning == 'optuna':
        def objective(trial):
            class_0 = np.linspace(0.25, 0.95, 200)
            class_1 = np.linspace(3, 8, 200)
            hyperparameters = {
                'tol': trial.suggest_uniform('tol', 1e-6, 1e-3),
                'solver': trial.suggest_categorical('solver', ['liblinear']),
                'max_iter': trial.suggest_int('max_iter', 1, 200),
                'C': trial.suggest_loguniform('C', 0.0001, 0.1),
                'penalty': trial.suggest_categorical('penalty', ['l2']),
                'fit_intercept': trial.suggest_categorical('fit_intercept', [True, False]),
                'random_state': trial.suggest_categorical('random_state', [42, 555, 1802]),
                'class_weight': {
                    0: trial.suggest_float('class_weight_0', class_0.min(), class_0.max()),
                    1: trial.suggest_float('class_weight_1', class_1.min(), class_1.max())
                },
                'warm_start': True
            }
            model = LogisticRegression(**hyperparameters)
            model.fit(X_train, y_train)
            preds = model.predict_proba(X_test)[:, 1]

            roc_auc = roc_auc_score(y_test, preds)
            return roc_auc

        study = optuna.create_study(direction='maximize')

        with tqdm(total=20) as pbar:
            def update_pbar(study, trial):
                pbar.update(1)

            study.optimize(objective, n_trials=n_trials,
                           callbacks=[update_pbar])

        # Get the best hyperparameters
        best_params = {
            'tol': study.best_params['tol'],
            'solver': study.best_params['solver'],
            'max_iter': study.best_params['max_iter'],
            'C': study.best_params['C'],
            'penalty': study.best_params['penalty'],
            'fit_intercept': study.best_params['fit_intercept'],
            'random_state': study.best_params['random_state'],
            'class_weight': {0: study.best_params['class_weight_0'], 1: study.best_params['class_weight_1']},
            'warm_start': True
        }
    else:
        best_params = best_params

    # Train the model with the best hyperparameters on the full training set
    final_model = LogisticRegression(**best_params)
    final_model.fit(X_train, y_train)

    # Get the feature importances (absolute values of coefficients)
    coefficients = np.abs(final_model.coef_[0])
    feature_importance = pd.DataFrame(
        {'Feature': train_imputed.columns, 'Importance': np.abs(coefficients)})

    # Calculate score on validate set
    # Calculate the ROC-AUC score
    roc_auc = roc_auc_score(y_test, final_model.predict_proba(X_test)[:, 1])

    # Calculate Gini index
    gini_index = 2 * roc_auc - 1

    print('Best Hyperparameters:', best_params)
    print('ROC-AUC on Validation Set:', roc_auc)
    print('Gini Index on Validation Set:', gini_index)

    if not debug:
        # Predict for test set and extract csv file
        submit = test_df[['SK_ID_CURR']]
        submit['TARGET'] = final_model.predict_proba(test_scaled)[:, 1]
        if filename:
            submission_file_name = filename
            submit.to_csv(submission_file_name, index=False)

    return feature_importance

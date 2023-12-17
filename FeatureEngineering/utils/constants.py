'''This file contains constants used in the project.

Constants:
    BUREAU_AGG: Aggregate features to dseb63_bureau.csv by SK_ID_CURR.
    BUREAU_ACTIVE_AGG: Aggregate features to dseb63_bureau.csv for active loans by SK_ID_CURR.
    BUREAU_CLOSED_AGG: Aggregate features to dseb63_bureau.csv for closed loans by SK_ID_CURR.
    BUREAU_LOAN_TYPE_AGG: Aggregate features to dseb63_bureau.csv 
                            by loan type (LoanType) and by SK_ID_CURR.
    BUREAU_TIME_AGG: Aggregate features to dseb63_bureau.csv 
                        by number of months in balance (MONTHS_BALANCE_SIZE) and by SK_ID_CURR.

    PREVIOUS_AGG: Aggregate features to dseb63_previous_application.csv by SK_ID_CURR.
    PREVIOUS_ACTIVE_AGG: Aggregate features to dseb63_previous_application.csv 
                                                    for active loans by SK_ID_CURR.
    PREVIOUS_APPROVED_AGG: Aggregate features to dseb63_previous_application.csv 
                                                    for approved loans by SK_ID_CURR.
    PREVIOUS_REFUSED_AGG: Aggregate features to dseb63_previous_application.csv 
                                                    for refused loans by SK_ID_CURR.
    PREVIOUS_LATE_PAYMENTS_AGG: Aggregate features to dseb63_previous_application.csv 
                                                    for late payments by SK_ID_CURR.
    PREVIOUS_LOAN_TYPE_AGG: Aggregate features to dseb63_previous_application.csv 
                                                    by loan type (LoanType) and by SK_ID_CURR.
    PREVIOUS_TIME_AGG: Aggregate features to dseb63_previous_application.csv
                        by number of months in balance (MONTHS_BALANCE_SIZE) and by SK_ID_CURR.

    POS_CASH_AGG: Aggregate features to dseb63_POS_CASH_balance.csv by SK_ID_CURR.

    INSTALLMENTS_AGG: Aggregate features to dseb63_installments_payments.csv by SK_ID_CURR.
    INSTALLMENTS_TIME_AGG: Aggregate features to dseb63_installments_payments.csv
                        by number of months in balance (MONTHS_BALANCE_SIZE) and by SK_ID_CURR.

    CREDIT_CARD_AGG: Aggregate features to dseb63_credit_card_balance.csv by SK_ID_CURR.
    CREDIT_CARD_TIME_AGG: Aggregate features to dseb63_credit_card_balance.csv 
                        by number of months in balance (MONTHS_BALANCE_SIZE) and by SK_ID_CURR.
    
    rolling_columns: list of column to calculate the 
                            rolling Exponential Weighted Moving Average over months
'''

BUREAU_AGG = {
    'SK_ID_BUREAU': ['nunique'],

    'AMT_CREDIT_MAX_OVERDUE': ['max', 'mean'],
    'AMT_CREDIT_SUM': ['max', 'mean', 'sum'],
    'AMT_CREDIT_SUM_DEBT': ['max', 'mean', 'sum'],
    'AMT_CREDIT_SUM_OVERDUE': ['max', 'mean', 'sum'],
    'AMT_CREDIT_SUM_LIMIT': ['mean', 'sum'],
    'AMT_ANNUITY': ['mean'],

    'BUREAU_CREDIT_FACT_DIFF': ['min', 'max', 'mean'],
    'BUREAU_CREDIT_ENDDATE_DIFF': ['min', 'max', 'mean'],
    'BUREAU_CREDIT_DEBT_RATIO': ['min', 'max', 'mean'],
    'BUREAU_IS_DPD': ['mean', 'sum'],
    'BUREAU_IS_DPD_OVER120': ['mean', 'sum'],

    'CNT_CREDIT_PROLONG': ['sum'],

    'CREDIT_ACTIVE_Active': ['mean'],
    'CREDIT_ACTIVE_Closed': ['mean'],
    'CREDIT_ACTIVE_Sold': ['mean'],
    'CREDIT_DAY_OVERDUE': ['max', 'mean', 'min'],
    'CREDIT_TYPE_Consumer credit': ['mean'],
    'CREDIT_TYPE_Credit card': ['mean'],
    'CREDIT_TYPE_Car loan': ['mean'],
    'CREDIT_TYPE_Mortgage': ['mean'],
    'CREDIT_TYPE_Microloan': ['mean'],

    'DAYS_CREDIT': ['min', 'max', 'mean', 'var'],
    'DAYS_CREDIT_ENDDATE': ['min', 'max', 'mean'],
    'DAYS_CREDIT_UPDATE': ['mean'],
    'DAYS_ENDDATE_FACT': ['min', 'max', 'mean'],
    'DEBT_CREDIT_DIFF': ['mean', 'sum'],

    'ENDDATE_DIF': ['min', 'max', 'mean'],

    'LL_AMT_CREDIT_SUM_OVERDUE': ['mean'],
    'LL_DEBT_CREDIT_DIFF': ['mean'],
    'LL_STATUS_12345': ['mean'],

    'MONTHS_BALANCE_MIN': ['min'],
    'MONTHS_BALANCE_MAX': ['max'],
    'MONTHS_BALANCE_MEAN': ['mean', 'var'],
    'MONTHS_BALANCE_SIZE': ['mean', 'sum'],

    'STATUS_0': ['mean'],
    'STATUS_1': ['mean'],
    'STATUS_12345': ['mean'],
    'STATUS_C': ['mean'],
    'STATUS_X': ['mean'],
}

BUREAU_ACTIVE_AGG = {
    'AMT_CREDIT_MAX_OVERDUE': ['max', 'mean'],
    'AMT_CREDIT_SUM': ['max', 'sum'],
    'AMT_CREDIT_SUM_DEBT': ['mean', 'sum'],
    'AMT_CREDIT_SUM_OVERDUE': ['max', 'mean'],

    'CREDIT_TO_ANNUITY_RATIO': ['mean'],

    'DAYS_CREDIT': ['max', 'mean'],
    'DAYS_CREDIT_ENDDATE': ['min', 'max'],
    'DAYS_CREDIT_UPDATE': ['min', 'mean'],

    'DEBT_PERCENTAGE': ['mean'],
    'DEBT_CREDIT_DIFF': ['mean'],

    'MONTHS_BALANCE_MEAN': ['mean', 'var'],
    'MONTHS_BALANCE_SIZE': ['mean', 'sum'],
}

BUREAU_CLOSED_AGG = {
    'AMT_CREDIT_MAX_OVERDUE': ['max', 'mean'],
    'AMT_CREDIT_SUM_OVERDUE': ['mean'],
    'AMT_CREDIT_SUM': ['max', 'mean', 'sum'],
    'AMT_CREDIT_SUM_DEBT': ['max', 'sum'],

    'DAYS_CREDIT': ['max', 'var'],
    'DAYS_CREDIT_ENDDATE': ['max'],
    'DAYS_CREDIT_UPDATE': ['max'],

    'DCREDIT_DOVERDUE_DIFF': ['mean'],  # credit overdue diff
    'DCREDIT_DENDFACT_DIFF': ['mean'],  # credit end fact diff
    'DUPDATE_DENDATE_DIFF': ['mean'],  # update end date diff
    'ENDDATE_DIF': ['mean'],
    'STATUS_12345': ['mean'],

}

BUREAU_LOAN_TYPE_AGG = {
    'AMT_CREDIT_MAX_OVERDUE': ['mean', 'max'],
    'AMT_CREDIT_SUM': ['mean', 'max'],
    'AMT_CREDIT_SUM_DEBT': ['mean', 'max'],


    'DAYS_CREDIT': ['mean', 'max'],
    'DAYS_CREDIT_ENDDATE': ['max'],

    'DEBT_PERCENTAGE': ['mean'],
    'DEBT_CREDIT_DIFF': ['mean'],
    'DEBT_CREDIT_LIMIT_DIFF': ['mean'],
    'DEBT_CREDIT_OVERDUE_DIFF': ['mean']
}

BUREAU_TIME_AGG = {
    'AMT_CREDIT_MAX_OVERDUE': ['max', 'mean'],
    'AMT_CREDIT_SUM_OVERDUE': ['mean'],
    'AMT_CREDIT_SUM': ['max', 'sum'],
    'AMT_CREDIT_SUM_DEBT': ['mean', 'sum'],

    'DEBT_PERCENTAGE': ['mean'],
    'DEBT_CREDIT_DIFF': ['mean'],
    'DEBT_CREDIT_LIMIT_DIFF': ['mean'],
    'DEBT_CREDIT_OVERDUE_DIFF': ['mean'],

    'STATUS_0': ['mean'],
    'STATUS_12345': ['mean'],
}

PREVIOUS_AGG = {
    'SK_ID_PREV': ['nunique'],

    'AMT_ANNUITY': ['min', 'max', 'mean'],
    'AMT_DOWN_PAYMENT': ['max', 'mean'],
    'APPLICATION_CREDIT_DIFF': ['min', 'max', 'mean'],
    'APPLICATION_CREDIT_RATIO': ['min', 'max', 'mean', 'var'],

    'CNT_PAYMENT': ['max', 'mean'],
    'CREDIT_TO_ANNUITY_RATIO': ['mean', 'max'],

    'DAYS_TERMINATION': ['max'],
    'DAYS_DECISION': ['min', 'max', 'mean'],
    'DOWN_PAYMENT_TO_CREDIT': ['mean'],

    'HOUR_APPR_PROCESS_START': ['min', 'max', 'mean'],

    'NEW_CREDIT_GOODS_RATE': ['mean', 'max', 'var', 'min'],
    'NEW_END_DIFF': ['min', 'max'],
    'NEW_DAYS_DUE_DIFF': ['min', 'max'],
    'NEW_RETURN_DAY': ['min', 'max'],

    'RATE_DOWN_PAYMENT': ['max', 'mean'],
}

PREVIOUS_ACTIVE_AGG = {
    'SK_ID_PREV': ['nunique'],

    'AMT_ANNUITY': ['max', 'sum'],
    'AMT_APPLICATION': ['max', 'mean'],
    'AMT_CREDIT': ['sum'],
    'AMT_DOWN_PAYMENT': ['max', 'mean'],
    'AMT_PAYMENT': ['sum'],

    'CNT_PAYMENT': ['mean', 'sum'],

    'DAYS_DECISION': ['min', 'mean'],
    'DAYS_LAST_DUE_1ST_VERSION': ['min', 'max', 'mean'],

    'INSTALMENT_PAYMENT_DIFF': ['mean', 'max'],

    'REMAINING_DEBT': ['max', 'mean', 'sum'],
    'REPAYMENT_RATIO': ['mean'],

    'SIMPLE_INTERESTS': ['mean'],
}

PREVIOUS_APPROVED_AGG = {
    'SK_ID_PREV': ['nunique'],

    'AMT_ANNUITY': ['min', 'max', 'mean'],
    'AMT_CREDIT': ['min', 'max', 'mean'],
    'AMT_DOWN_PAYMENT': ['max'],
    'AMT_GOODS_PRICE': ['max'],
    'AMT_INTEREST': ['min', 'max', 'mean'],
    'APPLICATION_CREDIT_DIFF': ['max'],
    'APPLICATION_CREDIT_RATIO': ['min', 'max', 'mean'],

    'CNT_PAYMENT': ['max', 'mean'],
    'CREDIT_TO_ANNUITY_RATIO': ['mean', 'max'],

    'DAYS_DECISION': ['min', 'mean'],
    'DAYS_TERMINATION': ['mean'],
    'DAYS_FIRST_DRAWING': ['max', 'mean'],
    'DAYS_FIRST_DUE': ['min', 'mean'],
    'DAYS_LAST_DUE_1ST_VERSION': ['min', 'max', 'mean'],
    'DAYS_LAST_DUE': ['max', 'mean'],
    'DAYS_LAST_DUE_DIFF': ['min', 'max', 'mean'],

    'HOUR_APPR_PROCESS_START': ['min', 'max'],

    'INTEREST_SHARE': ['min', 'max', 'mean'],
    'INTEREST_RATE': ['min', 'max', 'mean'],

    'SIMPLE_INTERESTS': ['min', 'max', 'mean'],
}

PREVIOUS_REFUSED_AGG = {
    'AMT_APPLICATION': ['max', 'mean'],
    'AMT_CREDIT': ['min', 'max'],
    'APPLICATION_CREDIT_DIFF': ['min', 'max', 'mean', 'var'],
    'APPLICATION_CREDIT_RATIO': ['min', 'mean'],

    'CNT_PAYMENT': ['max', 'mean'],

    'DAYS_DECISION': ['min', 'max', 'mean'],

    'NAME_CONTRACT_TYPE_Consumer loans': ['mean'],
    'NAME_CONTRACT_TYPE_Cash loans': ['mean'],
    'NAME_CONTRACT_TYPE_Revolving loans': ['mean'],
}

PREVIOUS_LATE_PAYMENTS_AGG = {
    'APPLICATION_CREDIT_DIFF': ['min'],

    'DAYS_DECISION': ['min', 'max', 'mean'],
    'DAYS_LAST_DUE_1ST_VERSION': ['min', 'max', 'mean'],

    'NAME_CONTRACT_TYPE_Consumer loans': ['mean'],
    'NAME_CONTRACT_TYPE_Cash loans': ['mean'],
    'NAME_CONTRACT_TYPE_Revolving loans': ['mean'],
}

PREVIOUS_LOAN_TYPE_AGG = {
    'AMT_CREDIT': ['sum'],
    'AMT_ANNUITY': ['mean', 'max'],
    'APPLICATION_CREDIT_DIFF': ['min', 'var'],
    'APPLICATION_CREDIT_RATIO': ['min', 'max', 'mean'],

    'DAYS_DECISION': ['max'],
    'DAYS_LAST_DUE_1ST_VERSION': ['max', 'mean'],

    'SIMPLE_INTERESTS': ['min', 'mean', 'max', 'var'],
}
PREVIOUS_TIME_AGG = {
    'AMT_CREDIT': ['sum'],
    'AMT_ANNUITY': ['mean', 'max'],
    'APPLICATION_CREDIT_DIFF': ['min'],
    'APPLICATION_CREDIT_RATIO': ['min', 'max', 'mean'],

    'DAYS_DECISION': ['min', 'mean'],
    'DAYS_LAST_DUE_1ST_VERSION': ['min', 'max', 'mean'],

    'NAME_CONTRACT_TYPE_Consumer loans': ['mean'],
    'NAME_CONTRACT_TYPE_Cash loans': ['mean'],
    'NAME_CONTRACT_TYPE_Revolving loans': ['mean'],

    'SIMPLE_INTERESTS': ['mean', 'max'],
}

POS_CASH_AGG = {
    'SK_ID_PREV': ['nunique'],
    'SK_ID_CURR': ['count'],

    'EXP_CNT_INSTALMENT': ['last', 'min', 'max', 'mean', 'sum'],
    'EXP_CNT_INSTALMENT_FUTURE': ['last', 'min', 'max', 'mean', 'sum'],

    'LATE_PAYMENT': ['mean'],

    'MONTHS_BALANCE': ['min', 'max', 'size'],

    'POS_IS_DPD': ['mean', 'sum'],
    'POS_IS_DPD_UNDER_120': ['mean', 'sum'],
    'POS_IS_DPD_OVER_120': ['mean', 'sum'],

    'SK_DPD': ['max', 'mean', 'sum', 'var', 'min'],
    'SK_DPD_DEF': ['max', 'mean', 'sum'],
}
INSTALLMENTS_AGG = {
    'SK_ID_PREV': ['size', 'nunique'],

    'AMT_INSTALMENT': ['min', 'max', 'mean', 'sum'],
    'AMT_PAYMENT': ['min', 'max', 'mean', 'sum'],

    'DAYS_ENTRY_PAYMENT': ['min', 'max', 'mean'],
    'DPD': ['max', 'mean', 'var'],
    'DBD': ['max', 'mean', 'var'],
    'DPD_7': ['mean'],
    'DPD_15': ['mean'],

    'INS_IS_DPD_UNDER_120': ['mean', 'sum'],
    'INS_IS_DPD_OVER_120': ['mean', 'sum'],

    'LATE_PAYMENT': ['mean', 'sum'],
    'LATE_PAYMENT_RATIO': ['mean'],

    'PAID_OVER': ['mean'],
    'PAYMENT_DIFFERENCE': ['mean'],
    'PAYMENT_RATIO': ['mean'],

    'SIGNIFICANT_LATE_PAYMENT': ['mean', 'sum'],
}

INSTALLMENTS_TIME_AGG = {
    'SK_ID_PREV': ['size'],

    'AMT_INSTALMENT': ['min', 'max', 'mean', 'sum'],
    'AMT_PAYMENT': ['min', 'max', 'mean', 'sum'],

    'DAYS_ENTRY_PAYMENT': ['min', 'max', 'mean'],
    'DPD': ['max', 'mean', 'var'],
    'DBD': ['max', 'mean', 'var'],
    'DPD_7': ['mean'],
    'DPD_15': ['mean'],

    'LATE_PAYMENT': ['mean'],
    'LATE_PAYMENT_RATIO': ['mean'],

    'PAYMENT_DIFFERENCE': ['mean'],
    'PAYMENT_RATIO': ['mean'],

    'SIGNIFICANT_LATE_PAYMENT': ['mean'],
}


CREDIT_CARD_AGG = {
    'AMT_BALANCE': ['sum', 'min', 'max'],
    'AMT_CREDIT_LIMIT_ACTUAL': ['max', 'sum', 'min'],
    'AMT_DRAWINGS_ATM_CURRENT': ['max', 'sum'],
    'AMT_DRAWINGS_CURRENT': ['max', 'sum'],
    'AMT_DRAWINGS_POS_CURRENT': ['max', 'sum'],
    'AMT_DRAWING_SUM': ['sum', 'max'],
    'AMT_INST_MIN_REGULARITY': ['max', 'mean', 'min'],
    'AMT_INTEREST_RECEIVABLE': ['min', 'mean'],
    'AMT_PAYMENT_TOTAL_CURRENT': ['max', 'mean', 'sum', 'var'],
    'AMT_TOTAL_RECEIVABLE': ['max', 'mean', 'sum'],

    'BALANCE_LIMIT_RATIO': ['mean', 'max', 'min'],

    'CNT_DRAWING_SUM': ['sum', 'max'],
    'CNT_DRAWINGS_ATM_CURRENT': ['max', 'mean', 'sum'],
    'CNT_DRAWINGS_CURRENT': ['max', 'mean', 'sum'],
    'CNT_DRAWINGS_POS_CURRENT': ['mean', 'sum', 'max'],

    'EXP_AMT_BALANCE': ['last'],
    'EXP_AMT_CREDIT_LIMIT_ACTUAL': ['last'],
    'EXP_AMT_RECEIVABLE_PRINCIPAL': ['last'],
    'EXP_AMT_RECEIVABLE': ['last'],
    'EXP_AMT_TOTAL_RECEIVABLE': ['last'],
    'EXP_AMT_DRAWING_SUM': ['last'],
    'EXP_BALANCE_LIMIT_RATIO': ['last'],
    'EXP_CNT_DRAWING_SUM': ['last'],
    'EXP_MIN_PAYMENT_RATIO': ['last'],
    'EXP_PAYMENT_MIN_DIFF': ['last'],
    'EXP_MIN_PAYMENT_TOTAL_RATIO': ['last'],
    'EXP_AMT_INTEREST_RECEIVABLE': ['last'],
    'EXP_SK_DPD_RATIO': ['last'],

    'LIMIT_USE': ['max', 'mean'],
    'LATE_PAYMENT': ['max', 'sum'],

    'MIN_PAYMENT_RATIO': ['min', 'mean'],
    'MIN_PAYMENT_TOTAL_RATIO': ['min', 'mean'],
    'MONTHS_BALANCE': ['min'],

    'SK_DPD': ['mean', 'max', 'sum'],
    'SK_DPD_DEF': ['max', 'sum'],
    'SK_DPD_RATIO': ['max', 'mean'],

    'PAYMENT_DIV_MIN': ['min', 'mean'],
    'PAYMENT_MIN_DIFF': ['min', 'mean'],
    'PAYMENT_MIN_TOTAL_DIFF': ['min', 'mean'],
}

CREDIT_CARD_TIME_AGG = {
    'AMT_BALANCE': ['mean', 'max'],

    'CNT_DRAWINGS_ATM_CURRENT': ['mean'],

    'EXP_AMT_DRAWING_SUM': ['last'],
    'EXP_BALANCE_LIMIT_RATIO': ['last'],
    'EXP_CNT_DRAWING_SUM': ['last'],
    'EXP_MIN_PAYMENT_RATIO': ['last'],
    'EXP_PAYMENT_MIN_DIFF': ['last'],
    'EXP_MIN_PAYMENT_TOTAL_RATIO': ['last'],
    'EXP_AMT_INTEREST_RECEIVABLE': ['last'],
    'EXP_SK_DPD_RATIO': ['last'],

    'LIMIT_USE': ['max', 'mean'],

    'SK_DPD': ['max', 'sum'],
}

rolling_columns = [
    'AMT_BALANCE',
    'AMT_CREDIT_LIMIT_ACTUAL',
    'AMT_DRAWING_SUM',
    'AMT_INTEREST_RECEIVABLE',
    'AMT_RECEIVABLE',
    'AMT_RECEIVABLE_PRINCIPAL',
    'AMT_TOTAL_RECEIVABLE',

    'BALANCE_LIMIT_RATIO',

    'CNT_DRAWING_SUM',

    'MIN_PAYMENT_RATIO',
    'MIN_PAYMENT_TOTAL_RATIO',

    'PAYMENT_MIN_DIFF',

    'SK_DPD_RATIO']

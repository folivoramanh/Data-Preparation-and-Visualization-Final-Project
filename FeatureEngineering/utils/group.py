import pandas as pd


def group(df_to_agg, prefix, aggregations, aggregate_by='SK_ID_CURR'):
    agg_df = df_to_agg.groupby(aggregate_by).agg(aggregations)
    agg_df.columns = pd.Index(['{}{}_{}'.format(prefix, e[0], e[1].upper())
                               for e in agg_df.columns.tolist()])
    return agg_df.reset_index()


def group_and_merge(df_to_agg, df_to_merge, prefix, aggregations, aggregate_by='SK_ID_CURR'):
    agg_df = group(df_to_agg, prefix, aggregations, aggregate_by=aggregate_by)
    return df_to_merge.merge(agg_df, how='left', on=aggregate_by)

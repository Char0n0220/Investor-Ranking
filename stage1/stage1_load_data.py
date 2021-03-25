from sql_scripts import traditional_investor_stage1, non_traditional_investor_stage1
from utilities.helpers import standatd_tenor_conversion, stage1_scoring
import numpy as np


def load_stage1_tra(connection, start_date, issuer, currency, sector, tenor):
    tra_investor_df = connection.read_sql(traditional_investor_stage1.format(start_date, issuer, currency, sector))

    # Calculate Standard Tenor:
    tra_investor_df.dropna(subset=['issue_date', 'maturity_date'], inplace=True)
    tra_investor_df['tenor_raw'] = (tra_investor_df['maturity_date'] -
                                    tra_investor_df['issue_date']) / np.timedelta64(1, 'Y')
    tra_investor_df['tenor'] = tra_investor_df['tenor_raw'].map(lambda x: standatd_tenor_conversion(x))

    # Save ISIN info for future use:
    isin_info = tra_investor_df[['investor', 'isin', 'issue_date', 'maturity_date', 'tenor']].drop_duplicates()
    isin_info.reset_index(inplace=True, drop=True)

    # Filter by Tenor as required:
    tra_investor_df = tra_investor_df[tra_investor_df['tenor'] == tenor]

    # Apply aggregation accordingly:
    tra_investor_agg_raw = tra_investor_df[['investor', 'investor_id', 'invest_amount', 'invest_change']]
    tra_investor_agg_raw['invest_count'] = 1
    tra_investor_stage1 = tra_investor_agg_raw.groupby(by=['investor', 'investor_id']).agg({'invest_amount': 'sum',
                                                                                            'invest_change': 'sum',
                                                                                            'invest_count': 'count'}).reset_index()
    # Scoring
    tra_investor_stage1_score = stage1_scoring(tra_investor_stage1)
    return tra_investor_stage1_score, tra_investor_stage1, isin_info


def load_stage1_non_tra(connection, start_date, currency, sector, tenor, tra_investor_id_list):
    mix_investor_df = connection.read_sql(non_traditional_investor_stage1.format(start_date, currency, sector))

    # Generate Non Traditional Investor: Mixed - Traditional
    #tra_investor_df, _, _ = load_stage1_tra(connection, date_start, issuer, currency, sector, tenor)
    non_tra_investor_df = mix_investor_df[~mix_investor_df.investor_id.isin(tra_investor_id_list)]

    # Calculate Standard Tenor:
    non_tra_investor_df.dropna(subset=['issue_date', 'maturity_date'], inplace=True)
    non_tra_investor_df['tenor_raw'] = (non_tra_investor_df['maturity_date'] -
                                        non_tra_investor_df['issue_date']) / np.timedelta64(1, 'Y')
    non_tra_investor_df['tenor'] = non_tra_investor_df['tenor_raw'].map(lambda x: standatd_tenor_conversion(x))

    # Save ISIN info for future use:
    isin_info = non_tra_investor_df[['investor', 'isin', 'issue_date', 'maturity_date', 'tenor']].drop_duplicates()
    isin_info.reset_index(inplace=True, drop=True)

    # Filter by Tenor as required:
    non_tra_investor_df = non_tra_investor_df[non_tra_investor_df['tenor'] == tenor]

    # Apply aggregation accordingly:
    non_tra_investor_agg_raw = non_tra_investor_df[['investor', 'investor_id', 'invest_amount', 'invest_change']]
    non_tra_investor_agg_raw['invest_count'] = 1
    non_tra_investor_stage1 = non_tra_investor_agg_raw.groupby(by=['investor',
                                                                   'investor_id']).agg({'invest_amount': 'sum',
                                                                                        'invest_change': 'sum',
                                                                                        'invest_count': 'count'}).reset_index()
    # Scoring
    non_tra_investor_stage1_score = stage1_scoring(non_tra_investor_stage1)
    return non_tra_investor_stage1_score, non_tra_investor_stage1, isin_info


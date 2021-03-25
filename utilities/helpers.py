from sklearn.preprocessing import MinMaxScaler


def standatd_tenor_conversion(tenor):
    # Get standard tenor
    try:
        if tenor <= 2.5:
            standard_tenor = 2
        elif tenor <= 4:
            standard_tenor = 3
        elif tenor <= 6:
            standard_tenor = 5
        elif tenor <= 8.5:
            standard_tenor = 7
        elif (tenor <= 12.5) & (tenor > 8.5):
            standard_tenor = 10
        elif (tenor <= 18.5) & (tenor > 12.5):
            standard_tenor = 15
        elif (tenor <= 26) & (tenor > 18.5):
            standard_tenor = 22
        elif (tenor > 26):
            standard_tenor = 30
    except:
        raise ValueError("Tenor is not a valid numerical value, check if start_date & end_date are NULL")
    else:
        return standard_tenor


def stage1_scoring(df):
    # Min Max Scalar:
    stage1_scaler = MinMaxScaler(feature_range=(0.1, 1))
    df.fillna(0, inplace=True)
    df['size_score'] = stage1_scaler.fit_transform(df[['invest_amount']])
    df['frequency_score'] = stage1_scaler.fit_transform(df[['invest_count']])
    df['rebalancing_score'] = stage1_scaler.fit_transform(df[['invest_change']])
    df = df[['investor', 'investor_id', 'size_score', 'frequency_score', 'rebalancing_score']]
    return df

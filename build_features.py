from connection import get_engine
import pandas as pd

def calculate_daily_return(rate_series):
    return rate_series.pct_change()
def build_features(group:pd.DataFrame):
    group=group.sort_values('date').copy()
    group['daily_return']=calculate_daily_return(group['rate'])
    group['rolling_avg_week']=group['rate'].rolling(window=7).mean()
    group['rolling_std_week']=group['rate'].rolling(window=7).std()
    group['lag_1d']=group['rate'].shift(1)
    group['lag_7d']=group['rate'].shift(7)
    return group

engine=get_engine()
pd.set_option('display.max_columns',None)
df=pd.read_sql(
    "select date,base_currency,quote_currency,rate from exchange_rate_daily order by base_currency,quote_currency,date",engine
)
if __name__=="__main__":
    df_features=df.groupby(['base_currency','quote_currency'],group_keys=False)[['date','base_currency','quote_currency','rate']].apply(build_features)
    # print(len(df_features))
    df_features_clean=df_features.dropna(subset=['daily_return','rolling_avg_week','rolling_std_week','lag_1d','lag_7d'])
    # print(df_features_clean.head(15))
    df_features_clean[['daily_return','rolling_avg_week','rolling_std_week','lag_1d','lag_7d']]=df_features_clean[['daily_return','rolling_avg_week','rolling_std_week','lag_1d','lag_7d']].round(6)
    # print(df_features_clean.isnull().sum())
    df_features_clean=df_features_clean.rename(
        columns={
            'rolling_avg_week':'rolling_avg_7d',
            'rolling_std_week':'rolling_std_7d'
        }
    )
    df_features_clean.to_sql(
        'rate_features',
        engine,
        if_exists='append',
        index=False,
        method='multi',
        chunksize=5000
    )
    print(f"Загружено строк:{len(df_features_clean)}")
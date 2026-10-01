import pandas as pd
from connection import get_engine
df=pd.read_csv('raw_data.csv',encoding='utf-8-sig')
df=df.rename(columns={
    'base':'base_currency',
    'quote':'quote_currency'
})
df['date']=pd.to_datetime(df['date']).dt.date
df = df[~((df['quote_currency'] == 'BYN') & (df['date'] < pd.Timestamp('2016-07-01').date()))]
df = df[~((df['base_currency'] == 'BYN') & (df['date'] < pd.Timestamp('2016-07-01').date()))]
print(f"После фильтрации: {len(df)} строк")
engine=get_engine()
df.to_sql(
    'exchange_rate_daily',
    engine,
    if_exists="append",
    index=False,
    method='multi',
    chunksize=5000
)
print(f"Загружено:{len(df)} строк")
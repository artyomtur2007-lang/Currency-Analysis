import pandas as pd
import requests
import time
url='https://api.frankfurter.dev/v2/rates'
currency_pairs=[
    ('USD','EUR'),
    ('USD','RUB'),
    ('EUR','RUB'),
    ('EUR','BYN'),
    ('RUB','BYN')
]
start_date='2016-01-01'
end_date='2026-01-04'
records=[]
for base,quote in currency_pairs:
    params={'base':base,
            'quotes':quote,
            'from':start_date,
            'to':end_date}
    try:
        response=requests.get(url,params=params,timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Ошибка для пары {base},{quote}")
        continue
    data=response.json()
    records.extend(data)
    time.sleep(0.5)
df=pd.DataFrame(records)
print(df.head())
df.to_csv('raw_data.csv',index=False)
print('Успешно сохранено')


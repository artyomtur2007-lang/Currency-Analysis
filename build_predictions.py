import pandas as pd
from connection import get_engine
from sklearn.metrics import mean_absolute_error
from sklearn.linear_model import LinearRegression

pd.set_option('display.max_columns',None)
engine=get_engine()
df=pd.read_sql('''select date,base_currency,quote_currency,rate,daily_return,rolling_avg_7d,rolling_std_7d,
    lag_1d,lag_7d from rate_features order by base_currency,quote_currency,date''',engine)

df['target']=df.groupby(['base_currency','quote_currency'])['rate'].shift(periods=-1)
df=df.dropna(subset=['target'])

feature_cols=['daily_return','rolling_avg_7d','rolling_std_7d','lag_1d','lag_7d']
test_days=60

metric_result=[]
prediction_rows=[]
for (base,quote),group in df.groupby(['base_currency','quote_currency']):
    group=group.sort_values('date')
    train=group.iloc[:-test_days]
    test=group.iloc[-test_days:]
    X_train=train[feature_cols]
    y_train=train['target']
    X_test=test[feature_cols]
    y_test=test['target']

    model=LinearRegression()
    model.fit(X_train,y_train)
    predictions=model.predict(X_test)

    naive_mae=mean_absolute_error(y_test,test['rate'])
    model_mae=mean_absolute_error(y_test,predictions)

    metric_result.append({
        'base_currency':base,
        'quote_currency':quote,
        'naive_mae':naive_mae,
        'model_mae':model_mae,
        'improvement_%':(naive_mae-model_mae)/naive_mae*100
    })
    pair_prediction=pd.DataFrame({
        'date':test['date'].values,
        'base_currency':base,
        'quote_currency':quote,
        'actual_rate':y_test.values,
        'predicted_rate':predictions,
        'naive_prediction':test['rate'].values,
        'model_name':'LinearRegression'
    })
    prediction_rows.append(pair_prediction)

metrics_df=pd.DataFrame(metric_result)
result_df=pd.concat(prediction_rows,ignore_index=True)
# print(metrics_df)
# print(result_df.head())
result_df.to_sql(
    'rate_predictions',
    engine,
    if_exists='append',
    index=False,
    method="multi",
    chunksize=5000
)
print(f"Загружено прогнозов:{len(result_df)}")